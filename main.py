#main.py

import streamlit as st
import pandas as pd
from datetime import datetime
import logging

# Import functions from other modules
from file_handling import read_file_chardet, process_uploaded_file
from data_processing import identify_columns_form, process_file_categories, change_dtypes
from drill_traces import generate_drilltraces, plot3d_dhtraces
from utils import File, simplify_dtypes, required_cols
from config import APP_TITLE, APP_ICON, ALLOWED_EXTENSIONS
import datatype_guesser

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
            with st.expander("Upload Collar and Survey Files", expanded=True):
                collar_file = st.file_uploader("Upload Collar File", type=ALLOWED_EXTENSIONS, key="collar_uploader")
                survey_file = st.file_uploader("Upload Survey File", type=ALLOWED_EXTENSIONS, key="survey_uploader")

                if collar_file:
                    process_uploaded_file(collar_file, "Collar")

                if survey_file:
                    process_uploaded_file(survey_file, "Survey")

            # Guess and identify columns for each file after upload
            for file in st.session_state.files_list:
                if file.category in ["Collar", "Survey"]:
                    with st.expander(f"Identify columns for {file.name}", expanded=True):
                        st.write(f"Select column data types for the {file.category} file: {file.name}")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.dataframe(file.df)
                        with col2:
                            auto_guess = st.button("Auto Guess", key=f"{file.name}_auto_guess")

                            if auto_guess:
                                # Initialize a set to keep track of assigned mandatory fields
                                assigned_mandatory_fields = set()
                                column_assignments = {}

                                # First, assign best guesses for mandatory fields
                                for column in file.df.columns:
                                    guessed_datatype = datatype_guesser.guess_type('datacolumn', f"{file.category}_{column}", file.df[column])
                                    if guessed_datatype in file.required_cols and guessed_datatype not in assigned_mandatory_fields:
                                        column_assignments[column] = guessed_datatype
                                        assigned_mandatory_fields.add(guessed_datatype)
                                    else:
                                        # If not a required column, guess again without the file category prefix
                                        guessed_datatype = datatype_guesser.guess_column_type(file.category, column, file.df[column])
                                        column_assignments[column] = guessed_datatype

                                file.user_defined_dtypes.update(column_assignments)
                                st.success(f"Auto guessed data types for {file.name}")

                            st.write("Current column assignments:")
                            for column in file.df.columns:
                                current_dtype = file.user_defined_dtypes.get(column, "Text")
                                options = list(file.required_cols.keys()) + datatype_guesser.COLUMN_DATATYPES
                                new_dtype = st.selectbox(
                                    f"Column: {column}",
                                    options=options,
                                    index=options.index(current_dtype) if current_dtype in options else 0,
                                    key=f"{file.name}_{column}_dtype"
                                )
                                file.user_defined_dtypes[column] = new_dtype

                            if st.button("Apply Column Types", key=f"{file.name}_apply_types"):
                                file.df = change_dtypes(file.df, file.user_defined_dtypes)
                                st.success(f"Applied column types for {file.name}")

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

with tab3:
    st.header("3D Visualization")
    if "df_drilltraces" in st.session_state and not st.session_state["df_drilltraces"].empty:
        plot3d_dhtraces(st.session_state["df_drilltraces"])
    else:
        st.info("No drill traces data available. Please generate drill traces in the 'Data Input' tab first.")

with tab4:
    st.header("Application Log")
    # Create a container for the log entries
    log_container = st.container()
    
    # Display log entries in reverse chronological order
    for log_entry in reversed(st.session_state["log"]):
        log_container.write(f"{log_entry['timestamp']} - {log_entry['action']} (User: {log_entry['username']})")