import streamlit as st
import pandas as pd

global df_collar
global df_survey

uploaded_file1 = st.file_uploader("Upload a CSV file 1", type=["csv"], key=1)
if uploaded_file1 is not None:
    df_collar = pd.read_csv(uploaded_file1)
    st.dataframe(df_collar)

uploaded_file2 = st.file_uploader("Upload a CSV file 2", type=["csv"], key=1)
if uploaded_file2 is not None:
    df_survey = pd.read_csv(uploaded_file2)
    st.dataframe(df_survey)
