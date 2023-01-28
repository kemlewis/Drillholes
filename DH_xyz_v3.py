import streamlit as st
import pandas as pd
import traceback

class File:
    def __init__(self, name, df, category, columns=[]):
        self.name = name
        self.df = df
        self.category = category
        self.columns = columns
        self.columns_datatype = columns_datatype
        self.required_columns = required_columns


# Create a list to store the files
files_list = []

def main():
    st.set_page_config(page_title="My App", page_icon=":guardsman:", layout="wide")
    with st.expander("Upload Files"):
        upload_files()
    with st.expander("Categorise Files"):
        categorise_files_form()
    with st.expander("Identify Columns"):
        identify_columns_form()

# Create a function to handle file uploads
def upload_files():
    uploaded_files = st.file_uploader("Choose files to upload", type=["csv", "xlsx"], accept_multiple_files=True, key="dh_file_uploader", help="Upload your drillhole collar, survey, point and interval files in csv or excel format")

    # Create a pandas dataframe for each file and create a File object
    for file in uploaded_files:
        file_df = pd.read_csv(file) if file.name.endswith("csv") else pd.read_excel(file)
        file_obj = File(file.name, file_df, None)
        files_list.append(file_obj)
        st.success(f"File {file.name} was successfully uploaded.")

        
# Create a function to handle file categorization
def categorise_files_form():
    # Use a form to present the list of files and a dropdown menu for each file
    with st.form("categorise_files"):
        for file in files_list:
            file.name = st.selectbox(f"Select file category for {file.name}", ["Collar", "Survey", "Point", "Interval"],key=file.name)
        # Submit the form and initiate identifying columns
        submit_file_categories = st.form_submit_button("Submit", on_click=categorise_files_submit)

def categorise_files_submit():
    for file in files_list:
        file.required_columns = required_columns(file)
    st.write("FORM WAS SUBMITTED")
    
def required_columns(file):
    if file_category == "Collar":
        required_columns = ["HoleID", "DH_X", "DH_Y", "DH_Z", "Depth"]
    elif file_category == "Survey":
        required_columns = ["HoleID", "Depth", "Dip", "Azimuth"]
    elif file_category == "Point":
        required_columns = ["HoleID", "Depth"]
    elif file_category == "Interval":
        required_columns = ["HoleID", "From", "To"]
    else:
        file_category == None
        st.write("No file category is assigned to " + file.name)
    
# Create a function to handle column identification
def identify_columns_form():
    # Create a form to select columns for the selected file based on file type
    for file in files_list:
        with st.form(file.name):
            with st.container(file.name):
                with st.column(1):
                    # Show the dataframe preview for the selected file
                    st.dataframe(file_select.df)
                with st.column(2):
                    for i in file.columns:
                        cols = st.columns(2)
                        cols[0].write(file.columns[i])
                        cols[1].write(st.selectbox())
            # Submit the form and initiate view summary
            submit_column_identification = st.form_submit_button("Submit", on_click=identify_columns_submit)


def identify_columns_submit():
    # Find the selected File object in the files_list
    selected_file = next((file for file in files_list if file.name == file_select), None)

    # Update the selected File object's columns attribute with the selected column_select value
    selected_file.columns = column_select

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


if __name__ == '__main__':
    main()
