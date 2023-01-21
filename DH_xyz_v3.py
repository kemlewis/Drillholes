import streamlit as st
import pandas as pd

st.title("Upload Data")

def handle_file_upload(file):
    if file is None:
        return None
    if file is not None:
        data = pd.read_csv(file)
        st.write(data)
        return data

def handle_files(file_uploaders):
    files = {}
    dataframes = {}
    for label, file_uploader in file_uploaders.items():
        file = file_uploader()
        if file:
            files[label] = file
            dataframes[label] = pd.read_csv(file)
    return files, dataframes

def main():
    file_uploaders = {'collar': st.file_uploader("Upload collar data (csv or excel)", type=["csv", "xlsx"]),
                      'survey': st.file_uploader("Upload survey data (csv or excel)", type=["csv", "xlsx"]),
                      'point': st.file_uploader("Upload point data (csv or excel)", type=["csv", "xlsx"]),
                      'interval': st.file_uploader("Upload interval data (csv or excel)", type=["csv", "xlsx"])}
    files, dataframes = handle_files(file_uploaders)


if __name__ == '__main__':
    main()
