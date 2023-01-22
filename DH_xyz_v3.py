import streamlit as st
import pandas as pd

# Initialize an empty dictionary
uploaded_files = {}

def main():
    # Allow user to select file
    df = None
    file = st.file_uploader("Select a file", type=["csv", "xlsx"], clear_cache=False)
    if file is not None:
        # Read the file into a DataFrame
        if file.name.endswith(".csv"):
            encodings = ["utf-8", "latin1", "iso-8859-1", "ascii"]
            for e in encodings:
                try:
                    df = pd.read_csv(file, encoding=e)
                    break
                except:
                    continue
        else:
            df = pd.read_excel(file)

        #Prompt user to select category
        file_category = st.selectbox("Select a category for the file:", ["Collar", "Survey", "Point", "Interval"])
        st.write(df)
        # Confirm button
        if st.button("Confirm"):
            if file_category == "Collar" or file_category == "Survey":
                if file_category+"_df" in uploaded_files:
                    st.warning("A file already exists for this category, it will be overwritten")
                uploaded_files[file_category+"_df"] = df
                uploaded_files[file_category+"_file"] = file
                uploaded_files[file_category+"_category"] = file_category
                st.success("File stored successfully")
                st.write(uploaded_files)
            else:
                uploaded_files[file.name] = file
                uploaded_files[file.name + "_df"] = df
                uploaded_files[file.name + "_category"] = file_category
                st.success("File stored successfully")
                st.write(uploaded_files)

if __name__ == "__main__":
    main()
