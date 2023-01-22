import streamlit as st

# Create a function for each page
def load_collar():
    st.title("Load Collar")
    st.write("This is the Load Collar page.")

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
    .stButton {
        width: 100%;
        text-align: center;
    }
    """
    st.sidebar.markdown(f'<style>{style}</style>', unsafe_allow_html=True)
    if st.sidebar.button("Load Collar", key='load_collar', className="stButton"):
        load_collar()
    if st.sidebar.button("Load Survey", key='load_survey', className="stButton"):
        load_survey()
    if st.sidebar.button("Load Point Data", key='load_point_data', className="stButton"):
        load_point_data()
    if st.sidebar.button("Load Interval Data", key='load_interval_data', className="stButton"):
        load_interval_data()
    if st.sidebar.button("3d Plot", key='plot_3d', className="stButton"):
        plot_3d()



def main():
    st.markdown("<h1 style='text-align:center;font-size:3rem;'>Drillhole Wizard</h1>", unsafe_allow_html=True)
    st.title("My App")
    navigate()


if __name__ == "__main__":
    main()
