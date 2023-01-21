import streamlit as st
import pandas as pd

st.title("Upload Data")

def handle_file_upload(file, key):
    if file is None:
        st.write("NONE")
        return None
    data = pd.read_csv(file)
    st.dataframe(data)
    return data

def main():
    collar_file = st.file_uploader("Upload collar data (csv or excel)", type=["csv", "xlsx"], key=1, on_change=lambda file: handle_file_upload(file, 1))
    survey_file = st.file_uploader("Upload survey data (csv or excel)", type=["csv", "xlsx"], key=2, on_change=lambda file: handle_file_upload(file, 2))
    point_file = st.file_uploader("Upload point data (csv or excel)", type=["csv", "xlsx"], key=3, on_change=lambda file: handle_file_upload(file, 3))
    interval_file = st.file_uploader("Upload interval data (csv or excel)", type=["csv", "xlsx"], key=4, on_change=lambda file: handle_file_upload(file, 4))
    
    df_collar = collar_file
    df_survey = survey_file
    df_point_file = point_file
    df_interval_file = interval_file
    
    

if __name__ == '__main__':
    main()
