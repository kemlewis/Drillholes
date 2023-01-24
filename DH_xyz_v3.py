import streamlit as st
import pandas as pd

# Initialize an empty dictionary
uploaded_files = {}
file = None
df = None
file_category_chosen = False


def main():
    upload_file()
    if df is not None:
        st.write(df)
        file_category = file_type_submit(df, file)
        if file_category:
            identify_columns(file_category, df)
            st.success("Columns stored successfully")


    
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
        else:
            df = pd.read_excel(file)
    
    
def file_type_submit(df, file):
    with st.form(key="form_file_type_submit"):
        #Prompt user to select category
        file_category = st.selectbox("Select a category for the file:", ["Collar", "Survey", "Point", "Interval"])
        # Submit form button
        submitted = st.form_submit_button("Submit")
        if submitted:
            if file_category == "Collar" or file_category == "Survey":
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
   

def identify_columns(file_category, df):
    with st.form(key="identify_columns"):
        selected_columns = []
        if file_category == "Collar":
            columns_to_identify = ["HoleID", "DH_X", "DH_Y", "DH_Z"]
        elif file_category == "Survey":
            columns_to_identify = ["HoleID", "Depth", "Dip", "Azimuth"]
        elif file_category == "Point":
            columns_to_identify = ["HoleID", "Depth"]
        elif file_category == "Interval":
            columns_to_identify = ["HoleID", "From", "To"]
        else:
            st.warning("Invalid file category")
            return
        for column in columns_to_identify:
            selected_columns.append(st.selectbox(f"Select the column for {column}", df.columns))
        # Submit form button
        submitted = st.form_submit_button("Submit")
        if submitted:
            uploaded_files[file_category+"_columns"] = selected_columns
            st.success("Columns stored successfully")





if __name__ == "__main__":
    main()

