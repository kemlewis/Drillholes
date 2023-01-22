import streamlit as st

# Create a function for each page
def load_collar():
    st.write("This is the Load Collar page.")

def load_survey():
    st.write("This is the Load Survey page.")

def load_point_data():
    st.write("This is the Load Point Data page.")

def load_interval_data():
    st.write("This is the Load Interval Data page.")

def plot_3d():
    st.write("This is the 3d Plot page.")

# Create a function to navigate between pages
def navigate():
    page = st.sidebar.selectbox("Select a page", ["Load Collar", "Load Survey", "Load Point Data", "Load Interval Data", "3d Plot"])
    if page == "Load Collar":
        load_collar()
    elif page == "Load Survey":
        load_survey()
    elif page == "Load Point Data":
        load_point_data()
    elif page == "Load Interval Data":
        load_interval_data()
    elif page == "3d Plot":
        plot_3d()

def main():
    st.set_page_config(page_title="My App", page_icon=":guardsman:", layout="wide")
    navigate()

if __name__ == "__main__":
    main()
