import streamlit as st
import pandas as pd
from datetime import datetime
import logging

# Import functions from other modules
from file_handling import read_file_chardet, uploaded_files_list
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

# File upload
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

# Display uploaded files
uploaded_files_list()

# Categorize files
categorise_files_form()

# Identify columns for each file
for file in st.session_state.files_list:
    identify_columns_form(file)

# Generate drill traces
if st.button("Generate Drill Traces"):
    generate_drilltraces()
    if "df_drilltraces" in st.session_state and not st.session_state["df_drilltraces"].empty:
        plot3d_dhtraces(st.session_state["df_drilltraces"])

# Display log
if st.checkbox("Show Log"):
    st.write("Application Log:")
    for log_entry in st.session_state["log"]:
        st.write(f"{log_entry['timestamp']} - {log_entry['action']} (User: {log_entry['username']})")