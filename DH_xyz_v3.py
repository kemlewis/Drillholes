import streamlit as st
import pandas as pd

def main():
    st.set_page_config(page_title="Upload Data", page_icon=":guardsman:", layout="wide")
    st.title("Upload Data")

    collar_file = st.file_uploader("Upload collar data (csv or excel)", type=["csv", "xlsx"])
    if collar_file is not None:
        collar_df = pd.read_csv(collar_file)
        st.dataframe(collar_df)
    survey_file = st.file_uploader("Upload survey data (csv or excel)", type=["csv", "xlsx"])
    if survey_file is not None:
        survey_df = pd.read_csv(survey_file)
        st.dataframe(survey_df)
    point_file = st.file_uploader("Upload point data (csv or excel)", type=["csv", "xlsx"])
    if point_file is not None:
        point_df = pd.read_csv(point_file)
        st.dataframe(point_df)
    interval_file = st.file_uploader("Upload interval data (csv or excel)", type=["csv", "xlsx"])
    if interval_file is not None:
        interval_df = pd.read_csv(interval_file)
        st.dataframe(interval_df)

if __name__ == '__main__':
    main()
