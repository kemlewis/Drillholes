import streamlit as st
import pandas as pd

uploaded_file1 = st.file_uploader("Upload a CSV file 1", type=["csv"])
if uploaded_file1 is not None:
    data1 = pd.read_csv(uploaded_file1)
    st.dataframe(data1)

uploaded_file2 = st.file_uploader("Upload a CSV file 2", type=["csv"])
if uploaded_file2 is not None:
    data2 = pd.read_csv(uploaded_file2)
    st.dataframe(data2)

uploaded_file3 = st.file_uploader("Upload a CSV file 3", type=["csv"])
if uploaded_file3 is not None:
    data3 = pd.read_csv(uploaded_file3)
    st.dataframe(data3)
