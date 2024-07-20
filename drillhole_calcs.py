import pandas as pd
import numpy as np
import math
import streamlit as st

def calculate_xyz(depth_1, dip_1, azi_1, depth_2, dip_2, azi_2):
    MD = depth_2 - depth_1
    if abs(dip_1) != 90:
        dip_1 = math.radians(90 + dip_1)
        dip_2 = math.radians(90 + dip_2)
        azi_1 = math.radians(azi_1)
        azi_2 = math.radians(azi_2)
        
        B_rad = math.acos(math.cos(dip_2 - dip_1) - (math.sin(dip_1) * math.sin(dip_2) * (1 - math.cos(azi_2 - azi_1))))
        RF = (2 / B_rad) * math.tan(B_rad / 2) if B_rad != 0 else 1

        dDepth = MD / 2
        dN = dDepth * ((math.sin(dip_1) * math.cos(azi_1)) + (math.sin(dip_2) * math.cos(azi_2))) * RF
        dE = dDepth * ((math.sin(dip_1) * math.sin(azi_1)) + (math.sin(dip_2) * math.sin(azi_2))) * RF
        dV = dDepth * (math.cos(dip_1) + math.cos(dip_2)) * RF

        return MD, RF, dN, dE, dV
    else:
        return MD, 1, 0, 0, MD

def calc_drilltraces(df_collar, df_survey, required_cols_df_collar, required_cols_df_survey, collar_df_reassigned_dtypes, survey_df_reassigned_dtypes):
    try:
        # Rename columns based on required columns mapping
        df_collar = df_collar.rename(columns=required_cols_df_collar)
        df_survey = df_survey.rename(columns=required_cols_df_survey)

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
        st.error(f"Error in calc_drilltraces: {str(e)}")
        raise

def generate_drill_traces(df_collar, df_survey):
    required_cols_df_collar = {
        'HoleID': 'HoleID',
        'DH_X': 'DH_X',
        'DH_Y': 'DH_Y',
        'DH_Z': 'DH_Z'
    }
    required_cols_df_survey = {
        'HoleID': 'HoleID',
        'Depth': 'Depth',
        'Azimuth': 'Azimuth',
        'Dip': 'Dip'
    }
    collar_df_reassigned_dtypes = df_collar.dtypes.to_dict()
    survey_df_reassigned_dtypes = df_survey.dtypes.to_dict()

    return calc_drilltraces(
        df_collar,
        df_survey,
        required_cols_df_collar,
        required_cols_df_survey,
        collar_df_reassigned_dtypes,
        survey_df_reassigned_dtypes
    )