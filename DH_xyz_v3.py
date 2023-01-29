import streamlit as st
import pandas as pd
import traceback

class File:
    def __init__(self, name, df, category, columns=[], columns_datatype=[], required_columns=[], simplified_dtypes={}, df_reassigned_dtypes={}):
        self.name = name
        self.df = df
        self.category = category
        self.columns = columns
        self.columns_datatype = columns_datatype
        self.required_columns = required_columns
        self.simplified_dtypes = simplified_dtypes
        self.df_reassigned_dtypes = df_reassigned_dtypes

# Create a list to store the files class objects
files_list = []

#   categorise_files_form is a function that handles file categorization. It uses the st module to create a form 
#   with a select box for each file in the files_list. The user can select a category for 
#   each file, and when the form is submitted, the function calls the required_columns(file) 
#   function to get the required columns for each file's category and assigns it to the 
#   required_columns attribute of the File object. The function then displays a success message for each file.

def categorise_files_form():
    if len(files_list) == 0:
        st.warning("No files found")
    else:
        with st.form("categorise_files_1"):
            for i, file in enumerate(files_list):
                file.category = st.selectbox(f"Select file category for {file.name}", ["Collar", "Survey", "Point", "Interval"],key=file.name)
            submit_file_categories = st.form_submit_button("Submit")
            if submit_file_categories:
                st.write("Submitting files...")
                for file in files_list:
                    file.required_columns = required_columns(file)
                    st.success(f'The file {file.name} has been categorised as a {file.category} file, and its required columns are {file.required_columns}')

#   required_columns is a function that takes a File object as an input and returns a list of required 
#   columns for the file's category. Depending on the category, the function returns a 
#   list of required columns. If the category is not one of the four options (Collar, Survey, 
#   Point, Interval) it assigns "Not populated" and displays an error message.

def required_columns(file):
    if file.category == "Collar":
        required_columns = ["HoleID", "DH_X", "DH_Y", "DH_Z", "Depth"]
    elif file.category == "Survey":
        required_columns = ["HoleID", "Depth", "Dip", "Azimuth"]
    elif file.category == "Point":
        required_columns = ["HoleID", "Depth"]
    elif file.category == "Interval":
        required_columns = ["HoleID", "From", "To"]
    else:
        required_columns = ["Not populated"]
        st.write("No file category is assigned to " + file.name)
    return required_columns

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
                    this_col_options = file.required_columns + simplified_dtypes_options + ["Not imported"]
                    this_col_options = list(map(str, this_col_options))
                    #search for the item
                    this_col_index = this_col_options.index(this_col_default)
                    this_col_key = [file.name] + ["_"] + [column]
                    this_col_key = list(map(str, this_col_key))
                    file.columns_datatype[column] = st.selectbox(label=f"Select the data type for column '{column}' with {len(file.df[column].unique())} unique values:", options=this_col_options, index=this_col_index, key=this_col_key)
                # Submit the form and initiate view summary
                submit_column_identification = st.form_submit_button("Submit")
                if submit_column_identification:
                    file.df_reassigned_dtypes = change_dtypes(file.df, file.columns_datatype)
                    st.success("Success")
                    st.success(f'The {file.category} file {file.name} has had its column datatypes processed as follows: {file.columns_datatype}')

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


#   upload_files is a function that handles file uploads. It uses the st module to create a file uploader widget, 
#   and allows the user to select multiple files of type csv and xlsx.
#   
#   When files are uploaded, it creates a pandas DataFrame for each file and creates a File object for each file.
#   The function also calls the function simplify_dtypes() and assigns the returned value as 
#   uploaded_file_simplified_dtypes which is used to create the File object.
#   
#   The function then appends the File objects to the files_list and displays a success message.

def upload_files():
    uploaded_files = st.file_uploader("Choose files to upload", type=["csv", "xlsx"], accept_multiple_files=True, key="dh_file_uploader", help="Upload your drillhole collar, survey, point and interval files in csv or excel format")
    # Create a pandas dataframe for each file and create a File object
    for uploaded_file in uploaded_files:
        uploaded_file_df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith("csv") else pd.read_excel(uploaded_file)
        uploaded_file_simplified_dtypes = simplify_dtypes(uploaded_file_df)
        uploaded_file_obj = File(uploaded_file.name, uploaded_file_df, None, uploaded_file_df.columns, [], [], uploaded_file_simplified_dtypes)
        files_list.append(uploaded_file_obj)
        st.success(f"File {uploaded_file.name} was successfully uploaded.")


def main():
    st.set_page_config(page_title="My App", page_icon=":guardsman:", layout="wide")
    with st.expander("Upload Files", expanded=True):
        upload_files()
    try:
        if len(files_list) == 0:
            raise ValueError("No files have been uploaded.")
        with st.expander("Categorise Files"):
            categorise_files_form()
    except ValueError as e:
        st.error(e)
    try:
        if len(files_list) == 0:
            raise ValueError("No files have been uploaded.")
        else:
            for file in files_list:
                if file.category is None:
                    raise ValueError(f"File {file.name} has not been categorised.")
        with st.expander("Identify Columns"):
            for file in files_list:
                if file.category is not None:
                    identify_columns_form(file)
    except ValueError as e:
        st.error(e)


if __name__ == '__main__':
    main()
