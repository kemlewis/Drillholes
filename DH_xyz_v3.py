import streamlit as st
import pandas as pd

def upload_file():
    st.set_page_config(page_title="Upload File", page_icon=":file_folder:", layout="wide")
    st.title("Upload File")

    uploaded_file = st.file_uploader("Choose a CSV or Excel file to upload", type=["csv", "xls", "xlsx"])

    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)
            st.dataframe(data.head())
            st.success("File uploaded and displayed successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")

def main():
    st.sidebar.title("File Uploader")
    st.sidebar.selectbox("Select file type", ["CSV", "Excel"])

    if st.button("Upload File"):
        upload_file()

if __name__ == "__main__":
    main()
