import streamlit as st
import pandas as pd
import logging
from utils import required_cols

logger = logging.getLogger(__name__)

def categorise_files_form():
    files_list = st.session_state.files_list
    with st.form("categorise_files_1"):
        for idx, file in enumerate(files_list):
            file.category = st.selectbox(f"Select file category for {file.name}", ["Collar", "Survey", "Point", "Interval"], key=f"{file.name}_{idx}")
        submit_file_categories = st.form_submit_button("Submit")
        if submit_file_categories:
            process_file_categories(files_list)

def process_file_categories(files_list):
    num_collars = sum(1 for file in files_list if file.category == "Collar")
    num_surveys = sum(1 for file in files_list if file.category == "Survey")
    if num_collars == 1 and num_surveys == 1:
        for file in files_list:
            if file.category is not None:
                file.required_cols = required_cols(file)
                st.success(f'The file {file.name} has been categorised as a {file.category} file, and its required columns are {file.required_cols}')
            else:
                st.error(f"{file.name} has not been assigned a file category.")
    else:
        st.error(f'Either more than one file with category "Collar" or more than one file with category "Survey".')
    st.session_state.files_list = files_list

def identify_columns_form(file):
    simplified_dtypes_options = ["Text", "Category", "Numeric", "Datetime", "Boolean"]
    with st.expander(file.name):
        st.write(f"Select column data types for the {file.category} file: {file.name}")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(file.df)
        with col2:
            with st.form(file.name):
                for i, column in enumerate(file.columns):
                    this_col_default = file.simplified_dtypes.get(column, "Text")
                    this_col_options = list(file.required_cols.keys()) + simplified_dtypes_options + ["Not imported"]
                    this_col_options = list(map(str, this_col_options))
                    
                    if this_col_default not in this_col_options:
                        this_col_default = "Text"
                    
                    selected_datatype = st.selectbox(
                        label=f"Select the data type for column '{column}' with {len(file.df[column].unique())} unique values:",
                        options=this_col_options,
                        index=this_col_options.index(this_col_default),
                        key=f"{file.name}_{column}_{i}"
                    )
                    file.user_defined_dtypes[column] = selected_datatype
                submit_column_identification = st.form_submit_button("Submit")
                if submit_column_identification:
                    file.df_reassigned_dtypes = change_dtypes(file.df, file.user_defined_dtypes)
                    st.success(f'The {file.category} file {file.name} has had its column datatypes processed')

def change_dtypes(df, column_types):
    df_copy = df.copy()
    for column, col_type in column_types.items():
        if column not in df_copy.columns:
            logger.warning(f"{column} not found in the dataframe.")
            continue
        try:
            if col_type == "Text":
                df_copy[column] = df_copy[column].astype(str)
            elif col_type == "Category":
                df_copy[column] = df_copy[column].astype("category")
            elif col_type == "Numeric":
                df_copy[column] = pd.to_numeric(df_copy[column], errors='coerce')
            elif col_type == "Datetime":
                df_copy[column] = pd.to_datetime(df_copy[column], errors='coerce')
            elif col_type == "Boolean":
                df_copy[column] = df_copy[column].astype(bool)
            elif col_type in ["HoleID", "DH_X", "DH_Y", "DH_Z", "Depth", "Dip", "Azimuth", "From", "To"]:
                if col_type == "HoleID":
                    df_copy[column] = df_copy[column].astype(str)
                else:
                    df_copy[column] = pd.to_numeric(df_copy[column], errors='coerce')
        except Exception as e:
            logger.error(f"Error converting {column} to {col_type}: {str(e)}")
            df_copy[column] = df_copy[column].astype(str)
    return df_copy

def map_columns(file):
    st.write(f"Map columns for {file.name}")
    mapped_columns = {}
    for required_col in file.required_cols:
        mapped_columns[required_col] = st.selectbox(
            f"Select column for {required_col}",
            options=[""] + file.columns,
            key=f"{file.name}_{required_col}_mapping"
        )
    
    if st.button("Apply Column Mapping"):
        file.df = file.df.rename(columns={v: k for k, v in mapped_columns.items() if v})
        st.success("Column mapping applied successfully")
        return file
    return None

def validate_data(file):
    st.write(f"Validating data for {file.name}")
    validation_results = {}
    
    for col in file.required_cols:
        if col not in file.df.columns:
            validation_results[col] = "Missing"
        elif file.df[col].isnull().any():
            validation_results[col] = "Contains null values"
        else:
            validation_results[col] = "Valid"
    
    for col, result in validation_results.items():
        st.write(f"{col}: {result}")
    
    if all(result == "Valid" for result in validation_results.values()):
        st.success("All required columns are valid")
    else:
        st.error("Some columns have issues. Please correct them before proceeding.")

def preprocess_data(file):
    st.write(f"Preprocessing data for {file.name}")
    
    # Remove any leading/trailing whitespace
    for col in file.df.columns:
        if file.df[col].dtype == 'object':
            file.df[col] = file.df[col].str.strip()
    
    # Handle missing values
    for col in file.required_cols:
        if file.df[col].isnull().any():
            if file.df[col].dtype in ['float64', 'int64']:
                fill_value = st.number_input(f"Enter fill value for missing data in {col}", value=0.0)
                file.df[col].fillna(fill_value, inplace=True)
            else:
                fill_value = st.text_input(f"Enter fill value for missing data in {col}", value="Unknown")
                file.df[col].fillna(fill_value, inplace=True)
    
    st.success("Data preprocessing completed")
    return file