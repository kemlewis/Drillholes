import streamlit as st
import pandas as pd

uploaded_file1 = st.file_uploader("Upload a CSV file 1", type=["csv"])
if uploaded_file1 is not None:
    try:
        data1 = pd.read_csv(uploaded_file1)
        if data1.empty:
            st.error("The file is empty or doesn't contain any data.")
        else:
            st.dataframe(data1)
    except pd.errors.EmptyDataError:
        st.error("The file is empty or doesn't contain any data.")

uploaded_file2 = st.file_uploader("Upload a CSV file 2", type=["csv"])
if uploaded_file2 is not None:
    try:
        data2 = pd.read_csv(uploaded_file2)
        if data2.empty:
            st.error("The file is empty or doesn't contain any data.")
        else:
            st.dataframe(data2)
    except pd.errors.EmptyDataError:
        st.error("The file is empty or doesn't contain any
