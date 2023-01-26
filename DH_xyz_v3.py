import streamlit as st
import pandas as pd

def main():
    st.set_page_config(page_title="File Upload and Processing", page_icon=":clipboard:", layout="wide")
    st.title("File Upload and Processing")

    # Define the list of predefined file types
    file_types = ["File Type A", "File Type B", "File Type C"]

    # Allow the user to upload multiple files
    uploaded_files = st.file_uploader("Select files to upload", type=["csv", "xlsx"], accept_multiple_files=True)

    # Create a dictionary to store the information for each file
    file_data = {}

    # Process each uploaded file
    for file in uploaded_files:
        # Create a pandas dataframe from the file
        df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)

        # Categorize the file based on its type
        file_type = st.selectbox("Select the file type", file_types)

        # Identify specific columns in the file
        columns = st.multiselect("Select the columns to include", df.columns.tolist())

        # Store the information for the file in the dictionary
        file_data[file] = {"file_type": file_type, "columns": columns, "dataframe": df}

    # Display the information for each file
    for file, data in file_data.items():
        st.header(file)
        st.write("File Type: ", data["file_type"])
        st.write("Columns: ", data["columns"])
        st.write("Dataframe: ", data["dataframe"])

if __name__=="__main__":
    main()
