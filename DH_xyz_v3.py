import streamlit as st
import pandas as pd

st.title("Upload Data")

def handle_file_upload(file):
    if file = collar_file:
        if collar_file is None:
            collar_df = pd.read_csv(collar_file)
            diplay_collar_df = st.dataframe(collar_df)
    if file = survey_file:
        if survey_file is None:
            survey_df = pd.read_csv(survey_file)
            diplay_survey_df = st.dataframe(survey_df)
    if file = point_file:
        if point_file is not None:
            point_df = pd.read_csv(point_file)
            st.dataframe(point_df)
    if file = interval_file:
        if interval_file is not None:
            interval_df = pd.read_csv(interval_file)
            st.dataframe(interval_df)
        
    

#def main():
   

        

collar_file = st.file_uploader("Upload collar data (csv or excel)", type=["csv", "xlsx"], key=1, on_change=uploader_callback)
survey_file = st.file_uploader("Upload survey data (csv or excel)", type=["csv", "xlsx"], key=2, on_change=uploader_callback)
point_file = st.file_uploader("Upload point data (csv or excel)", type=["csv", "xlsx"], key=3, on_change=uploader_callback)
interval_file = st.file_uploader("Upload interval data (csv or excel)", type=["csv", "xlsx"], key=4, on_change=uploader_callback)


if __name__ == '__main__':
    main()
