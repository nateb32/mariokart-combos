from os.path import exists

import pandas as pd
import streamlit as st

import getmariodata
import tools

## ----- MAKE WEBPAGE -----
st.set_page_config(page_title="Optimize-Me-Mario", layout="wide")

st.header("Let's :orange[_Discover_] Your Racers!")
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


with st.sidebar.form("priorities"):
    st.subheader(":green[PRIORITIZE YOUR STATS:]")
    statpriorities = st.multiselect(
        "Stat Priorities (order matters):",
        ["Speed", "Acceleration", "Weight", "Traction", "Handling", "Mini-Turbo"],
    )
    sortvals = [
        prt.replace("Speed", "SL")
        .replace("Acceleration", "AC")
        .replace("Weight", "WG")
        .replace("Traction", "ON")
        .replace("Handling", "TL")
        .replace("Mini-Turbo", "MT")
        for prt in statpriorities
    ]

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
# Show the Key
if st.checkbox("Display Key"):
    st.markdown(
        ":blue[WG]: Weight :blue[AC]: Acceleration, :blue[ON]: On-Road traction, :blue[OF]: (Off-Road) Traction, :blue[MT]: Mini-Turbo  \n"
        ":blue[SL]: Ground Speed, :blue[SW]: Water Speed, :blue[SA]: Anti-Gravity Speed, :blue[SG]: Air Speed,  \n"
        ":blue[TL]: Ground Handling, :blue[TW]: Water Handling, :blue[TA]: Anti-Gravity Handling, :blue[TG]: Air Handling"
    )
# Print the DataFrame
combosDF = combosDF.reset_index(drop=True)
st.dataframe(combosDF, use_container_width=True)
st.markdown("**:orange[Current Selection:]**  " + str(len(combosDF)) + " options")

## ----- PROMPT TO PULL IN MARIO KART DATA ---
st.sidebar.subheader(":blue[Stats out-of-date? Tap this button ↓]")
if st.sidebar.button("Get New Data"):
    with st.spinner(text="Pulling in Mario Kart Data..."):
        getmariodata.pullwiki()
        st.balloons()
        st.success("Done!")
