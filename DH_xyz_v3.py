import pandas as pd
import streamlit as st

def read_csv(file_type):
    """
    Read a CSV file and return a dataframe
    """
    # Allow user to upload the file
    file = st.file_uploader(f"Upload the {file_type} file (CSV, UTF-8 encoding)", type=["csv"])

    # Create a dataframe from the file
    if file is not None:
        try:
            df = pd.read_csv(file)
        except Exception as e:
            st.error(f"An error occurred while reading the {file_type} file. Please check that it is a valid CSV file.")
            st.exception(e)
            return None
        else:
            return df
    else:
        return None

def select_columns(df, file_type):
    """
    Allow the user to select columns and return the dataframe with the selected columns
    """
    if file_type == "collar":
        hole_id_col = st.selectbox("Select the column for 'hole_id'", df.columns)
        x_col = st.selectbox("Select the column for 'x'", df.columns)
        y_col = st.selectbox("Select the column for 'y'", df.columns)
        z_col = st.selectbox("Select the column for 'z'", df.columns)
        # Remember the selected columns
        df = df[[hole_id_col, x_col, y_col, z_col]]
    elif file_type == "survey":
        hole_id_col = st.selectbox("Select the column for 'hole_id'", df.columns)
        depth_col = st.selectbox("Select the column for 'depth'", df.columns)
        dip_col = st.selectbox("Select the column for 'dip'", df.columns)
        azimuth_col = st.selectbox("Select the column for 'azimuth'", df.columns)
        # Remember the selected columns
        df = df[[hole_id_col, depth_col, dip_col, azimuth_col]]
    else:
        return None
    return df

def main():
    df_collar = read_csv("collar")
    if df_collar is not None:
        df_collar = select_columns(df_collar, "collar")

    df_survey = read_csv("survey")
    if df_survey is not None:
        df_survey = select_columns(df_survey, "survey")

if __name__ == "__main__":
    main()
