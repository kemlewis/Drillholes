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

def main():
    collar_file = st.file_uploader("Upload collar data (csv or excel)", type=["csv", "xlsx"], key=1)
    survey_file = st.file_uploader("Upload survey data (csv or excel)", type=["csv", "xlsx"], key=2)
    point_file = st.file_uploader("Upload point data (csv or excel)", type=["csv", "xlsx"], key=3)
    interval_file = st.file_uploader("Upload interval data (csv or excel)", type=["csv", "xlsx"], key=4)

    df_collar = handle_file_upload(collar_file)
    df_survey = handle_file_upload(survey_file)
    df_point_file = handle_file_upload(point_file)
    df_interval_file = handle_file_upload(interval_file)

if __name__ == '__main__':
    main()
