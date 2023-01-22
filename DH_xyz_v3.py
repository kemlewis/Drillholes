import streamlit as st
import pandas as pd

df_collar = pd.DataFrame()
dict_collar = {"HoleID": None, "DH_X": None, "DH_Y": None, "DH_Z": None}

# Create a function for each page
def load_collar():
    file_types = ["csv", "xlsx"]
    file_type = st.selectbox("Select file type", file_types)
    file = st.file_uploader("Upload file", type=file_types)

    # File validation and error handling
    if file is None:
        st.error("Please upload a file")
        return
    if file_type not in file.name:
        st.error("Invalid file type")
        return

    global df_collar
    try:
        if file_type == 'csv':
            for encoding in ['utf-8', 'ISO-8859-1']:
                try:
                    df_collar = pd.read_csv(file, encoding=encoding)
                    break
                except:
                    continue
        elif file_type == 'xlsx':
            df_collar = pd.read_excel(file)
    except Exception as e:
        st.error(f"Error: {e}")
        return

    if df_collar.empty:
        st.error("File contains no data")
        return
    else:
        st.success("File loaded successfully")
        st.dataframe(df_collar)
        select_columns()

def select_columns():
    # HoleID default to left-most column
    hole_id = st.selectbox("Select HoleID column", df_collar.columns, index=0)
    dict_collar["HoleID"] = hole_id
    
    x_cols = [col for col in df_collar.columns if 'x' in col.lower()]
    # DH_X default to first column that contains 'x'
    dh_x = st.selectbox("Select DH_X column", x_cols, index=0)
    dict_collar["DH_X"] = dh_x
    
    y_cols = [col for col in df_collar.columns if 'y' in col.lower()]
    # DH_Y default to first column that contains 'y'
    dh_y = st.selectbox("Select DH_Y column", y_cols, index=0)
    dict_collar["DH_Y"] = dh_y

    z_cols = [col for col in df_collar.columns if '_z' in col.lower() or 'rl' in col.lower()]
    # DH_Z default to first column that contains '_z' or 'rl'
    if z_cols:
        dh_z = st.selectbox("Select DH_Z column", z_cols, index=0)
    else:
        dh_z = st.selectbox("Select DH_Z column", df_collar.columns)
    dict_collar["DH_Z"] = dh_z
    
    if st.button("Confirm"):
        st.success("Columns selected successfully")

def load_survey():
    st.title("Load Survey")
    st.write("This is the Load Survey page.")

def load_point_data():
    st.title("Load Point Data")
    st.write("This is the Load Point Data page.")

def load_interval_data():
    st.title("Load Interval Data")
    st.write("This is the Load Interval Data page.")

def plot_3d():
    st.title("3d Plot")
    st.write("This is the 3d Plot page.")

# Create a function to navigate between pages
def navigate():
    style = """
    <style>
    .stButton {
        width: 150px;
        font-size: 1.2rem;
        text-align: center;
    }
    </style>
    """
    st.sidebar.markdown(style, unsafe_allow_html=True)
    if st.sidebar.button("Load Collar", key='load_collar'):
        load_collar()
    if st.sidebar.button("Load Survey", key='load_survey'):
        load_survey()
    if st.sidebar.button("Load Point Data", key='load_point_data'):
        load_point_data()
    if st.sidebar.button("Load Interval Data", key='load_interval_data'):
        load_interval_data()
    if st.sidebar.button("3d Plot", key='plot_3d'):
        plot_3d()



def main():
    st.markdown("<h1 style='text-align:center;font-size:3rem;'>Drillhole Wizard</h1>", unsafe_allow_html=True)
    st.title("My App")
    navigate()


if __name__ == "__main__":
    main()
