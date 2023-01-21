import streamlit as st
import pandas as pd

class FileReader:
    def __init__(self):
        self.ENCODINGS = ["utf-8", "latin1", "iso-8859-1", "ascii"]
        self.df_collar = None
        self.df_survey = None

    def main(self):
        st.title("File Reader")
        self.load_collar_file()
        self.load_survey_file()

    def load_collar_file(self):
        file = st.file_uploader("Select a collar file (csv or excel)", type=["csv", "xlsx"], key="collar")
        if file is not None:
            self.df_collar = self.read_file(file, key="collar")
            if self.df_collar is not None:
                st.success(f"{file.name} loaded successfully!")
                st.write(self.df_collar)

    def load_survey_file(self):
        file = st.file_uploader("Select a survey file (csv or excel)", type=["csv", "xlsx"], key="survey")
        if file is not None:
            self.df_survey = self.read_file(file, key="survey")
            if self.df_survey is not None:
                st.success(f"{file.name} loaded successfully!")
                st.write(self.df_survey)

    def read_file(self, file, key):
        for encoding in self.ENCODINGS:
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
                if encoding == self.ENCODINGS[-1]:
                    st.warning("An error occurred while reading the file. Please make sure the file is in the correct format or check the encoding.")
                    encoding = st.selectbox("Select the file's encoding", self.ENCODINGS, key="unique_encoding_key_"+key)
                    if st.button("Confirm", key="confirm_"+key):
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


if __name__ == "__main__":
    file_reader = FileReader()
    file_reader.main()
