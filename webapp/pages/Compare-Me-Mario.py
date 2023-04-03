import altair as alt
import pandas as pd
import streamlit as st
from streamlit_extras.buy_me_a_coffee import button
from utils import tools

with st.sidebar:
    button(username="natebrawn", floating=False, width=221)

st.subheader(":orange[_Compare_] Your Racers!")
st.markdown(":violet[Select the setups you would like to compare in the sidebar.]")
## ----- BRING IN DATA -----
full_combosDF = tools.readData("data\MarioKart8D_Combos.csv")
combosDF = full_combosDF
# Get unique values of each item:
options = tools.getOptions(full_combosDF)


## ----- COMPARISON TAB -----
def getsetup(data, r, b, t, g):
    return data[
        (data["Driver"] == r)
        & (data["Body"] == b)
        & (data["Tires"] == t)
        & (data["Glider"] == g)
    ]


def newracer(setupnum):
    st.subheader(":violet[Setup " + str(setupnum) + ":]")
    rc = st.selectbox(
        "Racer",
        options.Driver,
        label_visibility="collapsed",
        key="racercomp" + str(setupnum),
    )
    bc = st.selectbox(
        "Body",
        options.Body,
        label_visibility="collapsed",
        key="bodycomp" + str(setupnum),
    )
    tc = st.selectbox(
        "Tires",
        options.Tires,
        label_visibility="collapsed",
        key="tirescomp" + str(setupnum),
    )
    gc = st.selectbox(
        "Glider",
        options.Glider,
        label_visibility="collapsed",
        key="glidercomp" + str(setupnum),
    )
    return rc, bc, tc, gc


if "numsetups" not in st.session_state:
    st.session_state["numsetups"] = 2

with st.sidebar:
    if st.button("Add Another Setup"):
        st.session_state.numsetups += 1
        if st.session_state.numsetups >= 5:
            st.session_state.numsetups = 2

    with st.form("compareracers"):
        rc1, bc1, tc1, gc1 = newracer(1)
        rc2, bc2, tc2, gc2 = newracer(2)
        if st.session_state.numsetups >= 3:
            rc3, bc3, tc3, gc3 = newracer(3)
        if st.session_state.numsetups >= 4:
            rc4, bc4, tc4, gc4 = newracer(4)

        compsubmitted = st.form_submit_button(
            "**COMPARE THESE RACERS**", type="primary", use_container_width=True
        )

if compsubmitted:
    # Make way to send warning if two options are equal
    # default =  [options.Driver[0], options.Body[0], options.Tires[0], options.Glider[0]]

    setup1 = getsetup(full_combosDF, rc1, bc1, tc1, gc1)
    setup2 = getsetup(full_combosDF, rc2, bc2, tc2, gc2)
    mashsetup = [setup1, setup2]
    if st.session_state.numsetups >= 3:
        setup3 = getsetup(full_combosDF, rc3, bc3, tc3, gc3)
        mashsetup = [setup1, setup2, setup3]
    if st.session_state.numsetups >= 4:
        setup4 = getsetup(full_combosDF, rc4, bc4, tc4, gc4)
        mashsetup = [setup1, setup2, setup3, setup4]

    comparisonDF = pd.concat(mashsetup).transpose()
    comparisonDF = pd.concat(
        [
            pd.Series(comparisonDF.iloc[4:, :].index),
            pd.DataFrame(comparisonDF.iloc[4:, :].values),
        ],
        axis=1,
    )
    comparisonDF.columns = ["Stats"] + [
        "Setup " + str(snum) for snum in range(1, st.session_state.numsetups + 1)
    ]

    valuecols = list(comparisonDF.columns[1:])
    meltedComps = pd.melt(comparisonDF, id_vars=["Stats"], value_vars=valuecols)
    st.dataframe(comparisonDF)
    chart = (
        alt.Chart(meltedComps, title="Racer Setup Comparison")
        .mark_bar(
            opacity=0.8,
        )
        .encode(
            column=alt.Column(
                "Stats:O",
                spacing=5,
                header=alt.Header(labelOrient="bottom", labelColor="green"),
            ),
            x=alt.X("variable", sort=valuecols, axis=None),
            y=alt.Y("value:Q"),
            color=alt.Color("variable"),
        )
    )

    st.altair_chart(chart, theme="streamlit")
st.image("assets\Racer Optimization Tool.png")
