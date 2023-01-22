import streamlit as st
import pandas as pd

# Initialize an empty dictionary
uploaded_files = {}

def main():
    # Allow user to select file
    file = st.file_uploader("Select a file", type=["csv", "xlsx"])
    if file is not None:
        # Read the file into a DataFrame
        df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)

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
                # Clear the file uploader
                st.file_uploader("Select a file", type=["csv", "xlsx"], clear_cache=True)
            else:
                uploaded_files[file.name] = file
                uploaded_files[file.name + "_df"] = df
                uploaded_files[file.name + "_category"] = file_category
                st.success("File stored successfully")
                # Clear the file uploader
                st.file_uploader("Select a file", type=["csv", "xlsx"], clear_cache=True)

if __name__ == "__main__":
    main()
