# drill_traces.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import logging
import plotly.graph_objects as go

logger = logging.getLogger(__name__)

def calculate_xyz(depth_1, dip_1, azi_1, depth_2, dip_2, azi_2):
    MD = depth_2 - depth_1
    if abs(dip_1) != 90:
        dip_1 = np.radians(90 + dip_1)
        dip_2 = np.radians(90 + dip_2)
        azi_1 = np.radians(azi_1)
        azi_2 = np.radians(azi_2)
        
        B_rad = np.arccos(np.cos(dip_2 - dip_1) - (np.sin(dip_1) * np.sin(dip_2) * (1 - np.cos(azi_2 - azi_1))))
        RF = (2 / B_rad) * np.tan(B_rad / 2) if B_rad != 0 else 1

        dDepth = MD / 2
        dN = dDepth * ((np.sin(dip_1) * np.cos(azi_1)) + (np.sin(dip_2) * np.cos(azi_2))) * RF
        dE = dDepth * ((np.sin(dip_1) * np.sin(azi_1)) + (np.sin(dip_2) * np.sin(azi_2))) * RF
        dV = dDepth * (np.cos(dip_1) + np.cos(dip_2)) * RF

        return MD, RF, dN, dE, dV
    else:
        return MD, 1, 0, 0, MD

def generate_drilltraces(df_collar, df_survey):
    try:
        # Ensure required columns are present
        required_collar_cols = ['HoleID', 'DH_X', 'DH_Y', 'DH_Z']
        required_survey_cols = ['HoleID', 'Depth', 'Azimuth', 'Dip']
        
        for col in required_collar_cols:
            if col not in df_collar.columns:
                raise ValueError(f"Required column '{col}' not found in collar data")
        
        for col in required_survey_cols:
            if col not in df_survey.columns:
                raise ValueError(f"Required column '{col}' not found in survey data")

        # Merge collar and survey data
        df_traces = df_collar[required_collar_cols].merge(df_survey[required_survey_cols], on='HoleID', how='inner')

        # Sort by HoleID and Depth
        df_traces = df_traces.sort_values(['HoleID', 'Depth'])

        # Initialize columns for calculated values
        df_traces['DH_dX'] = 0.0
        df_traces['DH_dY'] = 0.0
        df_traces['DH_dZ'] = 0.0

        # Group by HoleID and calculate drill traces
        for hole_id, group in df_traces.groupby('HoleID'):
            x_prev, y_prev, z_prev = group.iloc[0][['DH_X', 'DH_Y', 'DH_Z']]
            depth_prev, dip_prev, azi_prev = 0, group.iloc[0]['Dip'], group.iloc[0]['Azimuth']

            for idx, row in group.iterrows():
                depth, dip, azi = row['Depth'], row['Dip'], row['Azimuth']
                
                if depth > 0:
                    MD, RF, dN, dE, dV = calculate_xyz(depth_prev, dip_prev, azi_prev, depth, dip, azi)
                    
                    df_traces.at[idx, 'DH_dX'] = dE
                    df_traces.at[idx, 'DH_dY'] = dN
                    df_traces.at[idx, 'DH_dZ'] = dV
                    
                    x_prev += dE
                    y_prev += dN
                    z_prev -= dV  # Subtract dV because depth increases downwards
                    
                    df_traces.at[idx, 'DH_X'] = x_prev
                    df_traces.at[idx, 'DH_Y'] = y_prev
                    df_traces.at[idx, 'DH_Z'] = z_prev

                depth_prev, dip_prev, azi_prev = depth, dip, azi

        return df_traces

    except Exception as e:
        logger.error(f"Error in generate_drill_traces: {str(e)}")
        raise

def generate_all_drilltraces():
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
        return pd.concat(all_drilltraces, ignore_index=True)
    else:
        return None

def plot3d_dhtraces(df_dh_traces):
    try:
        fig = go.Figure()

        # Create a trace for each hole in each dataset
        for dataset in df_dh_traces['Dataset'].unique():
            dataset_traces = df_dh_traces[df_dh_traces['Dataset'] == dataset]
            for hole_id in dataset_traces['HoleID'].unique():
                hole_data = dataset_traces[dataset_traces['HoleID'] == hole_id]
                fig.add_trace(go.Scatter3d(
                    x=hole_data['DH_X'],
                    y=hole_data['DH_Y'],
                    z=hole_data['DH_Z'],
                    mode='lines',
                    name=f"{dataset} - {hole_id}",
                    line=dict(width=4),
                    hoverinfo='text',
                    text=[f'Dataset: {dataset}<br>HoleID: {hole_id}<br>Depth: {depth:.2f}<br>X: {x:.2f}<br>Y: {y:.2f}<br>Z: {z:.2f}'
                          for depth, x, y, z in zip(hole_data['Depth'], hole_data['DH_X'], hole_data['DH_Y'], hole_data['DH_Z'])]
                ))

        # Create the layout
        layout = go.Layout(
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z',
                aspectmode='data'
            ),
            title='3D Drill Traces for All Datasets',
            hovermode='closest',
            height=800,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )

        # Create the figure and plot
        fig.update_layout(layout)
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Failed to plot 3D drill traces: {str(e)}")
        logger.error(f"3D plotting error: {str(e)}", exc_info=True)

def validate_drill_traces(df_drilltraces):
    st.write("Validating drill traces")
    
    # Check for missing values
    missing_values = df_drilltraces.isnull().sum()
    if missing_values.sum() > 0:
        st.warning("Missing values detected in the following columns:")
        st.write(missing_values[missing_values > 0])
    else:
        st.success("No missing values detected")

    # Check for negative depths
    negative_depths = df_drilltraces[df_drilltraces['Depth'] < 0]
    if not negative_depths.empty:
        st.warning("Negative depths detected:")
        st.write(negative_depths)
    else:
        st.success("No negative depths detected")

    # Check for duplicate entries
    duplicates = df_drilltraces[df_drilltraces.duplicated()]
    if not duplicates.empty:
        st.warning("Duplicate entries detected:")
        st.write(duplicates)
    else:
        st.success("No duplicate entries detected")

def analyze_drill_traces(df_drilltraces):
    st.write("Analyzing drill traces")

    # Basic statistics
    st.write("Basic statistics:")
    st.write(df_drilltraces.describe())

    # Total length of all drill holes
    total_length = df_drilltraces.groupby('HoleID')['Depth'].max().sum()
    st.write(f"Total length of all drill holes: {total_length:.2f} meters")

    # Average depth of drill holes
    avg_depth = df_drilltraces.groupby('HoleID')['Depth'].max().mean()
    st.write(f"Average depth of drill holes: {avg_depth:.2f} meters")

    # Deepest drill hole
    deepest_hole = df_drilltraces.loc[df_drilltraces.groupby('HoleID')['Depth'].idxmax()]
    st.write("Deepest drill hole:")
    st.write(deepest_hole)

    # Distribution of dips and azimuths
    st.write("Distribution of dips:")
    st.hist_chart(df_drilltraces['Dip'])
    st.write("Distribution of azimuths:")
    st.hist_chart(df_drilltraces['Azimuth'])