import streamlit as st
import pandas as pd

ENCODINGS = ["utf-8", "latin1", "iso-8859-1", "ascii"]

def main():
    st.title("File Reader")

    collar_file = st.file_uploader("Select a collar file (csv or excel)", type=["csv", "xlsx"])
    if collar_file is not None:
        df_collar = read_file(collar_file)
        if df_collar is not None:
            st.success("Collar file loaded successfully!")
            st.dataframe(df_collar)
        else:
            st.warning("An error occurred while loading the collar file.")

    survey_file = st.file_uploader("Select a survey file (csv or excel)", type=["csv", "xlsx"])
    if survey_file is not None:
        df_survey = read_file(survey_file)
        if df_survey is not None:
            st.success("Survey file loaded successfully!")
            st.dataframe(df_survey)
        else:
            st.warning("An error occurred while loading the survey file.")

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
                encoding = st.selectbox("Select the file's encoding", ENCODINGS)
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


if __name__ == "__main__":
    main()
