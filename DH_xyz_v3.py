import streamlit as st
import pandas as pd

def main():
    st.title("File Reader")

    file = st.file_uploader("Select a file", type=["csv", "xlsx"])

    if file is None:
        st.warning("Please upload a file.")
        return

    try:
        if file.endswith(".csv"):
            data = pd.read_csv(file)
        elif file.endswith(".xlsx"):
            data = pd.read_excel(file)
        else:
            st.warning("File type not supported. Please upload a csv or excel file.")
            return

        st.dataframe(data)

    except Exception as e:
        st.error("An error occurred while reading the file. Please make sure the file is in the correct format.")

if __name__ == "__main__":
    main()
