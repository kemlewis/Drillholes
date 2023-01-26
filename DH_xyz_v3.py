import streamlit as st
import pandas as pd

# Create a dictionary to store uploaded files and their information
files_dict = {}

def main():
    
    st.set_page_config(page_title="My App", page_icon=":guardsman:", layout="wide")

    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select a page", ["Upload Files", "Categorise Files", "Identify Columns", "View Summary"])
    if page == "Upload Files":
        upload_files()
    elif page == "Categorise Files":
        categorise_files()
    elif page == "Identify Columns":
        identify_columns()
    elif page == "View Summary":
        view_summary()

# Create a function to handle file uploads
def upload_files():
    
    uploaded_files = st.file_uploader("Choose files to upload", type=["csv", "xlsx"], accept_multiple_files=True, key="dh_file_uploader", help="Upload your drillhole collar, survey, point and interval files in csv or excel format")

    # Create a pandas dataframe for each file
    for file in uploaded_files:
        file_df = pd.read_csv(file) if file.name.endswith("csv") else pd.read_excel(file)
        files_dict[file.name] = {"dataframe": file_df}
        st.success(f"File {file.name} was successfully uploaded.")

    # Add a "Next" button to navigate to the next page
    if st.button("Next"):
        st.write("Navigating to Categorise Files")
        categorise_files()

# Create a function to handle file categorization
def categorise_files():
    with st.form("categoirse_files"):
        # Use a form to present the list of files and a dropdown menu for each file
        for file_name, file_info in files_dict.items():
            file_type = st.selectbox(f"Select file type for {file_name}", ["Collar", "Survey", "Point", "Interval"])
            file_info["type"] = file_type
            
        # Perform validation of the selections
        collar_files = [file_info for file_name, file_info in files_dict.items() if file_info["type"] == "Collar"]
        survey_files = [file_info for file_name, file_info in files_dict.items() if file_info["type"] == "Survey"]
        point_files = [file_info for file_name, file_info in files_dict.items() if file_info["type"] == "Point"]
        interval_files = [file_info for file_name, file_info in files_dict.items() if file_info["type"] == "Interval"]

        # Submit the form and initiate identifying columns
        submitted = st.form_submit_button("submit_categoirse_files")
        if submitted:
            if len(collar_files) != 1 or len(survey_files) != 1:
                st.error("There must be exactly one Collar file and exactly one Survey file.")
                st.write("Navigating to Categorise Files", disabled=True)
            else:
                st.success("File categories were stored correctly.")
                if st.button("Next"):
                    st.write("Navigating to Categorise Files", disabled=False)
                    identify_columns()


# Create a function to handle column identification
def identify_columns():
    with st.form("identify_columns"):
        # Create a dropdown menu to select a file to identify columns for
        file_select = st.selectbox("Select a file to identify columns for:", files_by_category["Collar"] + files_by_category["Survey"] + files_by_category["Point"] + files_by_category["Interval"])

        # Show the dataframe preview for the selected file
        selected_file = file_dict[file_select]
        st.dataframe(selected_file)

        # Create a form to select columns for the selected file based on file type
        if file_select in files_by_category["Collar"]:
            column_select = st.multiselect("Select the necessary columns for Collar file:", ["HoleID", "DH_X", "DH_Y", "DH_Z", "Depth"])
        elif file_select in files_by_category["Survey"]:
            column_select = st.multiselect("Select the necessary columns for Survey file:", ["HoleID", "Depth", "Dip", "Azimuth"])
        elif file_select in files_by_category["Point"]:
            column_select = st.multiselect("Select the necessary columns for Point file:", ["HoleID", "Depth"])
        elif file_select in files_by_category["Interval"]:
            column_select = st.multiselect("Select the necessary columns for Interval file:", ["HoleID", "From", "To"])
        else:
            st.warning("Invalid file type")
            return

        #Submit the form
        if st.button("Submit"):
            # Store the column selections in the dictionary reference for the selected file
            file_dict[file_select]["columns"] = column_select
            # Show a success message
            st.success("Column selections stored successfully for file: " + file_select)

            
def view_summary():

    # display summary information for each file
    for file in files:
        st.write("File:", file["name"])
        st.write("Category:", file["category"])
        if file["category"] == "Collar":
            st.write("Number of drillholes:", len(file["df"]["HoleID"].unique()))
        else:
            st.write("Number of drillholes:", len(file["df"]["HoleID"].unique()))
            st.write("Number of drillholes with missing references:", len(collar_holes.difference(file["df"]["HoleID"].unique())))
            st.write("List of drillholes missing references:", list(collar_holes.difference(file["df"]["HoleID"].unique())))
            if file["category"] == "Survey":
                st.write("Number of drillholes missing collar references:", len(file["df"]["HoleID"].unique().difference(collar_holes)))
                st.write("List of drillholes missing collar reference:", list(file["df"]["HoleID"].unique().difference(collar_holes)))


if __name__ == '__main__':
    main()
