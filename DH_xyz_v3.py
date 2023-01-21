import streamlit as st
import pandas as pd

st.title("Upload Data")

def handle_file_upload(file):
    if file.name == "collar_file":
        if collar_file is None:
            collar_df = pd.read_csv(collar_file)
            st.dataframe(collar_df)
    if file.name == "survey_file":
        if survey_file is None:
            survey_df = pd.read_csv(survey_file)
            st.dataframe(survey_df)
    if file.name == "point_file":
        if point_file is not None:
            point_df = pd.read_csv(point_file)
            st.dataframe(point_df)
    if file.name == "interval_file":
        if interval_file is not None:
            interval_df = pd.read_csv(interval_file)
            st.dataframe(interval_df)
        
    

#def main():
   

        

collar_file = st.file_uploader("Upload collar data (csv or excel)", type=["csv", "xlsx"], key=1, on_change=handle_file_upload)
survey_file = st.file_uploader("Upload survey data (csv or excel)", type=["csv", "xlsx"], key=2, on_change=handle_file_upload)
point_file = st.file_uploader("Upload point data (csv or excel)", type=["csv", "xlsx"], key=3, on_change=handle_file_upload)
interval_file = st.file_uploader("Upload interval data (csv or excel)", type=["csv", "xlsx"], key=4, on_change=handle_file_upload)


if __name__ == '__main__':
    main()
