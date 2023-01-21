import streamlit as st
import pandas as pd

class FileReader:
    def __init__(self):
        self.ENCODINGS = ["utf-8", "latin1", "iso-8859-1", "ascii"]
        self.df_files = []

    def main(self):
        st.title("File Reader")
        while True:
            file = st.file_uploader("Select a file (csv or excel)", type=["csv", "xlsx"])
            if file is not None:
                df_file = self.read_file(file)
                if df_file is not None:
                    st.success(f"{file.name} loaded successfully!")
                    st.write(df_file)
                    self.df_files.append(df_file)
            if not st.button("Add another file"):
                break

    def read_file(self, file):
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
                    st.error("An error occurred while reading the file. Please make sure the file is in the correct format or check the encoding.")
                    st.warning("You can try specifying the file's encoding manually.")
                    encoding = st.selectbox("Select the file's encoding", self.ENCODINGS)
                    if st.button("Confirm"):
                        try:
                            if file.name.endswith(".csv"):
                                data = pd.read_csv(file, encoding=encoding,error_bad_lines=False)
                            elif file.name.endswith(".xlsx"):
                                data = pd.read_excel(file, encoding=encoding)
                            else:
                                st.warning("File type not supported. Please upload a csv or excel file.")
                                return None
                            return data
                        except Exception as e:
                            st.error("An error occurred while reading the file with the specified encoding. Please make sure the file is in the correct format or try a different encoding.")

if __name__ == "__main__":
    file_reader = FileReader()
    file_reader.main()
