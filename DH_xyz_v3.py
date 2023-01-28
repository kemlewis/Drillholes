import streamlit as st
import pandas as pd
import traceback

class File:
    def __init__(self, name, df, category, columns=[], columns_datatype=[], required_columns=[], simplified_dtypes={}):
        self.name = name
        self.df = df
        self.category = category
        self.columns = columns
        self.columns_datatype = columns_datatype
        self.required_columns = required_columns
        self.simplified_dtypes = simplified_dtypes


# Create a list to store the files
files_list = []

def main():
    st.set_page_config(page_title="My App", page_icon=":guardsman:", layout="wide")
    with st.expander("Upload Files", expanded=True):
        upload_files()
        st.write(files_list)
        for file in files_list:
            st.write(file.name)
            st.write(file.category)
            st.write(file.df)
    try:
        if len(files_list) == 0:
            raise ValueError("No files have been uploaded.")
        with st.expander("Categorise Files"):
            for file in files_list:
                categorise_files_form(file)
                st.write(file.name)
                st.write(file.category)
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


# Create a function to handle file uploads
def upload_files():
    uploaded_files = st.file_uploader("Choose files to upload", type=["csv", "xlsx"], accept_multiple_files=True, key="dh_file_uploader", help="Upload your drillhole collar, survey, point and interval files in csv or excel format")
    # Create a pandas dataframe for each file and create a File object
    for uploaded_file in uploaded_files:
        uploaded_file_df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith("csv") else pd.read_excel(uploaded_file)
        uploaded_file_simplified_dtypes = simplify_dtypes(uploaded_file_df)
        uploaded_file_obj = File(uploaded_file.name, uploaded_file_df, None, uploaded_file_df.columns, [], [], uploaded_file_simplified_dtypes)
        files_list.append(uploaded_file_obj)
        st.success(f"File {uploaded_file.name} was successfully uploaded.")
    

        
# Create a function to handle file categorization
def categorise_files_form(file):
    # Use a form to present the list of files and a dropdown menu for each file
    with st.form("categorise_files"):
        file.category = st.selectbox(f"Select file category for {file.name}", ["Collar", "Survey", "Point", "Interval"],key=file.name)
        # Submit the form and initiate identifying columns
        submit_file_categories = st.form_submit_button("Submit", on_click=categorise_files_submit)

def categorise_files_submit():
    for file in files_list:
        file.required_columns = required_columns(file)
    st.write("FORM WAS SUBMITTED")

    
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


# Create a function to handle column identification
# This didn't update
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
                for i, column in file.columns:
                    this_col_default = file.simplified_dtypes.get(column) if column in file.simplified_dtypes else None
                    this_col_default = str(this_col_default)
                    this_col_options = file.required_columns + simplified_dtypes_options + ["Not imported"]
                    this_col_options = list(map(str, this_col_options))
                    option = st.selectbox(label=f"Select the data type for column '{column}':", options=this_col_options, key=column)
                # Submit the form and initiate view summary
                submit_column_identification = st.form_submit_button("Submit", on_click=identify_columns_submit)


def identify_columns_submit():
    # Show a success message
    st.success("Success")

    
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

                
if __name__ == '__main__':
    main()
