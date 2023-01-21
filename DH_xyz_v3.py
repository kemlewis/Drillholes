import streamlit as st
import pandas as pd

ENCODINGS = ["utf-8", "latin1", "iso-8859-1", "ascii"]

def main():
    st.title("File Reader")
    df_collar = load_file("Select a collar file (csv or excel)", type=["csv", "xlsx"])
    df_survey = load_file("Select a survey file (csv or excel)", type=["csv", "xlsx"])
    if df_collar is not None:
        st.dataframe(df_collar)
    if df_survey is not None:
        st.dataframe(df_survey)

def load_file(label, type):
    file = st.file_uploader(label, type=type)
    if file is not None:
        data = read_file(file)
        if data is not None:
            st.success(f"{file.name} loaded successfully!")
            return data
        else:
            st.warning(f"An error occurred while loading the {file.name} file.")
            return None

def read_file(file):
    for encoding in ENCODINGS:
        try:
            if file.name.endswith(".csv"):
                data = pd.read_csv(file, encoding=encoding)
            elif file.name.endswith(".xlsx"):
                data = pd.read_excel(file, encoding=encoding)
            else:
                st.warning("File type not supported. Please upload a csv or excel file.")
                return None
            return data
        except Exception as e:
            if encoding == ENCODINGS[-1]:
                st.warning("An error occurred while reading the file. Please make sure the file is in the correct format or check the encoding.")
                encoding = st.selectbox("Select the file's encoding", ENCODINGS, key="unique_encoding_key")
                if st.button("Confirm"):
                    try:
                        if file.name.endswith(".csv"):
                            data = pd.read_csv(file, encoding=encoding)
                        elif file.name.endswith(".xlsx"):
                            data = pd.read_excel(file, encoding=encoding)
                        else:
                            st.warning("File type not supported. Please upload a csv or excel file.")
                            return None
                        return data
                    except Exception as e:
                        st.error("An error occurred while reading the file. Please make sure the file is in the correct format or check the encoding.")
                        return None
                else:
                    continue
            else:
                continue

def __init__(self):
    self.ENCODINGS = ["utf-8", "latin1", "iso-8859-1", "ascii"]
    self.df_collar = None
    self.df_survey = None

def main():
    self = __init__()
    st.title("File Reader")
    df_collar = load_file("Select a collar file (csv or excel)", type=["csv", "xlsx"])
    df_survey = load_file("Select a survey file (csv or excel)", type=["csv", "xlsx"])
    if df_collar is not None:
        self.df_collar = df_collar
        st.dataframe(df_collar)
    if df_survey is not None:
        self.df_survey = df_survey
        st.dataframe(df_survey)
