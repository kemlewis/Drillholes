import streamlit as st
import pandas as pd

global df_collar
global df_survey

uploaded_file1 = st.file_uploader("Upload a CSV file 1", type=["csv"], key=1)
if uploaded_file1 is not None and key == 1:
    df_collar = pd.read_csv(uploaded_file1)
    st.write(df_collar)

uploaded_file2 = st.file_uploader("Upload a CSV file 2", type=["csv"], key=1)
if uploaded_file2 is not None and key == 2:
    df_survey = pd.read_csv(uploaded_file2)
    st.write(df_survey)
