from os.path import exists

import pandas as pd
import streamlit as st

import getmariodata


## ----- Read In CSV Data -----
@st.cache_data
def readData(csvfile):
    if not exists(csvfile):
        with st.spinner(text="Pulling in Mario Kart Data..."):
            getmariodata.pullwiki()
            st.balloons()
            st.success("Done!")
    return pd.read_csv("MarioKart8D_Combos.csv", index_col=False)


def getOptions(data):
    # Get unique values of each item:
    options = pd.Series({c: data.iloc[:, :5][c].unique() for c in data.iloc[:, :5]})
    return options
