import streamlit as st
import pandas as pd
import io

def get_dataframe_from_csv(file):
    return pd.read_csv(file)

def main():
    st.title("Upload multiple CSV files")

    uploaded_files = st.file_uploader("Choose a CSV file", type=["csv"], multiple=True)

    if uploaded_files:
        dataframe_dict = {}
        for file in uploaded_files:
            df = get_dataframe_from_csv(file)
            dataframe_dict[file.name] = df

        st.write(dataframe_dict)

if __name__ == "__main__":
    main()
