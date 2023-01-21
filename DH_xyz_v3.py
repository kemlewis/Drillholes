import streamlit as st
import pandas as pd

def main():
    st.title("Upload Data")
    st.markdown("<h1 style='text-align:center;'>Upload Data <i class='fa fa-guardsman' aria-hidden='true'></i></h1>", unsafe_allow_html=True)
    st.markdown("<style>body{width:95%;}</style>", unsafe_allow_html=True)

    collar_file = st.file_uploader("Upload collar data (csv or excel)", type=["csv", "xlsx"], key=fu1)
    if collar_file is not None:
        collar_df = pd.read_csv(collar_file)
        diplay_collar_df = st.dataframe(collar_df, key=df1)
    survey_file = st.file_uploader("Upload survey data (csv or excel)", type=["csv", "xlsx"], key=fu2)
    if survey_file is not None:
        survey_df = pd.read_csv(survey_file)
        diplay_survey_df = st.dataframe(survey_df, key=df2)
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
