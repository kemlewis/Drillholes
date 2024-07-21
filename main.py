import streamlit as st
import pandas as pd
from datetime import datetime
import logging

# Import functions from other modules
from file_handling import read_file_chardet
from data_processing import categorise_files_form, identify_columns_form, process_file_categories, change_dtypes
from drill_traces import generate_drilltraces, plot3d_dhtraces
from utils import File, simplify_dtypes, required_cols
from config import APP_TITLE, APP_ICON, ALLOWED_EXTENSIONS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Streamlit page config
st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")

# Initialize session state
if 'files_list' not in st.session_state:
    st.session_state['files_list'] = []
if "log" not in st.session_state:
    st.session_state["log"] = []
if "df_drilltraces" not in st.session_state:
    st.session_state["df_drilltraces"] = pd.DataFrame()

# Log app start
if len(st.session_state["log"]) == 0:
    st.session_state["log"].append({"timestamp": datetime.now(), "action": "App started", "username": "user1"})

# Main app
st.title(APP_TITLE)

# Create four main tabs
tab1, tab2, tab3, tab4 = st.tabs(["Data Input", "Data Viewer", "3D Visualization", "Log"])

with tab1:
    # Create sub-tabs for different data types
    data_tabs = st.tabs(["Drillholes", "Points", "Lines", "Surfaces"])

    with data_tabs[0]:  # Drillholes tab
        # Create sub-tabs for drillhole data types
        dh_tabs = st.tabs(["DH Survey/Collar", "DH Points", "DH Intervals"])

        with dh_tabs[0]:  # DH Survey/Collar tab
            st.header("DH Survey/Collar Data Input")

            # File upload in an expander
            with st.expander("Upload Files", expanded=True):
                uploaded_files = st.file_uploader("Upload your files", type=ALLOWED_EXTENSIONS, accept_multiple_files=True)

                if uploaded_files:
                    for file in uploaded_files:
                        if file.name not in [f.name for f in st.session_state.files_list]:
                            st.session_state["log"].append({"timestamp": datetime.now(), "action": f"File {file.name} uploaded", "username": "user1"})
                            df = read_file_chardet(file)
                            if df is not None:
                                simplified_dtypes = simplify_dtypes(df)
                                file_instance = File(name=file.name, df=df, category=None, columns=df.columns.tolist(), columns_dtypes=df.dtypes.to_dict(), simplified_dtypes=simplified_dtypes)
                                st.session_state.files_list.append(file_instance)

            # Categorize files in an expander
            with st.expander("Categorize Files", expanded=True):
                categorise_files_form()

            # Guess and identify columns for each file after categorization
            for file in st.session_state.files_list:
                if file.category is not None:  # Ensure the file has been categorized
                    identify_columns_form(file)

            # Generate drill traces
            if st.button("Generate Drill Traces"):
                generate_drilltraces()
                if "df_drilltraces" in st.session_state and not st.session_state["df_drilltraces"].empty:
                    st.success("Drill traces generated successfully. Switch to the '3D Visualization' tab to view the plot.")

        with dh_tabs[1]:  # DH Points tab
            st.header("DH Points Data Input")
            st.info("DH Points data input functionality to be implemented.")

        with dh_tabs[2]:  # DH Intervals tab
            st.header("DH Intervals Data Input")
            st.info("DH Intervals data input functionality to be implemented.")

    with data_tabs[1]:  # Points tab
        st.header("Points Data Input")
        st.info("Points data input functionality to be implemented.")

    with data_tabs[2]:  # Lines tab
        st.header("Lines Data Input")
        st.info("Lines data input functionality to be implemented.")

    with data_tabs[3]:  # Surfaces tab
        st.header("Surfaces Data Input")
        st.info("Surfaces data input functionality to be implemented.")

with tab2:
    st.header("Data Viewer")
    
    # Create two columns
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Available Data")
        
        # Create a list of available dataframes
        data_list = []
        
        # Add uploaded files
        for file in st.session_state.files_list:
            data_list.append({
                "Type": file.category,
                "Name": file.name,
                "Source": "Uploaded"
            })
        
        # Add generated drill traces if available
        if not st.session_state["df_drilltraces"].empty:
            data_list.append({
                "Type": "Drill Traces",
                "Name": "Generated Drill Traces",
                "Source": "Generated"
            })
        
        # Create a DataFrame from the data list
        df_available_data = pd.DataFrame(data_list)
        
        # Column filter
        with st.expander("Column Filter"):
            columns = df_available_data.columns.tolist()
            selected_columns = st.multiselect("Select columns to display", columns, default=columns)
        
        # Display the table with selected columns
        st.dataframe(df_available_data[selected_columns])
        
        # Radio button for selecting the dataframe to view
        if not df_available_data.empty:
            selected_df = st.radio("Select data to view:", df_available_data['Name'].tolist())
        else:
            st.write("No data available")
            selected_df = None
    
    with col2:
        st.subheader("Data Preview")
        
        # Display the selected dataframe
        if selected_df is not None:
            if selected_df == "Generated Drill Traces":
                st.dataframe(st.session_state["df_drilltraces"])
            else:
                selected_file = next((file for file in st.session_state.files_list if file.name == selected_df), None)
                if selected_file:
                    st.dataframe(selected_file.df)
                else:
                    st.write("No data available for the selected option.")
        else:
            st.write("No data selected")