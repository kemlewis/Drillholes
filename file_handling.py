#file_handling.py

import streamlit as st
import pandas as pd
import io
import chardet
import hashlib
import logging
from datetime import datetime
from utils import File, simplify_dtypes
from datatype_guesser import REQUIRED_COLUMNS

logger = logging.getLogger(__name__)

def get_file_hash(file_content):
    return hashlib.md5(file_content).hexdigest()

def read_file_chardet(uploaded_file):
    try:
        file_content = uploaded_file.read()
        file_size = len(file_content)
        file_hash = get_file_hash(file_content)
        
        if uploaded_file.name.endswith(('xlsx', 'xls', 'xlsm')):
            df = pd.read_excel(io.BytesIO(file_content))
            encoding = "Excel (binary)"
        else:
            result = chardet.detect(file_content)
            encoding = result['encoding']
            text_content = file_content.decode(encoding)
            df = pd.read_csv(io.StringIO(text_content))
        
        return df, encoding, file_size, file_hash
    except Exception as e:
        logger.error(f"File reading error: {str(e)}", exc_info=True)
        return None, None, None, None

def process_uploaded_file(file, category, dataset):
    df, encoding, file_size, file_hash = read_file_chardet(file)
    if df is not None:
        simplified_dtypes = simplify_dtypes(df)
        file_instance = File(
            name=file.name,
            df=df,
            category=category,
            columns=df.columns.tolist(),
            columns_dtypes=df.dtypes.to_dict(),
            simplified_dtypes=simplified_dtypes,
            dataset=dataset
        )
        file_instance.required_cols = REQUIRED_COLUMNS[category]
        
        # Remove any existing file of the same category and dataset
        st.session_state.files_list = [f for f in st.session_state.files_list if not (f.category == category and f.dataset == dataset)]
        st.session_state.files_list.append(file_instance)
        
        log_entry = {
            "timestamp": datetime.now(),
            "action": f"{category} file uploaded for {dataset}",
            "username": "user1",
            "filename": file.name,
            "category": category,
            "dataset": dataset,
            "encoding": encoding,
            "file_size": f"{file_size / 1024:.2f} KB",
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "file_hash": file_hash
        }
        st.session_state["log"].append(log_entry)
        
        return file_instance
    else:
        st.error(f"Failed to read {file.name}.")
        return None

def uploaded_files_list():
    files_list = st.session_state.get("files_list", [])
    if len(files_list) > 0:
        for idx, file in enumerate(files_list):
            col1, col2 = st.columns(2)
            with col1:
                st.write(file.name)
            with col2:
                file_to_delete = file.name
                delete_file = st.button("Delete", key=f"delete_{file_to_delete}_{idx}")
                if delete_file:
                    files_list = [f for f in files_list if f.name != file_to_delete]
                    st.session_state.files_list = files_list
    else:
        st.write("No files are uploaded")

def delete_file(file_name):
    st.session_state.files_list = [file for file in st.session_state.files_list if file.name != file_name]
    st.success(f"File {file_name} has been deleted.")

def get_file_by_name(file_name):
    for file in st.session_state.files_list:
        if file.name == file_name:
            return file
    return None

def update_file_in_session(file):
    for idx, f in enumerate(st.session_state.files_list):
        if f.name == file.name:
            st.session_state.files_list[idx] = file
            break