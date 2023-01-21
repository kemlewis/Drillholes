import streamlit as st
import pandas as pd

st.title("Upload Data")
collar_file = st.file_uploader("Upload collar data (csv or excel)", type=["csv", "xlsx"], key=1, on_change=uploader_callback, key="collar_file")
survey_file = st.file_uploader("Upload survey data (csv or excel)", type=["csv", "xlsx"], key=2)
point_file = st.file_uploader("Upload point data (csv or excel)", type=["csv", "xlsx"], key=3)
interval_file = st.file_uploader("Upload interval data (csv or excel)", type=["csv", "xlsx"], key=4)

def uploader_callback():
    st.session_state['ctr'] += 1
    print('Uploaded file #%d' % st.session_state['ctr'])

def main():
   
    if collar_file is not None:
        collar_df = pd.read_csv(collar_file)
        diplay_collar_df = st.dataframe(collar_df)
    
    if survey_file is not None:
        survey_df = pd.read_csv(survey_file)
        diplay_survey_df = st.dataframe(survey_df)
    
    if point_file is not None:
        point_df = pd.read_csv(point_file)
        st.dataframe(point_df)
    
    if interval_file is not None:
        interval_df = pd.read_csv(interval_file)
        st.dataframe(interval_df)

if __name__ == '__main__':
    main()
