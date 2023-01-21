import streamlit as st
import pandas as pd

st.title("Upload Data")

def handle_file_upload(file):
    if file is None:
        return
    if 'collar_file' in file.filename:
        collar_df = pd.read_csv(file)
        st.dataframe(collar_df)
    elif 'survey_file' in file.filename:
        survey_df = pd.read_csv(file)
        st.dataframe(survey_df)
    elif 'point_file' in file.filename:
        point_df = pd.read_csv(file)
        st.dataframe(point_df)
    elif 'interval_file' in file.filename:
        interval_df = pd.read_csv(file)
        st.dataframe(interval_df)

def main():
    collar_file = st.file_uploader("Upload collar data (csv or excel)", type=["csv", "xlsx"], key=1, on_change=handle_file_upload)
    survey_file = st.file_uploader("Upload survey data (csv or excel)", type=["csv", "xlsx"], key=2, on_change=handle_file_upload)
    point_file = st.file_uploader("Upload point data (csv or excel)", type=["csv", "xlsx"], key=3, on_change=handle_file_upload)
    interval_file = st.file_uploader("Upload interval data (csv or excel)", type=["csv", "xlsx"], key=4, on_change=handle_file_upload)

if __name__ == '__main__':
    main()
