import streamlit as st
import pandas as pd
import traceback

class File:
    def __init__(self, name, df, category, columns=[], columns_datatype=[], required_columns=[], guessed_cols_dtypes={}):
        self.name = name
        self.df = df
        self.category = category
        self.columns = columns
        self.columns_datatype = columns_datatype
        self.required_columns = required_columns
        self.guessed_cols_dtypes = guessed_cols_dtypes


# Create a list to store the files
files_list = []

def main():
    st.set_page_config(page_title="My App", page_icon=":guardsman:", layout="wide")
    with st.expander("Upload Files"):
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
        uploaded_file_guessed_col_dtypes = guess_column_datatypes(uploaded_file_df)
        uploaded_file_obj = File(uploaded_file.name, uploaded_file_df, None, uploaded_file_df.columns, [], [], uploaded_file_guessed_col_dtypes)
        files_list.append(uploaded_file_obj)
        st.success(f"File {uploaded_file.name} was successfully uploaded.")

        
# Create a function to handle file categorization
def categorise_files_form():
    # Use a form to present the list of files and a dropdown menu for each file
    with st.form("categorise_files"):
        for file in files_list:
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
        required_columns = None
        st.write("No file category is assigned to " + file.name)


# Create a function to handle column identification
def identify_columns_form(file):
    
    dtypes = ["int64", "float64", "bool", "datetime64", "timedelta", "category"]
    selected_options = []
    with st.container():
        st.header(f"Select column data types for the " + file.category + " file: " + file.name)
        col1, col2, col3 = st.columns([2,1,1])
        with col1:
            # Show the dataframe preview for the selected file
            st.dataframe(file.df)
        with col2:
            # Create a form to select columns for the selected file based on file type
            with st.form(file.name):
                for column in file.columns:
                    option = st.selectbox(f"Select the datatype for column: {column}", ["Not imported"] + dtypes + file.required_columns)
                    if option in file.required_columns:
                        if option in selected_options:
                            st.warning(f"{option} has already been selected. Please select a different option.")
                        else:
                            selected_options.append(option)
                            file.columns_datatype[column] = option
                # Submit the form and initiate view summary
                submit_column_identification = st.form_submit_button("Submit", on_click=identify_columns_submit)


def identify_columns_submit():
    # Show a success message
    st.success("Column selections stored successfully for file: " + selected_file.name)

    
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


def guess_column_datatypes(df):
    guessed_dtypes = {}
    for col in df.columns:
        guessed_dtype = pd.api.types.infer_dtype(df[col])
        guessed_dtypes[col] = guessed_dtype
    return guessed_dtypes

                
if __name__ == '__main__':
    main()
