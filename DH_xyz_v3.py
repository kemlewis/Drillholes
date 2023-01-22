import streamlit as st
import pandas as pd

def display_dataframe(button_text):
    uploaded_file = st.file_uploader(button_text, type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.dataframe(data)

st.button("Upload Dataframe 1")
display_dataframe("Dataframe 1")
st.button("Upload Dataframe 2")
display_dataframe("Dataframe 2")
