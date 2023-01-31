import streamlit as st
import pandas as pd
import chardet
import os
import drillhole_calcs as dh_calcs

st.set_page_config(page_title="My App", page_icon=":guardsman:", layout="wide")

# Initialize the session state list
if 'files_list' not in st.session_state:
    files_list = st.empty()
    files_list = st.session_state.get("files_list", [])

class File:
    def __init__(self, name, df, category, columns=[], columns_dtypes=[], required_cols=[], simplified_dtypes={}, user_defined_dtypes={}, df_reassigned_dtypes={}):
        self.name = name
        self.df = df
        self.category = category
        self.columns = columns
        self.columns_dtypes = columns_dtypes
        self.required_cols = required_cols
        self.simplified_dtypes = simplified_dtypes
        self.user_defined_dtypes = user_defined_dtypes
        self.df_reassigned_dtypes = df_reassigned_dtypes

#   upload_files is a function that handles file uploads. It uses the st module to create a file uploader widget, 
#   and allows the user to select multiple files of type csv and xlsx.
#   
#   When files are uploaded, it creates a pandas DataFrame for each file and creates a File object for each file.
#   The function also calls the function simplify_dtypes() and assigns the returned value as 
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
                    try:
                        uploaded_file_df = read_file_codecs_list(uploaded_file)
                        try:
                            uploaded_file_df = read_file_chardet(uploaded_file)
                            try:
                                uploaded_file_df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith("csv") else pd.read_excel(uploaded_file)
                                st.success("Success")
                            except Exception as e:
                                st.warning(f"Pandas default pd.read_csv and pd.read_excel failed to read {uploaded_file.name}")
                        except Exception as e:
                            st.warning(f"Pandas default pd.read_csv and pd.read_excel failed to read {uploaded_file.name}")
                    except Exception as e:
                        st.warning(f"Pandas default pd.read_csv and pd.read_excel failed to read {uploaded_file.name}")
                    if uploaded_file_df is None:
                        st.warning(f"{uploaded_file.name} was unable to be loaded.")
                    else:
                        if len(st.session_state.get("files_list", [])) > 0:
                            existing_file = next((file for file in st.session_state.get("files_list", []) if file.name == uploaded_file.name), None)
                            handle_existing_file(existing_file, uploaded_file, uploaded_file_df)
                            st.session_state.files_list = files_list
                        else:
                            files_list = st.session_state.get("files_list", [])
                            files_list.append(File(uploaded_file.name, uploaded_file_df, None, uploaded_file_df.columns, uploaded_file_df.dtypes, None, simplify_dtypes(uploaded_file_df)))
                            st.session_state.files_list = files_list

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
    codecs = ["utf-8", "utf-16", "utf-32", "ascii"]
    try:
        if file_extension in ["csv", "txt"]:
            for codec in codecs:
                try:
                    df = pd.read_csv(uploaded_file, encoding=codec)
                    return df
                except Exception as e:
                    print(f"Failed to read {uploaded_file.name} using {codec} encoding. Error: {e}")
        elif file_extension in ["xls", "xlsx", "xlsm", "ods", "odt"]:
            for codec in codecs:
                try:
                    df = pd.read_excel(uploaded_file, encoding=codec)
                    return df
                except Exception as e:
                    print(f"Failed to read {uploaded_file.name} using {codec} encoding. Error: {e}")
        else:
            raise ValueError(f"Invalid file type: {file_extension}. Please upload a file of type csv, txt, xls, xlsx, xlsm, ods, or odt.")
    except Exception as e:
        print(f"Failed to read {uploaded_file.name} by manually looping through codecs list. Error: {e}")
        return None

        
def handle_existing_file(existing_file, uploaded_file, uploaded_file_df):
    with container_overwrite_file:
        existing_files_popup = st.container()
        with existing_files_popup:
            if existing_file:
                st.write(f"A file with the name {uploaded_file.name} already exists. Do you want to overwrite it?")
                button_overwrite_confirm = st.button("Yes", key="overwrite_yes")
                button_overwrite_cancel = st.button("Cancel", key="overwrite_cancel")
                if overwrite_file:
                    files_list = st.session_state.get("files_list", [])
                    files_list.remove(existing_file)
                    files_list.append(File(uploaded_file.name, uploaded_file_df, None, uploaded_file_df.columns, uploaded_file_df.dtypes, None, simplify_dtypes(uploaded_file_df)))
                    st.session_state.files_list = files_list
                    st.success(f"File {uploaded_file.name} was successfully overwritten.")
                if button_overwrite_cancel:
                    files_list = st.session_state.get("files_list", [])
                    new_file_name = st.text_input(f"Please enter a new name for {uploaded_file.name}")
                    files_list.append(File(new_file_name, uploaded_file_df, None, uploaded_file_df.columns, uploaded_file_df.dtypes, None, simplify_dtypes(uploaded_file_df)))
                    st.session_state.files_list = files_list
                    st.success(f"File {uploaded_file.name} was successfully uploaded as {new_file_name}.")
            else:
                files_list = st.session_state.get("files_list", [])
                files_list.append(File(uploaded_file.name, uploaded_file_df, None, uploaded_file_df.columns, uploaded_file_df.dtypes, None, simplify_dtypes(uploaded_file_df)))
                st.session_state.files_list = files_list

#   categorise_files_form is a function that handles file categorization. It uses the st module to create a form 
#   with a select box for each file in the files_list. The user can select a category for 
#   each file, and when the form is submitted, the function calls the required_cols(file) 
#   function to get the required columns for each file's category and assigns it to the 
#   required_cols attribute of the File object. The function then displays a success message for each file.

def categorise_files_form():
    files_list = st.session_state.files_list
    with st.form("categorise_files_1"):
        for file in st.session_state.get("files_list", []):
            file.category = st.selectbox(f"Select file category for {file.name}", ["Collar", "Survey", "Point", "Interval"],key=file.name)
        submit_file_categories = st.form_submit_button("Submit")
        if submit_file_categories:
            st.write("Submitting files...")
            for file in st.session_state.get("files_list", []):
                if file.category is not None:
                    file.required_cols = required_cols(file)
                    st.success(f'The file {file.name} has been categorised as a {file.category} file, and its required columns are {file.required_cols}')
                else:
                    st.error(f"{file.name} has not been assigned a file category.")
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
    with st.container():
        st.header(f"Select column data types for the " + file.category + " file: " + file.name)
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
                    this_col_options = file.required_cols + simplified_dtypes_options + ["Not imported"]
                    #this_col_default = str(this_col_default)
                    this_col_options = list(d.df_required_cols()) + simplified_dtypes_options + ["Not imported"]
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

def button_cat_files():
    categorise_files_form()
    
def main_old():
    container_upload_files = st.container()
    container_categorise_files = st.container()
    container_identify_columns = st.container()
    container_generate_drilltraces = st.container()
    
    with container_upload_files:
        upload_files()
        for file in st.session_state.get("files_list", []):
            st.success(f"Successfully created pandas dataframe from {file.name}.")
            #st.write(vars(file))
    with st.container("Categorise Files"):
        button_cat_files = st.button("Load files for Categorisation", on_click=categorise_files_form)
#        try:
#            if len(st.session_state.get("files_list", [])) == 0:
#                raise ValueError("No files have been uploaded.")
#            else:
#                categorise_files_form()
#        except:
#            st.error(f"files_list is empty")
    with st.container("Identify Columns"):
        try:
            if len(st.session_state.get("files_list", [])) == 0:
                raise ValueError("No files have been uploaded.")
            else:
                for file in st.session_state.get("files_list", []):
                    if file.category is None:
                        raise ValueError(f"File {file.name} has not been categorised.")
                for file in st.session_state.get("files_list", []):
                    if file.category is not None:
                        identify_columns_form(file)
        except ValueError as e:
            st.error(e)
    with st.container("Calculate Drilltraces"):
        try:
            files_list = st.session_state.get("files_list", [])
            collar_file = [file for file in files_list if file.category == "Collar"]
            survey_file = [file for file in files_list if file.category == "Survey"]
            if len(collar_file) == 0 or len(survey_file) == 0:
                raise IndexError("One of the required files is missing")
            df_dh_traces = dh_calcs.calc_drilltraces(collar_file[0].df, survey_file[0].df, collar_file[0].required_cols, survey_file[0].required_cols)
            st.write(df_dh_traces)
        except IndexError as e:
            st.error(f"Error: {e}")
        except AttributeError as e:
            st.error(f"Error: {e}")
            
def main():
    
    container_log = st.container()
    container_upload_files = st.container()
    container_overwrite_file = st.container()
    container_categorise_files = st.container()
    container_identify_columns = st.container()
    container_generate_drilltraces = st.container()
    
    with container_upload_files:
        upload_files()
        for file in st.session_state.get("files_list", []):
            with container_log:
                st.success(f"Successfully created pandas dataframe from {file.name}.")

    with container_categorise_files:
        if len(st.session_state.get("files_list", [])) > 0:
            categorise_files_form()
            
if __name__ == '__main__':
    main()
