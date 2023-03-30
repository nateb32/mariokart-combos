import numpy as np
import streamlit as st
from streamlit_extras.buy_me_a_coffee import button

import getmariodata
import tools

## ----- MAKE WEBPAGE -----
st.set_page_config(page_title="Optimize-Me-Mario", layout="wide")
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# col1, col2 = st.columns([4, 1])
# with col2:
#     button(username="natebrawn", floating=False, width=221)

with st.sidebar:
    button(username="natebrawn", floating=False, width=221)

st.image("Racer Optimization Tool.png")
st.subheader(":orange[_Discover_] Your Racers!")
st.markdown(
    ":violet[Select priorities and filtering in the sidebar for more useful results.]"
)

## ----- Read In CSV Data -----
full_combosDF = tools.readData("MarioKart8D_Combos.csv")
combosDF = full_combosDF
# Get unique values of each item:
options = tools.getOptions(full_combosDF)


## ----- PRIORITIES FORM -----
@st.cache_data
def sortDF(combosDF, sortby):
    return combosDF.sort_values(by=sortby, ascending=False)


setupcols = ["Driver", "Body", "Tires", "Glider"]
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
allstats_abrev = list(combosDF.columns.values[4:])
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

with st.sidebar.form("priorities"):
    st.subheader(":green[PRIORITIZE YOUR STATS:]")
    statpriorities = st.multiselect(
        "Stat Priorities (order matters):",
        allstats,
        help="In-Game Stats:  \n:blue[Ground Speed (SL)], :violet[Acceleration (AC)], :green[Weight (WG)],  \n:orange[Ground Handling (TL)], and :red[Off-Road Traction (OF)]",
    )
    sortvals = [prt[-3:-1] for prt in statpriorities]

    priorities_submitted = st.form_submit_button("Submit")
    if statpriorities != []:
        combosDF = sortDF(combosDF, sortvals)


## ----- FILTERS FORM -----
@st.cache_data
def filterDF(combosDF, racer_filter, body_filter, tires_filter, glider_filter):
    if any(
        [racer_filter != [], body_filter != [], tires_filter != [], glider_filter != []]
    ):
        if racer_filter != []:
            combosDF = combosDF[combosDF.Driver.isin(racer_filter)]
        if body_filter != []:
            combosDF = combosDF[combosDF.Body.isin(body_filter)]
        if tires_filter != []:
            combosDF = combosDF[combosDF.Tires.isin(tires_filter)]
        if glider_filter != []:
            combosDF = combosDF[combosDF.Glider.isin(glider_filter)]
    return combosDF


with st.sidebar.form("filters"):
    st.subheader(":green[FILTERS]")
    racer_filter = st.multiselect("Racers:", options.Driver)
    body_filter = st.multiselect("Body:", options.Body)
    tires_filter = st.multiselect("Tires:", options.Tires)
    glider_filter = st.multiselect("Glider:", options.Glider)

    filters_submitted = st.form_submit_button("Submit")
    combosDF = filterDF(
        combosDF, racer_filter, body_filter, tires_filter, glider_filter
    )

## ----- DISPLAY DATAFRAME -----
combosDF = combosDF.reset_index(drop=True)

# if "gamestatsbutt" not in st.session_state:
#     gamestatsbutt = False
# if "statnamesbutt" not in st.session_state:
#     statnamesbutt = False

# Show only top 1000 values
maxrows = len(combosDF)
numrows = maxrows
if maxrows > 1000:
    numrows = 1000
    combosDF = combosDF.iloc[:numrows, :]

## --- OPTION BUTTONS
butt1, butt2, butt3, butt4, butt5 = st.columns(5)
# In-Game Stats Only Button
gamestatsbutt = butt1.checkbox("Only In-Game Stats")
if gamestatsbutt:
    # if statnamesbutt:
    #     combosDF = combosDF[setupcols + ingamestats]
    # else:
    combosDF = combosDF[setupcols + ingamestats_abrev]

# Stat Names Button
statnamesbutt = butt2.checkbox("Show Stat Names")
if statnamesbutt:
    if gamestatsbutt:
        combosDF.columns = setupcols + ingamestats
    else:
        combosDF.columns = setupcols + allstats

# HeatMap Button
heatmapbutt = butt3.checkbox("Show HeatMap")
if heatmapbutt:
    if maxrows >= 100:
        numrows = 100
    heatstyler = (
        combosDF.iloc[:numrows, :]
        .style.format(precision=2)
        .background_gradient(
            axis=0,
            vmin=0,
            vmax=6,
            subset=list(combosDF.columns.values[4:]),
            cmap="YlOrRd",
        )
        .set_table_styles([dict(selector="th", props=[("text-align", "center")])])
    )
    maindata = heatstyler.set_properties(**{"text-align": "center"}).hide(axis="index")
else:
    maindata = combosDF

# Display Main DataFrame
st.dataframe(maindata)

# Information below the dataframe
st.markdown(
    "**:orange[Displaying]**  :green["
    + str(numrows)
    + "] **:orange[out of]** :blue["
    + str(maxrows)
    + "] **:orange[options]**"
)

## ----- TOP SETUP -----
if st.button(
    "What are the highest scored setups?", help="Scored by aggregate sum of all stats"
):
    summedstats = full_combosDF.iloc[:, 4:].sum(axis=1)
    maxsum = max(summedstats)
    max_idxs = [idx for idx in summedstats.index if summedstats[idx] == maxsum]
    bestsetups = full_combosDF.iloc[max_idxs]
    st.dataframe(bestsetups)


## ----- PROMPT TO PULL IN MARIO KART DATA ---
st.sidebar.subheader(":blue[Stats out-of-date? Tap this button ↓]")
if st.sidebar.button("Get New Data"):
    with st.spinner(text="Pulling in Mario Kart Data..."):
        getmariodata.pullwiki()
        st.balloons()
        st.success("Done!")
