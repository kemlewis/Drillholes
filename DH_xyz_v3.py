import streamlit as st
import pandas as pd

# Initialize an empty dictionary
uploaded_files = {}

# Initialize an empty dictionary
uploaded_files = {}

def main():
    # Allow user to select file
    file = st.file_uploader("Select a file", type=["csv", "xlsx"])
    if file is not None:
        # Read the file into a DataFrame
        df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
        if df.empty:
            st.error("The file is empty. Please upload a valid file.")
            return
        # Store the file and the dataframe in the dictionary
        uploaded_files[file.name] = {"file": file, "df": df}
        st.write(df)
        # Prompt user to select category
        file_category = st.selectbox("Select a category for the file:", ["Collar", "Survey", "Point", "Interval"])
        # Confirm and Cancel buttons
        if st.button("Confirm"):
            uploaded_files[file.name]["category"] = file_category
            st.success("File stored successfully")
        elif st.button("Cancel"):
            del uploaded_files[file.name]
            st.warning("File removed from the dictionary")
            st.file_uploader("Select a file", type=["csv", "xlsx"], clear_cache=True)

if __name__ == "__main__":
    main()
