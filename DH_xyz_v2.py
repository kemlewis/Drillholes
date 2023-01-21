#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import numpy as np
import math
#from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def open_collar_file():
    collar_file = st.file_uploader("Select Collar .csv", type=["csv"])
    if collar_file is not None:
        collar_file_path = collar_file.name
        st.success("Collar file uploaded: " + collar_file_path)
        return collar_file_path

def open_survey_file():
    survey_file = st.file_uploader("Select Survey .csv", type=["csv"])
    if survey_file is not None:
        survey_file_path = survey_file.name
        st.success("Survey file uploaded: " + survey_file_path)
        return survey_file_path

def drillhole_summary(df_collar, df_survey):
    print("Number of drillholes in collar file: " + str(len(df_collar)))
    #print("Total drillhole meterage: " + str(round(df_collar.loc[df_collar["DEPTH"] > 0, "DEPTH"].sum(),0)) + " meters")
    print("Number of drillholes in survey file: " + str(len(df_survey['HOLEID'].unique())))
    print("Collar file headers: " )
    print(df_collar.columns.values)

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
        #print(dDepth + dip_1 + dip_2 + RF)

        return(MD, RF, dN, dE, dV)
    else:
        return(MD, 0, 0, 0, MD)

# Looping through dataframe for each hole and calculating drill trace from the collar down
for i, val in enumerate(unique):
    for index, row in df_collar_xyz.loc[df_collar_xyz['HOLEID']==unique[i]].iterrows():

        if row[4] > 0:
            results = calculate_xyz(row_previous[4], row_previous[6], row_previous[5], row[4], row[6], row[5])

            df_collar_xyz.at[index, 'DH_X'] = row_previous[1] + results[3]
            df_collar_xyz.at[index, 'DH_Y'] = row_previous[2] + results[2]
            df_collar_xyz.at[index, 'DH_RL'] = row_previous[3] - results[4]
            
            df_collar_xyz.at[index, 'DH_dX'] = results[3]
            df_collar_xyz.at[index, 'DH_dY'] = results[2]
            df_collar_xyz.at[index, 'DH_dRL'] = results[4]
            
        row_previous = df_collar_xyz.iloc[index]

# Formula reference: https://www.drillingformulas.com/minimum-curvature-method/
depth_1 = 0
depth_2 = 30
dip_1 = math.radians(90-70.0)
dip_2 = math.radians(90-70.4)
azi_1 = math.radians(325)
azi_2 = math.radians(324.9)

MD = depth_2 - depth_1
B_rad = math.acos (math.cos(dip_2-dip_1)-(math.sin(dip_1)*math.sin(dip_2)*(1-math.cos(azi_2-azi_1))))
#B_deg = math.degrees (B_rad)
RF = (2/B_rad)*math.tan(B_rad/2)
    
dDepth = (MD/2)
dN = dDepth*((math.sin(dip_1)*math.cos(azi_1))+(math.sin(dip_2)*math.cos(azi_2)))*RF
dE = dDepth*((math.sin(dip_1)*math.sin(azi_1))+(math.sin(dip_2)*math.sin(azi_2)))*RF
dV = dDepth*(math.cos(dip_1)+math.cos(dip_2))*RF

get_ipython().run_line_magic('matplotlib', 'qt')

fig = plt.figure(figsize=(10, 10))
ax = plt.axes(projection='3d')
ax.scatter3D(df_collar_xyz['DH_X'], df_collar_xyz['DH_Y'], df_collar_xyz['DH_RL'])
plt.show()


#df_collar_xyz.to_csv('DH_xyz.csv')


st.title("Drillhole Calculations Example")
collar_file_path = st.button("Select Collar .csv", open_collar_file)
survey_file_path = st.button("Select Survey .csv", open_survey_file)

if collar_file_path:
    st.write("Collar file path:", collar_file_path)
    df_collar = pd.read_csv(collar_file_path)
if survey_file_path:
    st.write("Survey file path:", survey_file_path)
    df_survey = pd.read_csv(survey_file_path)
if st.button("Process data"):
        drillhole_summary(df_collar, df_survey)
