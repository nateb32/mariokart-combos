# from os.path import exists

import pandas as pd
import streamlit as st

# ----- CONSTANTS -----
# List out statistic names and abreviations
allstats = [
    "Weight (WG)",
    "Acceleration (AC)",
    "On-Road traction (ON)",
    "Off-Road Traction (OF)",
    "Mini-Turbo (MT)",
    "Ground Speed (SL)",
    "Water Speed (SW)",
    "Anti-Gravity Speed (SA)",
    "Air Speed (SG)",
    "Ground Handling (TL)",
    "Water Handling (TW)",
    "Anti-Gravity Handling (TA)",
    "Air Handling (TG)",
]
allstats_abrev = list(allstats[4:])
ingamestats = [
    "Ground Speed (SL)",
    "Acceleration (AC)",
    "Weight (WG)",
    "Ground Handling (TL)",
    "Off-Road Traction (OF)",
]
ingamestats_abrev = [
    "SL",
    "AC",
    "WG",
    "TL",
    "OF",
]



## ----- FUNCTIONS -----
@st.cache_data
def readData(csvfile):
    # if not exists(csvfile):
    #     getmariodata.pullwiki()
    return pd.read_csv(csvfile, index_col=False)


def getOptions(data):
# Get unique values of each item:
    options = pd.Series({c: data.iloc[:, :5][c].unique() for c in data.iloc[:, :5]})
    return options

def hidehamburger():
# Hide hamburger menu
    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

# SORTING FUNCTION
@st.cache_data
def sortStats(combosDF, sortby):
    return combosDF.sort_values(by=sortby, ascending=False)

@st.cache_data
def filterStats(combosDF, racer_filter, body_filter, tires_filter, glider_filter):
    if racer_filter != []:
        combosDF = combosDF[combosDF.Driver.isin(racer_filter)]
    if body_filter != []:
        combosDF = combosDF[combosDF.Body.isin(body_filter)]
    if tires_filter != []:
        combosDF = combosDF[combosDF.Tires.isin(tires_filter)]
    if glider_filter != []:
        combosDF = combosDF[combosDF.Glider.isin(glider_filter)]
    return combosDF

def cutdownDF(dataframe):
# Show only top 1000 values
    maxrows = len(dataframe)
    numrows = maxrows
    if maxrows > 1000:
        numrows = 1000
        dataframe = dataframe.iloc[:numrows, :]
    return dataframe, maxrows, numrows