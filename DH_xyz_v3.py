import streamlit as st
import pandas as pd

# Initialize an empty dictionary
uploaded_files = {}
file = None
df = None
file_category = None
file_category_chosen = False


def main():
    upload_file()
    if df is not None:
        st.write(df)
        file_category = file_type_submit(df, file)
        selected_cols = column_identification(file_category)
        if selected_cols:
            identify_columns(selected_cols, df, file_category)

    
def upload_file():
    # Allow user to select file
    global df
    global file
    file = st.file_uploader("Select a file", type=["csv", "xlsx"])
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
        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file)
        else:
            st.error("Invalid file type. Please upload a file in .csv or .xlsx format")
            return
    
    
def file_type_submit(df, file):
    with st.form(key="form_file_type_submit"):
        #Prompt user to select category
        file_category = st.selectbox("Select a category for the file:", ["Collar", "Survey", "Point", "Interval"])
        # Submit form button
        submitted = st.form_submit_button("Submit")
        if submitted:
            if file_category in ["Collar", "Survey"]:
                if file_category+"_df" in uploaded_files:
                    st.warning("A file already exists for this category, it will be overwritten")
                uploaded_files[file_category+"_df"] = df
                uploaded_files[file_category+"_file"] = file
                uploaded_files[file_category+"_category"] = file_category
            else:
                uploaded_files[file.name] = file
                uploaded_files[file.name + "_df"] = df
                uploaded_files[file.name + "_category"] = file_category
            return file_category
   
def column_identification(file_category):
    selected_columns = []
    if file_category == "Collar":
        selected_columns = ["HoleID", "DH_X", "DH_Y", "DH_Z"]
    elif file_category == "Survey":
        selected_columns = ["HoleID", "Depth", "Dip", "Azimuth"]
    elif file_category == "Point":
        selected_columns = ["HoleID", "Depth"]
    elif file_category == "Interval":
        selected_columns = ["HoleID", "From", "To"]
    else:
        return None
    return selected_columns
        
def identify_columns(selected_columns, df, file_category):
    for column in selected_columns:
        selected_column = st.selectbox(f"Select the column for {column}", key=df.columns)
        uploaded_files[file_category+"_columns"][column] = selected_column
    if st.button("Submit"):
        st.success("Columns stored successfully")



if __name__ == "__main__":
    main()
