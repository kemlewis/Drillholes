import streamlit as st
import pandas as pd

def display_dataframe(button_text):
    if st.button(button_text):
        uploaded_file = st.file_uploader(button_text, type=["csv"])
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)
            st.dataframe(data)

display_dataframe("Upload Dataframe 1")
display_dataframe("Upload Dataframe 2")
