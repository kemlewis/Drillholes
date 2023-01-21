import streamlit as st
import pandas as pd
import io

def get_dataframe_from_csv(file, encodings=["utf-8", "ISO-8859-1"]):
    for encoding in encodings:
        try:
            return pd.read_csv(file, encoding=encoding)
        except:
            pass
    raise ValueError("Could not read file with any of the specified encodings.")


def main():
    st.title("Upload multiple CSV files")

    uploaded_files = st.file_uploader("Choose a CSV file", type=["csv"], multiple=True)

    if uploaded_files:
        dataframe_dict = {}
        for file in uploaded_files:
            df = get_dataframe_from_csv(file, ["utf-8", "ISO-8859-1"])
            dataframe_dict[file.name] = df

        st.write(dataframe_dict)


if __name__ == "__main__":
    main()
