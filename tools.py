from os.path import exists

import pandas as pd
import streamlit as st

import getmariodata


## ----- Read In CSV Data -----
@st.cache_data
def readData(csvfile):
    if not exists(csvfile):
        getmariodata.pullwiki()
    return pd.read_csv(csvfile, index_col=False)


def getOptions(data):
    # Get unique values of each item:
    options = pd.Series({c: data.iloc[:, :5][c].unique() for c in data.iloc[:, :5]})
    return options
