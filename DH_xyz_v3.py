import streamlit as st
import pandas as pd

st.title("Upload Data")

global df_collar
global df_survey

def handle_file_upload(file, key):
    if file is None:
        return None
    if file is not None:
        data = pd.read_csv(file)
        if key == 1:
            df_collar = data
            st.write(df_collar)
        elif key == 2:
            df_survey = data
            st.write(df_survey)

def handle_files(file_uploaders):
    files = {}
    dataframes = {}
    for label, file_uploader in file_uploaders.items():
        file = file_uploader
        if file:
            files[label] = file
            dataframes[label] = pd.read_csv(file)
    return files, dataframes

def main():
    file_uploaders = {'collar': st.file_uploader("Upload collar data (csv or excel)", type=["csv", "xlsx"], on_change=lambda file: handle_file_upload(file, 1)),
                      'survey': st.file_uploader("Upload survey data (csv or excel)", type=["csv", "xlsx"], on_change=lambda file: handle_file_upload(file, 2)),
                      'point': st.file_uploader("Upload point data (csv or excel)", type=["csv", "xlsx"], on_change=lambda file: handle_file_upload(file, 3)),
                      'interval': st.file_uploader("Upload interval data (csv or excel)", type=["csv", "xlsx"], on_change=lambda file: handle_file_upload(4, 4))}


if __name__ == '__main__':
    main()
