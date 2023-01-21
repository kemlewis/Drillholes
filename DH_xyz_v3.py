import streamlit as st
import pandas as pd

class FileReader:
    def __init__(self):
        self.ENCODINGS = ["utf-8", "latin1", "iso-8859-1", "ascii"]
        self.df_collar = None
        self.df_survey = None

    def main(self):
        st.title("File Reader")
        self.df_collar = self.load_file("Select a collar file (csv or excel)", type=["csv", "xlsx"], key="collar")
        self.df_survey = self.load_file("Select a survey file (csv or excel)", type=["csv", "xlsx"], key="survey")

    def load_file(self, label, type, key):
        file = st.file_uploader(label, type=type)
        if file is not None:
            data = self.read_file(file, key)
            if data is not None:
                st.success(f"{file.name} loaded successfully!")
                st.dataframe(data, key=key)
                return data
            else:
                st.warning(f"An error occurred while loading the {file.name} file.")
                return None

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
                    encoding = st.selectbox("Select the file's encoding", self.ENCODINGS, key=f"{key}_encoding_key")
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
    file_reader = FileReader()
    file_reader.main()
