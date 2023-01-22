import streamlit as st
import pandas as pd

# Initialize an empty dictionary
uploaded_files = {}

def main():
    # Allow user to select file
    file = st.file_uploader("Select a file", type=["csv", "xlsx"])
    if file is not None:
        # Add the uploaded file to the dictionary
        uploaded_files[file.name] = file

        # Read the file into a DataFrame
        df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)

        # Add the DataFrame to the dictionary
        uploaded_files[file.name + "_df"] = df
        st.write(df)
        #Prompt user to select category
        file_category = st.selectbox("Select a category for the file:", ["Collar", "Survey", "Point", "Interval"])
        uploaded_files[file.name + "_category"] = file_category

if __name__ == "__main__":
    main()
