import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create global variables for dataframes and column dictionaries
df_collar = None
df_survey = None
dict_collar_cols = {}
dict_survey_cols = {}

# Create function to handle file uploads and data validation
def upload_and_validate(file_type):
    if file_type == 'collar':
        dataframe = 'df_collar'
        column_dict = 'dict_collar_cols'
        required_columns = ['HoleID', 'DH_X', 'DH_Y', 'DH_Z']
    elif file_type == 'survey':
        dataframe = 'df_survey'
        column_dict = 'dict_survey_cols'
        required_columns = ['HoleID', 'DEPTH', 'DIP', 'AZI']
    else:
        st.error('Invalid file type')
        return

    # Allow user to upload file
    file = st.file_uploader(f'Upload {file_type} file')

    # Try to load file as a pandas dataframe
    if file is not None:
        try:
            globals()[dataframe] = pd.read_csv(file)
        except:
            try:
                globals()[dataframe] = pd.read_excel(file)
            except:
                st.error('Failed to load file as a dataframe')
                return

    # Check that all required columns are present in the dataframe
    for column in required_columns:
        if column not in globals()[dataframe].columns:
            st.error(f'{column} column not found in {file_type} file')
            return

    # Prompt user to select column indexes for required columns
    for column in required_columns:
        globals()[column_dict][column] = st.selectbox(f'Select {column} column index:', globals()[dataframe].columns)

    check_for_blank_duplicate(globals()[dataframe])
    st.success(f'{file_type} file loaded and validated successfully')

def check_for_blank_duplicate(dataframe):
    dataframe.dropna(inplace=True)
    dataframe.drop_duplicates(inplace=True)

# Create function to calculate and plot drillhole traces
def calculate_and_plot():
    # Check that both dataframes have been loaded
    if df_collar is None or df_survey is None:
        st.error('Please upload both collar and survey files')
        return

    # Sort df_survey by HoleID and depth
    df_survey.sort_values(by=['HoleID', 'DEPTH'], inplace=True)

    # Perform calculations using minimum curvature method
    df_drilltraces = df_survey.copy()
    df_drilltraces['X'] = df_collar.loc[df_drilltraces['HoleID'].values, 'DH_X'].values + df_drilltraces['DEPTH'] * np.cos(df_drilltraces['DIP'])
    df_drilltraces['Y'] = df_collar.loc[df_drilltraces['HoleID'].values, 'DH_Y'].values + df_drilltraces['DEPTH'] * np.sin(df_drilltraces['DIP']) * np.cos(df_drilltraces['AZI'])
    df_drilltraces['Z'] = df_collar.loc[df_drilltraces['HoleID'].values, 'DH_Z'].values + df_drilltraces['DEPTH'] * np.sin(df_drilltraces['DIP']) * np.sin(df_drilltraces['AZI'])

    # Plot the drill traces using a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for hole_id in df_collar['HoleID'].unique():
        ax.plot(df_drilltraces.loc[df_drilltraces['HoleID'] == hole_id, 'X'],
                df_drilltraces.loc[df_drilltraces['HoleID'] == hole_id, 'Y'],
                df_drilltraces.loc[df_drilltraces['HoleID'] == hole_id, 'Z'])
    st.pyplot(fig)

    # Show basic information about the data
    st.write('Number of drillholes:', len(df_collar['HoleID'].unique()))
    st.write('Minimum depth:', df_drilltraces['DEPTH'].min())
    st.write('Maximum depth:', df_drilltraces['DEPTH'].max())

# Create main function to run app
def main():
    st.set_page_config(page_title='Drillhole Dataset App', page_icon=':guardsman:', layout='wide')
    st.title('Drillhole Dataset App')
    st.sidebar.title('Options')

    # Add buttons to upload and validate collar and survey files
    if st.sidebar.button('Upload collar file'):
        upload_and_validate('collar')
    if st.sidebar.button('Upload survey file'):
        upload_and_validate('survey')

    # Add button to calculate and plot drillhole traces
    if st.sidebar.button('Generate drillhole traces'):
        calculate_and_plot()

if __name__ == '__main__':
    main()

