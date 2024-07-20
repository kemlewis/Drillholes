import streamlit as st
import pandas as pd
import io
import chardet
import logging

logger = logging.getLogger(__name__)

def read_file_chardet(uploaded_file):
    try:
        # Read the file content
        file_content = uploaded_file.read()
        
        # Check if it's an Excel file
        if uploaded_file.name.endswith(('xlsx', 'xls', 'xlsm')):
            # Use pandas to read Excel file
            df = pd.read_excel(io.BytesIO(file_content))
        else:
            # For CSV and TXT files, use chardet to detect encoding
            result = chardet.detect(file_content)
            encoding = result['encoding']
            confidence = result['confidence']
            st.write(f"The encoding of {uploaded_file.name} is {encoding} with a confidence of {confidence}")
            
            # Decode the content using the detected encoding
            text_content = file_content.decode(encoding)
            
            # Use pandas to read CSV
            df = pd.read_csv(io.StringIO(text_content))
        
        st.success(f"Successfully read {uploaded_file.name}")
        return df
    except Exception as e:
        st.error(f"Error reading file {uploaded_file.name}: {str(e)}")
        logger.error(f"File reading error: {str(e)}", exc_info=True)
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