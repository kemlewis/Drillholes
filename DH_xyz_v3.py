import streamlit as st
import pandas as pd

st.title("Upload Data")

def handle_file_upload(file, key):
    if file is None:
        st.write("NONE")
        return
    data = pd.read_csv(file)
    st.dataframe(data)
    if key == 1:
        df_collar = data
    elif key == 2:
        df_survey = data
    elif key == 3:
        df_point = data
    elif key == 4:
        df_interval = data

def main():
    collar_file = st.file_uploader("Upload collar data (csv or excel)", type=["csv", "xlsx"], key=1, on_change=lambda file: handle_file_upload(file, 1))
    survey_file = st.file_uploader("Upload survey data (csv or excel)", type=["csv", "xlsx"], key=2, on_change=lambda file: handle_file_upload(file, 2))
    point_file = st.file_uploader("Upload point data (csv or excel)", type=["csv", "xlsx"], key=3, on_change=lambda file: handle_file_upload(file, 3))
    interval_file = st.file_uploader("Upload interval data (csv or excel)", type=["csv", "xlsx"], key=4, on_change=lambda file: handle_file_upload(file, 4))
    st.dataframe()

if __name__ == '__main__':
    main()
