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

            col1, col2 = st.columns(2)

            with col1:
                # Collar file upload
                with st.expander("Upload Collar File", expanded=True):
                    collar_file = st.file_uploader("Upload Collar File", type=ALLOWED_EXTENSIONS, key="collar_uploader")
                    if collar_file:
                        if collar_file.name not in [f.name for f in st.session_state.files_list]:
                            st.session_state["log"].append({"timestamp": datetime.now(), "action": f"Collar file {collar_file.name} uploaded", "username": "user1"})
                            df = read_file_chardet(collar_file)
                            if df is not None:
                                simplified_dtypes = simplify_dtypes(df)
                                file_instance = File(name=collar_file.name, df=df, category="Collar", columns=df.columns.tolist(), columns_dtypes=df.dtypes.to_dict(), simplified_dtypes=simplified_dtypes)
                                # Remove any existing Collar file
                                st.session_state.files_list = [f for f in st.session_state.files_list if f.category != "Collar"]
                                st.session_state.files_list.append(file_instance)
                                st.success(f"Collar file {collar_file.name} uploaded successfully.")
                            else:
                                st.error(f"Failed to read {collar_file.name}.")
                        else:
                            st.warning(f"File {collar_file.name} already uploaded.")

            with col2:
                # Survey file upload
                with st.expander("Upload Survey File", expanded=True):
                    survey_file = st.file_uploader("Upload Survey File", type=ALLOWED_EXTENSIONS, key="survey_uploader")
                    if survey_file:
                        if survey_file.name not in [f.name for f in st.session_state.files_list]:
                            st.session_state["log"].append({"timestamp": datetime.now(), "action": f"Survey file {survey_file.name} uploaded", "username": "user1"})
                            df = read_file_chardet(survey_file)
                            if df is not None:
                                simplified_dtypes = simplify_dtypes(df)
                                file_instance = File(name=survey_file.name, df=df, category="Survey", columns=df.columns.tolist(), columns_dtypes=df.dtypes.to_dict(), simplified_dtypes=simplified_dtypes)
                                # Remove any existing Survey file
                                st.session_state.files_list = [f for f in st.session_state.files_list if f.category != "Survey"]
                                st.session_state.files_list.append(file_instance)
                                st.success(f"Survey file {survey_file.name} uploaded successfully.")
                            else:
                                st.error(f"Failed to read {survey_file.name}.")
                        else:
                            st.warning(f"File {survey_file.name} already uploaded.")

            # Display currently uploaded files
            st.subheader("Uploaded Files")
            for file in st.session_state.files_list:
                if file.category in ["Collar", "Survey"]:
                    st.write(f"{file.category}: {file.name}")

            # Guess and identify columns for each file after upload
            for file in st.session_state.files_list:
                if file.category in ["Collar", "Survey"]:
                    identify_columns_form(file)

            # Generate drill traces
            if st.button("Generate Drill Traces"):
                generate_drilltraces()
                if "df_drilltraces" in st.session_state and not st.session_state["df_drilltraces"].empty:
                    st.success("Drill traces generated successfully. Switch to the '3D Visualization' tab to view the plot.")

with tab2:
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
        with st.container():
            columns = df_available_data.columns.tolist()
            selected_columns = st.multiselect("Select columns to display", columns, default=columns)
        
        # Display the table with checkboxes and handle selection
        event = st.dataframe(
            df_available_data[selected_columns],
            hide_index=True,
            use_container_width=True,
            on_select='rerun',
            selection_mode='single-row'
        )

        if len(event.selection['rows']):
            selected_row = event.selection['rows'][0]
            selected_df = df_available_data.iloc[selected_row]['Name']
            st.session_state['selected_data'] = {
                'name': selected_df,
                'type': df_available_data.iloc[selected_row]['Type'],
                'source': df_available_data.iloc[selected_row]['Source']
            }
        else:
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
            
            # Display additional information about the selected dataset
            st.write(f"Selected Dataset: {st.session_state['selected_data']['name']}")
            st.write(f"Type: {st.session_state['selected_data']['type']}")
            st.write(f"Source: {st.session_state['selected_data']['source']}")
        else:
            st.write("No data selected")

# 3D Visualization tab
with tab3:
    st.header("3D Visualization")
    if "df_drilltraces" in st.session_state and not st.session_state["df_drilltraces"].empty:
        plot3d_dhtraces(st.session_state["df_drilltraces"])
    else:
        st.info("No drill traces data available. Please generate drill traces in the 'Data Input' tab first.")

# Log tab
with tab4:
    st.header("Application Log")
    # Create a container for the log entries
    log_container = st.container()
    
    # Display log entries in reverse chronological order
    for log_entry in reversed(st.session_state["log"]):
        log_container.write(f"{log_entry['timestamp']} - {log_entry['action']} (User: {log_entry['username']})")