import pandas as pd
import streamlit as st
import os

def read_csv(file_type):
    """
    Read a CSV file and return a dataframe
    """
    # Allow user to upload the file
    file = st.file_uploader(f"Upload the {file_type} file (CSV, UTF-8 encoding)", type=["csv"])

    if file is None:
        st.error("No file was uploaded.")
        return None, None
    try:
        if os.path.getsize(file.name) == 0:
            st.error("The file is empty.")
            return None, None
    except FileNotFoundError:
        st.error("The file could not be found.")
        return None, None
    if not file.name.endswith('.csv'):
        st.error("The file is not a valid csv file.")
        return None, None

    # Create a dataframe from the file
    try:
        df = pd.read_csv(file)
    except Exception as e:
        st.error(f"An error occurred while reading the {file_type} file. Please check that it is a valid CSV file.")
        st.exception(e)
        return None, None
    else:
        return df, None

def select_columns(df, file_type):
    """
    Allow the user to select columns, perform data validation and return the dataframe with all columns and the dictionary containing the selected columns
    """
    col_dict = dict()
    if file_type == "collar":
        hole_id_col = st.selectbox("Select the column for 'hole_id'", df.columns)
        x_col = st.selectbox("Select the column for 'x'", df.columns)
        y_col = st.selectbox("Select the column for 'y'", df.columns)
        z_col = st.selectbox("Select the column for 'z'", df.columns)
        # Perform data validation
        if (df[x_col].dtype not in [float, int]) or (df[y_col].dtype not in [float, int]) or (df[z_col].dtype not in [float, int]):
            st.error("The 'x', 'y' and 'z' columns should contain either floats or ints which can be positive or negative")
            return None, None
        if st.button("Confirm"):
            col_dict["hole_id"] = hole_id_col
            col_dict["x"] = x_col
            col_dict["y"] = y_col
            col_dict["z"] = z_col
    elif file_type == "survey":
        hole_id_col = st.selectbox("Select the column for 'hole_id'", df.columns)
        depth_col = st.selectbox("Select the column for 'depth'", df.columns)
        dip_col = st.selectbox("Select the column for 'dip'", df.columns)
        azimuth_col = st.selectbox("Select the column for 'azimuth'", df.columns)
        # Perform data validation
        if not set(df[hole_id_col]).issubset(set(df_collar["hole_id"])):
            st.error("The 'hole_id' column must contain strings that are present in the 'df_collar' dataframe column with the header 'hole_id'")
            return None, None
        if (df[depth_col].dtype not in [float, int]) or (df[dip_col].dtype not in [float, int]) or (df[azimuth_col].dtype not in [float, int]):
            st.error("The 'depth', 'dip' and 'azimuth' columns should contain positive ints or floats.")
            return None, None
        if st.button("Confirm"):
            col_dict["hole_id"] = hole_id_col
            col_dict["depth"] = depth_col
            col_dict["dip"] = dip_col
            col_dict["azimuth"] = azimuth_col
    else:
        return None, None
    return df, col_dict


def main():
    df_collar, collar_cols = read_csv("collar")
    if df_collar is not None:
        df_collar, collar_cols = select_columns(df_collar, "collar")

    df_survey, survey_cols = read_csv("survey")
    if df_survey is not None:
        df_survey, survey_cols = select_columns(df_survey, "survey")

if __name__ == "__main__":
    main()
