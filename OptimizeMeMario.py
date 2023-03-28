from os.path import exists

import pandas as pd
import streamlit as st

import getmariodata
import tools

## ----- MAKE WEBPAGE -----
st.set_page_config(page_title="Optimize-Me-Mario", layout="wide")
# tab1, tab2 = st.tabs(["Data-Me-Mario", "Compare-Me-Mario"])

# with tab1:
st.header("Let's :orange[_Discover_] Your Racers!")
st.markdown(
    ":violet[Select priorities and filtering in the sidebar for more useful results.]"
)
# with tab2:
#     st.header("Let's :orange[_Compare_] Your Racers!")


# ## ----- Read In CSV Data -----
# @st.cache_data
# def readData(csvfile):
#     if not exists(csvfile):
#         with st.spinner(text="Pulling in Mario Kart Data..."):
#             getmariodata.pullwiki()
#             st.balloons()
#             st.success("Done!")
#     return pd.read_csv("MarioKart8D_Combos.csv", index_col=False)

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
# with tab1:
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


# ## ----- COMPARISON TAB -----
# def getsetup(data, r, b, t, g):
#     return data[
#         (data["Driver"] == r)
#         & (data["Body"] == b)
#         & (data["Tires"] == t)
#         & (data["Glider"] == g)
#     ]


# def newracer(setupnum):
#     st.subheader(":violet[Setup " + str(setupnum) + ":]")
#     rc = st.selectbox(
#         "Racer",
#         options.Driver,
#         label_visibility="collapsed",
#         key="racercomp" + str(setupnum),
#     )
#     bc = st.selectbox(
#         "Body",
#         options.Body,
#         label_visibility="collapsed",
#         key="bodycomp" + str(setupnum),
#     )
#     tc = st.selectbox(
#         "Tires",
#         options.Tires,
#         label_visibility="collapsed",
#         key="tirescomp" + str(setupnum),
#     )
#     gc = st.selectbox(
#         "Glider",
#         options.Glider,
#         label_visibility="collapsed",
#         key="glidercomp" + str(setupnum),
#     )
#     return rc, bc, tc, gc


# with tab2:
#     if "numsetups" not in st.session_state:
#         st.session_state["numsetups"] = 2

#     if st.button("Add Another Setup"):
#         st.session_state.numsetups += 1
#         if st.session_state.numsetups >= 5:
#             numsetups = 2

#     with st.form("compareracers"):
#         mcol1, mcol2 = st.columns(2)
#         with mcol1:
#             rc1, bc1, tc1, gc1 = newracer(1)
#             if st.session_state.numsetups == 3:
#                 rc3, bc3, tc3, gc3 = newracer(3)
#         with mcol2:
#             rc2, bc2, tc2, gc2 = newracer(2)
#             if st.session_state.numsetups == 4:
#                 rc4, bc4, tc4, gc4 = newracer(4)

#         compsubmitted = st.form_submit_button(
#             "**COMPARE THESE RACERS**", type="primary", use_container_width=True
#         )

#     if compsubmitted:
#         setup1 = getsetup(full_combosDF, rc1, bc1, tc1, gc1)
#         setup2 = getsetup(full_combosDF, rc2, bc2, tc2, gc2)
#         mashsetup = [setup1, setup2]
#         if st.session_state.numsetups == 3:
#             setup3 = getsetup(full_combosDF, rc3, bc3, tc3, gc3)
#             mashsetup = [setup1, setup2, setup3]
#         if st.session_state.numsetups == 4:
#             setup4 = getsetup(full_combosDF, rc4, bc4, tc4, gc4)
#             mashsetup = [setup1, setup2, setup3, setup4]

#         comparisonDF = pd.concat(mashsetup).reset_index(drop=True)
#         # make attributes into one column
#         infocol = (
#             comparisonDF["Driver"]
#             + "+"
#             + comparisonDF["Body"]
#             + "+"
#             + comparisonDF["Tires"]
#             + "+"
#             + comparisonDF["Glider"]
#         )
#         comparisonDF = pd.concat([infocol, comparisonDF.iloc[:, 4:]], axis=1)
#         comparisonDF = comparisonDF.set_index(0).transpose()
#         st.dataframe(comparisonDF)

#         st.area_chart(comparisonDF)
#         st.bar_chart(comparisonDF)
