#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import numpy as np
from scipy import interpolate

def load_collar_file():
    collar_df = load_data("collar")
    if collar_df is not None:
        id_col = st.selectbox("Select the column containing the drillhole ID", collar_df.columns)
        x_col = st.selectbox("Select the column containing the X coordinate", collar_df.columns)
        y_col = st.selectbox("Select the column containing the Y coordinate", collar_df.columns)
        z_col = st.selectbox("Select the column containing the Z coordinate", collar_df.columns)
        extra_cols = st.multiselect("Select any additional columns to display", collar_df.columns)
        return collar_df, id_col, x_col, y_col, z_col, extra_cols
    else:
        return None, None, None, None, None, None

def load_survey_file():
    survey_df = load_data("survey")
    if survey_df is not None:
        id_col = st.selectbox("Select the column containing the drillhole ID", survey_df.columns)
        depth_col = st.selectbox("Select the column containing the depth", survey_df.columns)
        dip_col = st.selectbox("Select the column containing the dip", survey_df.columns)
        azimuth_col = st.selectbox("Select the column containing the azimuth", survey_df.columns)
        extra_cols = st.multiselect("Select any additional columns to display", survey_df.columns)
        return survey_df, id_col, depth_col, dip_col, azimuth_col, extra_cols
    else:
        return None, None, None, None, None, None

def calculate_drillhole_traces(collar_df, id_col_collar, x_col, y_col, z_col, survey_df, id_col_survey, depth_col, dip_col, azimuth_col):
    traces = {}
    for id, collar in collar_df[[id_col_collar, x_col, y_col, z_col]].groupby(id_col_collar):
        survey = survey_df[survey_df[id_col_survey] == id]
        survey["dx"] = np.cos(np.radians(survey[dip_col])) * np.cos(np.radians(survey[azimuth_col]))
        survey["dy"] = np.cos(np.radians(survey[dip_col])) * np.sin(np.radians(survey[azimuth_col]))
        survey["dz"] = -np.sin(np.radians(survey[dip_col]))
        survey["x"] = collar[x_col] + survey["dx"].cumsum()
        survey["y"] = collar[y_col] + survey["dy"].cumsum()
        survey["z"] = collar[z_col] + survey["dz"].cumsum()
        traces[id] = survey[["x", "y", "z", depth_col]].values
    return traces

def load_point_data():
    point_file = st.file_uploader("Upload point data file (.csv or .xlsx)")
    if point_file is not None:
        point_df = pd.read_csv(point_file) if point_file.endswith(".csv") else pd.read_excel(point_file)
        id_col = st.selectbox("Select the column containing the drillhole ID", point_df.columns)
        depth_col = st.selectbox("Select the column containing the depth", point_df.columns)
        extra_cols = st.multiselect("Select any additional columns to display", point_df.columns)
        return point_df, id_col, depth_col, extra_cols
    else:
        return None, None, None, None

def load_interval_data():
    interval_file = st.file_uploader("Upload interval data file (.csv or .xlsx)")
    if interval_file is not None:
        interval_df = pd.read_csv(interval_file) if interval_file.endswith(".csv") else pd.read_excel(interval_file)
        id_col = st.selectbox("Select the column containing the drillhole ID", interval_df.columns)
        from_col = st.selectbox("Select the column containing the 'from' depth", interval_df.columns)
        to_col = st.selectbox("Select the column containing the 'to' depth", interval_df.columns)
        extra_cols = st.multiselect("Select any additional columns to display", interval_df.columns)
        return interval_df, id_col, from_col, to_col, extra_cols
    else:
        return None, None, None, None, None

def interpolate_points(traces, point_df, id_col, depth_col):
    points = {}
    for id, group in point_df.groupby(id_col):
        if id in traces:
            f = interpolate.interp1d(traces[id][:, 3], traces[id][:, :3], axis=0, fill_value="extrapolate")
            points[id] = f(group[depth_col]).tolist()
    return points

def interpolate_intervals(traces, interval_df, id_col, from_col, to_col):
    intervals = {}
    for id, group in interval_df.groupby(id_col):
        if id in traces:
            f = interpolate.interp1d(traces[id][:, 3], traces[id][:, :3], axis=0, fill_value="extrapolate")
            intervals[id] = [f(group[from_col]), f(group[to_col])]
    return intervals

def plot_drillholes(traces, intervals, interval_df, data_cols, show_annotation):
    import plotly.graph_objs as go
    fig = go.Figure()
    for id, trace in traces.items():
        x = trace[:, 0]
        y = trace[:, 1]
        z = trace[:, 2]
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', name=id))
    for id, interval in intervals.items():
        if id in traces:
            x = [traces[id][0][0], traces[id][-1][0]]
            y = [traces[id][0][1], traces[id][-1][1]]
            z = [traces[id][0][2], traces[id][-1][2]]
            interval_data = interval_df[interval_df[id_col] == id]
            fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', name=id+'_interval'))
            if show_annotation:
                for i, point in enumerate(interval):
                    text = ', '.join([f"{col}: {interval_data.iloc[i][col]}" for col in data_cols])
                    fig.add_trace(go.Scatter3d(x=[point[0]], y=[point[1]], z=[point[2]], text=text, mode='markers', name=id+'_interval'))
    st.plotly_chart(fig)
    
def load_data(file_type):
    file = st.file_uploader(f"Upload {file_type} file (.csv or .xlsx)")
    if file is not None:
        try:
            if file.name.endswith(".csv"):
                file_contents = file.read()
                df = pd.read_csv(file_contents, encoding='utf-8')
            elif file.name.endswith(".xlsx"):
                df = pd.read_excel(file)
            else:
                st.error("File must be of type .csv or .xlsx")
                return None
            st.dataframe(df.head())
            return df
        except UnicodeDecodeError as e:
            try:
                file_contents = file.read()
                df = pd.read_csv(file_contents, encoding='latin-1')
                st.dataframe(df.head())
                return df
            except:
                try:
                    file_contents = file.read()
                    df = pd.read_csv(file_contents, encoding='iso-8859-1')
                    st.dataframe(df.head())
                    return df
                except:
                    try:
                        # remove invalid characters
                        file_contents = file.read()
                        df = pd.read_csv(file_contents, encoding='utf-8', errors='replace')
                        df.replace(r'[^\x00-\x7F]+', '', regex=True, inplace=True)
                        st.dataframe(df.head())
                        return df
                    except:
                        st.error("An error occurred while trying to read the file. Please check the file format and try again.")
                        return None
    else:

def load_interval_data():
    interval_df = load_data("interval")
    if interval_df is not None:
        id_col = st.selectbox("Select the column containing the drillhole ID", interval_df.columns)
        from_col = st.selectbox("Select the column containing the 'from' value", interval_df.columns)
        to_col = st.selectbox("Select the column containing the 'to' value", interval_df.columns)
        if from_col == to_col:
            st.error("'from' column and 'to' column should be different")
            return None, None, None, None
        if not (interval_df[from_col] <= interval_df[to_col]).all():
            st.error("'from' column should be less than or equal to 'to' column")
            return None, None, None, None
        extra_cols = st.multiselect("Select any additional columns to display", interval_df.columns)
        return interval_df, id_col, from_col, to_col, extra_cols
    else:
        return None, None, None, None, None

def interpolate_interval_data(interval_df, id_col, from_col, to_col, traces):
    interpolated_data = {}
    for id, intervals in interval_df[[id_col, from_col, to_col]].groupby(id_col):
        if id in traces:
            trace = traces[id]
            f = interpolate.interp1d(trace[:, 3], trace[:, :3], axis=0)
            intervals["distance_from"] = f(intervals[from_col])[:, 3]
            intervals["distance_to"] = f(intervals[to_col])[:, 3]
            interpolated_data[id] = intervals[["distance_from", "distance_to"]].values
    return interpolated_data

    
def main():
    collar_df = load_data("collar")
    if collar_df is not None:
        id_col = st.selectbox("Select the column containing the drillhole ID", collar_df.columns)
        x_col = st.selectbox("Select the column containing the X coordinate", collar_df.columns)
        y_col = st.selectbox("Select the column containing the Y coordinate", collar_df.columns)
        z_col = st.selectbox("Select the column containing the Z coordinate", collar_df.columns)
        extra_cols = st.multiselect("Select any additional columns to display", collar_df.columns)
    survey_df = load_data("survey")
    if survey_df is not None:
        id_col = st.selectbox("Select the column containing the drillhole ID", survey_df.columns)
        depth_col = st.selectbox("Select the column containing the depth", survey_df.columns)
        dip_col = st.selectbox("Select the column containing the dip", survey_df.columns)
        azimuth_col = st.selectbox("Select the column containing the azimuth", survey_df.columns)
        extra_cols = st.multiselect("Select any additional columns to display", survey_df.columns)
    if collar_df is not None and survey_df is not None:
        traces = calculate_drillhole_traces(collar_df, id_col_collar, x_col, y_col, z_col, survey_df, id_col_survey, depth_col, dip_col, azimuth_col)
        st.write("Drillhole traces:", drillhole_traces)

if __name__ == "__main__":
    main()
