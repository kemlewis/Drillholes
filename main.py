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
from datatype_guesser import REQUIRED_COLUMNS, COLUMN_DATATYPES

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Streamlit page config
st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")

# Initialize session state
if 'datasets' not in st.session_state:
    st.session_state.datasets = []
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
        st.header("Drillhole Data Input")

        # Add a new dataset
        if st.button("Add New Dataset"):
            st.session_state.datasets.append({"collar": None, "survey": None})

        # Display file uploaders for each dataset
        for idx, dataset in enumerate(st.session_state.datasets):
            with st.expander(f"Dataset {idx + 1}", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    dataset["collar"] = st.file_uploader(f"Upload Collar File for Dataset {idx + 1}", type=ALLOWED_EXTENSIONS, key=f"collar_uploader_{idx}")
                with col2:
                    dataset["survey"] = st.file_uploader(f"Upload Survey File for Dataset {idx + 1}", type=ALLOWED_EXTENSIONS, key=f"survey_uploader_{idx}")

        # Process uploaded files
        if st.button("Process Uploaded Files"):
            for idx, dataset in enumerate(st.session_state.datasets):
                if dataset["collar"] and dataset["survey"]:
                    dataset_name = f"Dataset_{idx+1}"
                    collar_file = process_uploaded_file(dataset["collar"], "Collar", dataset_name)
                    survey_file = process_uploaded_file(dataset["survey"], "Survey", dataset_name)
                    if collar_file and survey_file:
                        st.success(f"Dataset {idx + 1} processed successfully")
                    else:
                        st.error(f"Error processing Dataset {idx + 1}")
            st.experimental_rerun()

        # Guess and identify columns for each file after upload
        for file in st.session_state.files_list:
            if file.category in ["Collar", "Survey"]:
                with st.expander(f"Identify columns for {file.name} ({file.dataset})", expanded=True):
                    st.write(f"Select column data types for the {file.category} file: {file.name}")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.dataframe(file.df)
                    with col2:
                        auto_guess = st.button("Auto Guess", key=f"{file.name}_{file.dataset}_auto_guess")

                        if auto_guess:
                            assigned_mandatory_fields = set()
                            column_assignments = {}

                            for column in file.df.columns:
                                guessed_datatype = datatype_guesser.guess_type('datacolumn', f"{file.category}_{column}", file.df[column])
                                if guessed_datatype in file.required_cols and guessed_datatype not in assigned_mandatory_fields:
                                    column_assignments[column] = guessed_datatype
                                    assigned_mandatory_fields.add(guessed_datatype)
                                else:
                                    guessed_datatype = datatype_guesser.guess_column_type(file.category, column, file.df[column])
                                    column_assignments[column] = guessed_datatype

                            file.user_defined_dtypes.update(column_assignments)
                            st.success(f"Auto guessed data types for {file.name}")

                        st.write("Current column assignments:")
                        for column in file.df.columns:
                            current_dtype = file.user_defined_dtypes.get(column, "Text")
                            options = REQUIRED_COLUMNS.get(file.category, []) + COLUMN_DATATYPES
                            new_dtype = st.selectbox(
                                f"Column: {column}",
                                options=options,
                                index=options.index(current_dtype) if current_dtype in options else 0,
                                key=f"{file.name}_{file.dataset}_{column}_dtype"
                            )
                            file.user_defined_dtypes[column] = new_dtype

                        if st.button("Apply Column Types", key=f"{file.name}_{file.dataset}_apply_types"):
                            file.df = change_dtypes(file.df, file.user_defined_dtypes)
                            st.success(f"Applied column types for {file.name}")

        # Generate drill traces
        if st.button("Generate All Drill Traces"):
            all_drilltraces = []
            for idx, dataset in enumerate(st.session_state.datasets):
                collar_file = next((file for file in st.session_state.files_list if file.category == "Collar" and file.dataset == f"Dataset_{idx+1}"), None)
                survey_file = next((file for file in st.session_state.files_list if file.category == "Survey" and file.dataset == f"Dataset_{idx+1}"), None)
                if collar_file and survey_file:
                    drilltraces = generate_drilltraces(collar_file.df, survey_file.df)
                    if drilltraces is not None:
                        drilltraces['Dataset'] = f"Dataset_{idx+1}"
                        all_drilltraces.append(drilltraces)
            
            if all_drilltraces:
                st.session_state["df_drilltraces"] = pd.concat(all_drilltraces, ignore_index=True)
                st.success("All drill traces generated successfully. Switch to the '3D Visualization' tab to view the plot.")
            else:
                st.error("Failed to generate drill traces. Please check your input files.")

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
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Available Data")
        
        data_list = []
        
        for file in st.session_state.files_list:
            data_list.append({
                "Type": file.category,
                "Name": file.name,
                "Dataset": file.dataset,
                "Source": "Uploaded"
            })
        
        if not st.session_state["df_drilltraces"].empty:
            data_list.append({
                "Type": "Drill Traces",
                "Name": "Generated Drill Traces",
                "Dataset": "All",
                "Source": "Generated"
            })
        
        df_available_data = pd.DataFrame(data_list)
        
        with st.container():
            columns = df_available_data.columns.tolist()
            selected_columns = st.multiselect("Select columns to display", columns, default=columns)
        
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
                'dataset': df_available_data.iloc[selected_row]['Dataset'],
                'source': df_available_data.iloc[selected_row]['Source']
            }
        else:
            selected_df = None
    
    with col2:
        st.subheader("Data Preview")
        
        if selected_df is not None:
            if selected_df == "Generated Drill Traces":
                st.dataframe(st.session_state["df_drilltraces"])
            else:
                selected_file = next((file for file in st.session_state.files_list if file.name == selected_df), None)
                if selected_file:
                    st.dataframe(selected_file.df)
                else:
                    st.write("No data available for the selected option.")
            
            st.write(f"Selected Dataset: {st.session_state['selected_data']['name']}")
            st.write(f"Type: {st.session_state['selected_data']['type']}")
            st.write(f"Dataset: {st.session_state['selected_data']['dataset']}")
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
    log_container = st.container()
    
    with log_container:
        for log_entry in reversed(st.session_state["log"]):
            with st.expander(f"{log_entry['timestamp']} - {log_entry['action']} (User: {log_entry['username']})"):
                st.write(f"Filename: {log_entry.get('filename', 'N/A')}")
                st.write(f"Category: {log_entry.get('category', 'N/A')}")
                st.write(f"Dataset: {log_entry.get('dataset', 'N/A')}")
                st.write(f"Encoding: {log_entry.get('encoding', 'N/A')}")
                st.write(f"File size: {log_entry.get('file_size', 'N/A')}")
                st.write(f"Rows: {log_entry.get('rows', 'N/A')}")
                st.write(f"Columns: {log_entry.get('columns', 'N/A')}")
                if 'column_names' in log_entry:
                    st.write("Column names:")
                    st.write(", ".join(log_entry['column_names']))