import streamlit as st
import pandas as pd

ENCODINGS = ["utf-8", "latin1", "iso-8859-1", "ascii"]

def main():
    st.title("File Reader")

    file = st.file_uploader("Select a csv or excel file", type=["csv", "xlsx"])

    if file is None:
        st.warning("Please upload a file.")
        return

    for encoding in ENCODINGS:
        try:
            if file.endswith(".csv"):
                data = pd.read_csv(file, encoding=encoding)
            elif file.endswith(".xlsx"):
                data = pd.read_excel(file, encoding=encoding)
            else:
                st.warning("File type not supported. Please upload a csv or excel file.")
                return

            st.dataframe(data)
            break
        except Exception as e:
            if encoding == ENCODINGS[-1]:
                st.warning("An error occurred while reading the file. Please make sure the file is in the correct format or check the encoding.")
                encoding = st.selectbox("Select the file's encoding", ENCODINGS)
                if st.button("Confirm"):
                    try:
                        if file.endswith(".csv"):
                            data = pd.read_csv(file, encoding=encoding)
                        elif file.endswith(".xlsx"):
                            data = pd.read_excel(file, encoding=encoding)
                        else:
                            st.warning("File type not supported. Please upload a csv or excel file.")
                            return

                        st.dataframe(data)
                    except Exception as e:
                        st.error("An error occurred while reading the file. Please make sure the file is in the correct format or check the encoding.")
            else:
                continue

if __name__ == "__main__":
    main()
