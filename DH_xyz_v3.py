import streamlit as st
import pandas as pd

st.title("Upload Data")

def handle_file_upload(file, key):
    if file is None:
        st.write("NONE")
        return None
    data = pd.read_csv(file)
    
    return data

def main():
    collar_file = st.file_uploader("Upload collar data (csv or excel)", type=["csv", "xlsx"], key=1)
    survey_file = st.file_uploader("Upload survey data (csv or excel)", type=["csv", "xlsx"], key=2)
    point_file = st.file_uploader("Upload point data (csv or excel)", type=["csv", "xlsx"], key=3)
    interval_file = st.file_uploader("Upload interval data (csv or excel)", type=["csv", "xlsx"], key=4)

    df_collar = handle_file_upload(collar_file, 1)
    df_survey = handle_file_upload(survey_file, 2)
    df_point_file = handle_file_upload(point_file, 3)
    df_interval_file = handle_file_upload(interval_file, 4)

    if df_collar is not None:
        st.dataframe(df_collar)
    if df_survey is not None:
        st.dataframe(df_survey)
    if df_point_file is not None:
        st.dataframe(df_point_file)
    if df_interval_file is not None:
        st.dataframe(df_interval_file)


if __name__ == '__main__':
    main()
