import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import chardet
import os
import drillhole_calcs as dh_calcs
from fuzzywuzzy import fuzz
from datetime import datetime

st.set_page_config(page_title="My App", page_icon=":guardsman:", layout="wide")

# Initialize the session state list
if 'files_list' not in st.session_state:
    files_list = st.empty()
    files_list = st.session_state.get("files_list", [])

if "log" not in st.session_state:
    st.session_state["log"] = []

if "df_drilltraces" not in st.session_state:
    st.session_state["df_drilltraces"] = pd.DataFrame()

st.session_state["log"].append({"timestamp": datetime.now(), "action": "App started", "username": "user1"})

class File:
    def __init__(self, name, df, category, columns=[], columns_dtypes=[], required_cols={}, simplified_dtypes={}, user_defined_dtypes={}, df_reassigned_dtypes={}):
        self.name = name
        self.df = df
        self.category = category
        self.columns = columns
        self.columns_dtypes = columns_dtypes
        self.required_cols = required_cols
        self.simplified_dtypes = simplified_dtypes
        self.user_defined_dtypes = user_defined_dtypes
        self.df_reassigned_dtypes = df_reassigned_dtypes


def read_file_chardet(uploaded_file):

    # Use chardet to detect the file encoding
    file_bytes = uploaded_file.read()
    result = chardet.detect(file_bytes)
    encoding = result['encoding']
    confidence = result['confidence']
    st.write(f"The encoding of {uploaded_file.name} is {encoding} with a confidence of {confidence}")
    # Try and pass straight to pandas dataframe without doing anything else first
    try:
        uploaded_file_df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith("csv") else pd.read_excel(uploaded_file)
        st.success("Success")
    except:
        st.warning(f"Pandas default pd.read_csv and pd.read_excel failed to read {uploaded_file.name}")
        try:
            if uploaded_file.name.endswith(("csv","txt")):
                uploaded_file_df = pd.read_csv(uploaded_file, encoding=encoding)
            else:
                uploaded_file_df = pd.read_excel(uploaded_file, encoding=encoding)
        except:
            uploaded_file_df = create_dataframe_codes(uploaded_file)
        return uploaded_file_df


def read_file_codecs_list(uploaded_file):
    file_extension = uploaded_file.name.split(".")[-1]
    delimiters = [',', '\t', ';', '|']
    codecs = ['utf-8', 'utf-16', 'utf-32', 'ascii','big5','big5hkscs','cp037','cp273','cp424','cp437','cp500','cp720','cp737','cp775','cp850','cp852','cp855',
            'cp856','cp857','cp858','cp860','cp861','cp862','cp863','cp864','cp865','cp866','cp869','cp874','cp875','cp932','cp949',
            'cp950','cp1006','cp1026','cp1125','cp1140','cp1250','cp1251','cp1252','cp1253','cp1254','cp1255','cp1256','cp1257','cp1258',
            'euc_jp','euc_jis_2004','euc_jisx0213','euc_kr','gb2312','gbk','gb18030','hz','iso2022_jp','iso2022_jp_1','iso2022_jp_2',
            'iso2022_jp_2004','iso2022_jp_3','iso2022_jp_ext','iso2022_kr','latin_1','iso8859_2','iso8859_3','iso8859_4','iso8859_5','iso8859_6',
            'iso8859_7','iso8859_8','iso8859_9','iso8859_10','iso8859_11','iso8859_13','iso8859_14','iso8859_15','iso8859_16','johab','koi8_r','koi8_t',
            'koi8_u','kz1048','mac_cyrillic','mac_greek','mac_iceland','mac_latin2','mac_roman','mac_turkish','ptcp154','shift_jis','shift_jis_2004',
            'shift_jisx0213','utf_32','utf_32_be','utf_32_le','utf_16','utf_16_be','utf_16_le','utf_7','utf_8','utf_8_sig']
    
    if file_extension in ["csv", "txt"]:
            for codec in codecs:
                for delimiter in delimiters:
                    try:
                        df = pd.read_csv(uploaded_file, delimiter=delimiter, encoding=codec)
                        return df
                    except Exception as e:
                        print(f"Failed to read {uploaded_file.name} using {codec} encoding. Error: {e}")
    elif file_extension in ["xls", "xlsx", "xlsm", "ods", "odt"]:
        for codec in codecs:
            for delimiter in delimiters:
                try:
                    df = pd.read_excel(uploaded_file, delimiter=delimiters, encoding=codec)
                    return df
                except Exception as e:
                    print(f"Failed to read {uploaded_file.name} using {codec} encoding. Error: {e}")
    else:
        raise ValueError(f"Invalid file type: {file_extension}. Please upload a file of type csv, txt, xls, xlsx, xlsm, ods, or odt.")
        return None


def uploaded_files_list():
    files_list = st.session_state.get("files_list", [])
    if len(files_list) > 0:
        for file in files_list:
            col1, col2 = st.columns(2)
            with col1:
                st.write(file.name)
            with col2:
                file_to_delete = file.name
                delete_file = st.button("Delete", key="delete_" + file_to_delete)
                if delete_file:
                    files_list = [file for file in files_list if file.name != file_to_delete]
                    st.session_state.files_list = files_list
    else:
        st.write("No files are uploaded")

#   categorise_files_form is a function that handles file categorization. It uses the st module to create a form 
#   with a select box for each file in the files_list. The user can select a category for 
#   each file, and when the form is submitted, the function calls the required_cols(file) 
#   function to get the required columns for each file's category and assigns it to the 
#   required_cols attribute of the File object. The function then displays a success message for each file.

def categorise_files_form():
    files_list = st.session_state.files_list
    with st.form("categorise_files_1"):
        for file in files_list:
            file.category = st.selectbox(f"Select file category for {file.name}", ["Collar", "Survey", "Point", "Interval"],key=file.name)
        submit_file_categories = st.form_submit_button("Submit")
        if submit_file_categories:
            st.write("Submitting files...")
            num_collars = sum(1 for file in files_list if file.category == "Collar")
            num_surveys = sum(1 for file in files_list if file.category == "Survey")
            if num_collars == 1 and num_surveys == 1:
                # Only one file with category "Collar" and one file with category "Survey"
                for file in st.session_state.get("files_list", []):
                    if file.category is not None:
                        file.required_cols = required_cols(file)
                        st.success(f'The file {file.name} has been categorised as a {file.category} file, and its required columns are {file.required_cols}')
                    else:
                        st.error(f"{file.name} has not been assigned a file category.")
            else:
                st.error(f'Either more than one file with category "Collar" or more than one file with category "Survey".')
            st.session_state.files_list = files_list


#   required_cols is a function that takes a File object as an input and returns a list of required 
#   columns for the file's category. Depending on the category, the function returns a 
#   list of required columns. If the category is not one of the four options (Collar, Survey, 
#   Point, Interval) it assigns "Not populated" and displays an error message.


def required_cols(file):
    if file.category == "Collar":
        required_cols = ["HoleID", "DH_X", "DH_Y", "DH_Z", "Depth"]
    elif file.category == "Survey":
        required_cols = ["HoleID", "Depth", "Dip", "Azimuth"]
    elif file.category == "Point":
        required_cols = ["HoleID", "Depth"]
    elif file.category == "Interval":
        required_cols = ["HoleID", "From", "To"]
    else:
        required_cols = ["Not populated"]
        st.write("No file category is assigned to " + file.name)
    df_required_cols = {col: None for col in required_cols}
    return df_required_cols

#   identify_columns_form is a function that allows the user to define data types of all the columns in 
#   for the pandas dataframes that were created for each file they uploaded. Each file has a separate st.form, 
#   all the select boxes for the data type choices are run when the "submit" button is clicked by the user. 
#   
#   The simplified datatypes that can be assigned by the user are: "Text", "Category", "Numeric", "Datetime", "Boolean".
#   The user must also identify the "required columns" depending on the file category that they chose earlier (ie Collar, Survey etc).
#   These required columns will be used later for data processing and analysis.
#   When the user submits the form, it runs the df_reassigned_dtypes function which creates a new pandas dataframe and 
#   assigns dtypes based on the users selections.

def identify_columns_form(file):
    simplified_dtypes_options = ["Text", "Category", "Numeric", "Datetime", "Boolean"]
    selected_options = []
    with st.expander(file.name):
        st.write(f"Select column data types for the " + file.category + " file: " + file.name)
        try:
            col1, col2 = st.columns(2)
        except ValueError as e:
            if "too many values to unpack" in str(e):
                st.error("Error: too many columns selected. Please select only two columns.")
            else:
                raise e
        with col1:
            # Show the dataframe preview for the selected file
            st.dataframe(file.df)
        with col2:
            # Create a form to select columns for the selected file based on file type
            with st.form(file.name):
                for i, column in enumerate(file.columns):
                    #get the default dtype of this column in this file
                    this_col_default = file.simplified_dtypes.get(column) if column in file.simplified_dtypes else None
                    this_col_default = str(this_col_default)
                    this_col_options = list(file.required_cols.keys()) + simplified_dtypes_options + ["Not imported"]
                    this_col_options = list(map(str, this_col_options))
                    #search for the item
                    if this_col_default is not None and this_col_default in this_col_options:
                        this_col_index = this_col_options.index(this_col_default)
                    else:
                        this_col_default = "Text"
                        this_col_index = this_col_options.index(this_col_default)
                    selected_datatype = st.selectbox(label=f"Select the data type for column '{column}' with {len(file.df[column].unique())} unique values:", options=this_col_options, index=this_col_index, key=file.name + "_" + column)
                    file.user_defined_dtypes[column] = selected_datatype
                # Submit the form and initiate view summary
                submit_column_identification = st.form_submit_button("Submit")
                if submit_column_identification:
                    file.df_reassigned_dtypes = change_dtypes(file.df, file.user_defined_dtypes)
                    st.success("Success")
                    st.success(f'The {file.category} file {file.name} has had its column datatypes processed as follows: {file.columns_dtypes}')



def view_summary():
    # display summary information for each file
    for file in files_list:
        st.write("File:", file.name)
        st.write("Category:", file.category)
        if file.category == "Collar":
            st.write("Number of drillholes:", len(file.df["HoleID"].unique()))
        else:
            st.write("Number of drillholes:", len(file.df["HoleID"].unique()))
            st.write("Number of drillholes with missing references:", len(collar_holes.difference(file.df["HoleID"].unique())))
            st.write("List of drillholes missing references:", list(collar_holes.difference(file.df["HoleID"].unique())))
            if file.category == "Survey":
                st.write("Number of drillholes missing collar references:", len(file.df["HoleID"].unique().difference(collar_holes)))
                st.write("List of drillholes missing collar reference:", list(file.df["HoleID"].unique().difference(collar_holes)))
                
                

def simplify_dtypes(df):
    dtypes = {}
    for col in df.columns:
        if pd.api.types.is_string_dtype(df[col]):
            dtypes[col] = "Text"
        elif pd.api.types.is_categorical_dtype(df[col]):
            dtypes[col] = "Category"
        elif pd.api.types.is_numeric_dtype(df[col]):
            dtypes[col] = "Numeric"
        elif pd.api.types.is_datetime64_dtype(df[col]):
            dtypes[col] = "Datetime"
        elif pd.api.types.is_bool_dtype(df[col]):
            dtypes[col] = "Boolean"
    return dtypes

#   In the change_dtypes function, df is the input dataframe, and column_types is the input dictionary with 
#   column names as keys and their desired datatype as values. The function first creates a copy 
#   of the input dataframe, then loops through the dictionary and checks if the column exists in 
#   the dataframe. If it does, it tries to convert the column to the specified datatype using pandas' 
#   built-in functions. If it fails to convert, it will try similar datatype or will set it to text. 
#   Then it returns the new dataframe with changed dtypes.

def change_dtypes(df, column_types):
    df_copy = df.copy()
    for column, col_type in column_types.items():
        if column not in df_copy.columns:
            print(f"{column} not found in the dataframe.")
            continue
        if col_type == "Text":
            df_copy[column] = df_copy[column].astype(str)
        elif col_type == "Category":
            df_copy[column] = df_copy[column].astype("category")
        elif col_type == "Numeric":
            try:
                df_copy[column] = df_copy[column].astype(float)
            except ValueError:
                try:
                    df_copy[column] = df_copy[column].astype(int)
                except ValueError:
                    df_copy[column] = df_copy[column].astype(str)
                    print(f"{column} could not be converted to numeric and was set to text type.")
        elif col_type in ["Datetime", "Boolean"]:
            try:
                if col_type == "Datetime":
                    df_copy[column] = pd.to_datetime(df_copy[column])
                else:
                    df_copy[column] = df_copy[column].astype(bool)
            except ValueError:
                df_copy[column] = df_copy[column].astype(str)
                print(f"{column} could not be converted to {col_type} and was set to text type.")
        elif col_type in ["DH_X", "DH_Y", "DH_Z", "Depth", "Dip", "Azimuth", "From", "To"]:
            try:
                df_copy[column] = df_copy[column].astype(float)
            except ValueError:
                df_copy[column] = df_copy[column].astype(str)
                print(f"{column} could not be converted to numeric and was set to text type.")
    return df_copy


def plot3d_dhtraces(df_dh_traces):
    try:
        fig = px.line_3d(df_dh_traces, x="DH_X", y="DH_Y", z="DH_RL", color="HOLEID")
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.error("Plot failing to load")


def generate_drilltraces():
    
    files_list = st.session_state.get("files_list", [])
    collar_file = [file for file in files_list if file.category == "Collar"]
    survey_file = [file for file in files_list if file.category == "Survey"]
    
    if len(collar_file) == 0 or len(survey_file) == 0:
        raise IndexError("One of the required files is missing")
    else:
        df_dh_traces = dh_calcs.calc_drilltraces(collar_file[0].df, 
                                                 survey_file[0].df, 
                                                 collar_file[0].required_cols, 
                                                 survey_file[0].required_cols, 
                                                 collar_file[0].user_defined_dtypes, 
                                                 survey_file[0].user_defined_dtypes
                                                )
        return df_dh_traces

#   upload_files is a function that handles streamlit file uploads. It uses the st module to create a file uploader widget, 
#   and allows the user to select multiple files of type csv and xlsx.
#   
#   When files are uploaded, it creates a pandas DataFrame for each file, and stores it in a File Class object for each file (along with other metadata).
#   The File objects are then stored in a global st.session_state list called "files_list".
#
#   The function also calls simplify_dtypes() and assigns the returned value as 
#   uploaded_file_simplified_dtypes which is used to create the File object.
#   
#   The function then appends the File objects to the files_list and displays a success message.

def upload_files():
    files_list = st.session_state.get("files_list", [])
    with st.form("upload_files"):
        uploaded_files = st.file_uploader("Upload your file", type=["csv", "txt", "xls", "xlsx", "xlsm", "ods", "odt"], accept_multiple_files=True, key="dh_file_uploader", help="Upload your drillhole collar, survey, point and interval files in csv or excel format")
        submit_uploaded_files = st.form_submit_button("Submit")
        if submit_uploaded_files:
            if len(uploaded_files) > 0:
                for uploaded_file in uploaded_files:
                    uploaded_file_df = None
                    try:
                        uploaded_file_df = pd.read_csv(uploaded_file, error_bad_lines=False) if uploaded_file.name.endswith("csv") else pd.read_excel(uploaded_file)
                        st.success("Success")
                    except Exception as e:
                        st.warning(f"Pandas failed to load {uploaded_file.name}")
                        try:
                            uploaded_file_df = read_file_chardet(uploaded_file)
                            st.success("Success")
                        except Exception as e:
                            st.warning(f"Chardet failed to correctly read encoding for {uploaded_file.name}")
                            try:
                                uploaded_file_df = read_file_codecs_list(uploaded_file)
                                st.success("Success")
                            except Exception as e:
                                st.warning(f"Pandas failed to read file using list of codecs {uploaded_file.name}")
                    finally:
                        if uploaded_file_df is None:
                            st.warning(f"{uploaded_file.name} was unable to be loaded.")
                        else:
                            files_list = st.session_state.get("files_list", [])
                            files_list.append(File(uploaded_file.name, uploaded_file_df, None, uploaded_file_df.columns, uploaded_file_df.dtypes, None, simplify_dtypes(uploaded_file_df)))
                            st.session_state.files_list = files_list



def main():
    
    container_log = st.empty()
    container_uploaded_files_list = st.empty()
    container_upload_files = st.empty()
    container_overwrite_file = st.empty()
    container_categorise_files = st.empty()
    container_identify_columns = st.empty()
    container_generate_drilltraces = st.empty()
    plot3d_drilltraces = st.empty()

    with container_log.container():
        st.write(st.session_state.log)
    
    with container_uploaded_files_list.container():
        uploaded_files_list()
    
    with container_upload_files.container():
        upload_files()
                
    with container_categorise_files.container():
        if len(st.session_state.get("files_list", [])) > 0:
            categorise_files_form()

    with container_identify_columns.container():
        if len(st.session_state.get("files_list", [])) > 0:
            for file in st.session_state.get("files_list", []):
                if file.category is not None:
                    identify_columns_form(file)
                
    with container_generate_drilltraces.container():
        st.write("Generating drilltrace coordinates using minimum curvature method...")
        button_generate_drilltraces = st.button("Generate Drilltraces", key="button_generate_drilltraces")
        if button_generate_drilltraces:
            df_drilltraces = generate_drilltraces()
            st.session_state.df_drilltraces = df_drilltraces
            st.dataframe(df_drilltraces)
            
    with plot3d_drilltraces.container():
        st.write("There's supposed to be a 3d plot here")
        plot3d_drilltraces = st.button("Plot 3D Drilltraces", key="plot3d_drilltraces")
        if plot3d_drilltraces:
            if st.session_state.get("df_drilltraces") is not None:
                df_dh_traces = st.session_state.get("df_drilltraces")
                plot3d_dhtraces(df_dh_traces)



if __name__ == '__main__':
    main()
