import pandas as pd
import numpy as np
import math

# Fomula reference https://www.drillingformulas.com/minimum-curvature-method/
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
        #print(dDepth + dip_1 + dip_2 + RF)

        return(MD, RF, dN, dE, dV)
    else:
        return(MD, 0, 0, 0, MD)

# Looping through dataframe for each hole and calculating drill trace from the collar down
def calc_drilltraces(df_collar, df_survey, required_cols_df_collar, required_cols_df_survey, collar_df_reassigned_dtypes, survey_df_reassigned_dtypes):
    
    collar_df_reassigned_dtypes = {k: collar_df_reassigned_dtypes[v] for k, v in required_cols_df_collar.items()}
    survey_df_reassigned_dtypes = {k: survey_df_reassigned_dtypes[v] for k, v in required_cols_df_survey.items()}
    st.write(required_cols_df_collar)
    df_collar.rename(columns = required_cols_df_collar)
    df_survey.rename(columns = required_cols_df_survey)
    
    df_collar_xyz = df_collar[['HOLEID', 'DH_X', 'DH_Y', 'DH_RL']]
    df_collar_xyz=df_collar_xyz.merge(df_survey[['HOLEID','DEPTH','AZIMUTH','DIP']],how='left',on='HOLEID')
    df_collar_xyz.loc[df_collar_xyz['DEPTH'] != 0, ['DH_X', 'DH_Y', 'DH_RL']] = np.nan
    df_collar_xyz.sort_values(['HOLEID', 'DEPTH'], ascending=True)
    unique = df_collar_xyz['HOLEID'].unique()
    size_test = df_collar_xyz.groupby(['HOLEID']).size()
    
    for i, val in enumerate(unique):
        for index, row in df_collar_xyz.loc[df_collar_xyz['HOLEID']==unique[i]].iterrows():
            if row[4] == 0:
                df_collar_xyz.at[index, 'DH_dX'] = 0
                df_collar_xyz.at[index, 'DH_dY'] = 0
                df_collar_xyz.at[index, 'DH_dRL'] = 0

            if row[4] > 0:
                results = calculate_xyz(row_previous[4], row_previous[6], row_previous[5], row[4], row[6], row[5])

                df_collar_xyz.at[index, 'DH_X'] = row_previous[1] + results[3]
                df_collar_xyz.at[index, 'DH_Y'] = row_previous[2] + results[2]
                df_collar_xyz.at[index, 'DH_RL'] = row_previous[3] - results[4]

                df_collar_xyz.at[index, 'DH_dX'] = results[3]
                df_collar_xyz.at[index, 'DH_dY'] = results[2]
                df_collar_xyz.at[index, 'DH_dRL'] = results[4]

            row_previous = df_collar_xyz.iloc[index]
    return df_collar_xyz
