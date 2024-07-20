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

# Create three main tabs
tab1, tab2, tab3 = st.tabs(["Data Input", "3D Visualization", "Log"])

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
    if "df_drilltraces" in st.session_state and not st.session_state["df_drilltraces"].empty:
        plot3d_dhtraces(st.session_state["df_drilltraces"])
    else:
        st.info("No drill traces data available. Please generate drill traces in the 'Data Input' tab first.")

with tab3:
    st.header("Application Log")
    # Create a container for the log entries
    log_container = st.container()
    
    # Display log entries in reverse chronological order
    for log_entry in reversed(st.session_state["log"]):
        log_container.write(f"{log_entry['timestamp']} - {log_entry['action']} (User: {log_entry['username']})")