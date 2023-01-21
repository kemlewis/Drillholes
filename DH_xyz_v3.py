import streamlit as st
import pandas as pd

ENCODINGS = ["utf-8", "latin1", "iso-8859-1", "ascii"]

def main():
    st.title("File Reader")

    collar_file = st.file_uploader("Select a collar file (csv or excel)", type=["csv", "xlsx"])
    survey_file = st.file_uploader("Select a survey file (csv or excel)", type=["csv", "xlsx"])

    if collar_file is None or survey_file is None:
        st.warning("Please upload both collar and survey files.")
        return

    df_collar = read_file(collar_file)
    df_survey = read_file(survey_file)

    if df_collar is None or df_survey is None:
        st.error("An error occurred while reading the files. Please make sure the files are in the correct format or check the encoding.")
        return
    st.dataframe(df_collar)
    st.dataframe(df_survey)

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
