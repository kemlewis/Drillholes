import streamlit as st
import pandas as pd
import numpy as np
import math

df_collar = None
df_survey = None

def main():
    st.title("Drillhole Collar and Survey Data")
    st.write("Select the collar data file and survey data file")

    # Allow user to select collar data file
    collar_file = st.file_uploader("Select the collar data file", type="csv")
    if collar_file is not None:
        df_collar = pd.read_csv(collar_file, encoding='unicode_escape')
        
    # Allow user to select survey data file
    survey_file = st.file_uploader("Select the survey data file", type="csv")
    if survey_file is not None:
        df_survey = pd.read_csv(survey_file, encoding='unicode_escape')
        

    # Read in the selected files
    if df_collar is not None and df_survey is not None:

        st.write("Number of drillholes in collar file: " + str(len(df_collar['HOLEID'].unique())))
        st.write("Total drillhole meterage: " + str(round(df_collar.loc[df_collar["DEPTH"] > 0, "DEPTH"].sum(),0)) + " meters")
        st.write("Number of drillholes in survey file: " + str(len(df_survey['HOLEID'].unique())))
        st.write("Collar file headers: " )
        st.write(df_collar.columns.values)

        df_collar_xyz = df_collar[['HOLEID', 'DH_X', 'DH_Y', 'DH_RL']]
        df_collar_xyz=df_collar_xyz.merge(df_survey[['HOLEID','DEPTH','AZIMUTH','DIP']],how='left',on='HOLEID')
        df_collar_xyz.loc[df_collar_xyz['DEPTH'] != 0, ['DH_X', 'DH_Y', 'DH_RL']] = np.nan
        df_collar_xyz.sort_values(['HOLEID', 'DEPTH'], ascending=True)

        unique = df_collar_xyz['HOLEID'].unique()
        size_test = df_collar_xyz.groupby(['HOLEID']).size()

        # Minimum curvature formula for calcuating change in xyz from distance, dip and azi
        def calculate_xyz(depth_1, dip_1, azi_1, depth_2, dip_2, azi_2):
            MD = depth_2 - depth_1
            if abs(dip_1) != 90:
                dip_1 = math.radians(90+dip_1)
                dip_2 = math.radians(90+dip_2)
                azi_1 = math.radians(azi_1)
                azi_2 = math.radians(azi_2)

                B_rad = math.acos (math.cos(dip_2-dip_1)-(math.sin(dip_1)*math.sin(dip_2)*(1-math.cos(azi_2-azi_1))))
                B_deg = math.degrees (B_rad)
                if B_rad != 0:
                    RF = (2/B_rad)*math.tan(B_rad/2)
                else:
                    RF = 0

                dDepth = (MD/2)
                dN = dDepth*((math.sin(dip_1)*math.cos(azi_1))+(math.sin(dip_2)*math.cos(azi_2)))*RF
                dE = dDepth*((math.sin(dip_1)*math.sin(azi_1))+(math.sin(dip_2)*math.sin(azi_2)))*RF
                dV = dDepth*(math.cos(dip_1)+math.cos(dip_2))*RF

                return(MD, RF, dN, dE, dV)
            else:
                return(MD, 0, 0, 0, MD)
                
        for i, val in enumerate(unique):
            for index, row in df_collar_xyz.loc[df_collar_xyz['HOLEID']==unique[i]].iterrows():
                if row[4] > 0:
                    results = calculate_xyz(row_previous[4], row_previous[6], row_previous[5], row[4], row[6], row[5])
                    df_collar_xyz.at[index, 'DH_X'] = row_previous[1] + results[3]
                    df_collar_xyz.at[index, 'DH_Y'] = row_previous[2] + results[4]
                    df_collar_xyz.at[index, 'DH_RL'] = row_previous[3] + results[5]

                row_previous = row
        
        # Show the result
        st.write("The modified dataframe with the x, y, z coordinates is:")
        st.write(df_collar_xyz)
        
if __name__ == '__main__':
    main()

