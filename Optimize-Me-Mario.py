import plotly.express as px
import streamlit as st
from streamlit_extras.buy_me_a_coffee import button

from utils import tools

# ----- MAKE WEBPAGE -----
st.set_page_config(page_title="Optimize-Me-Mariokart", layout="wide")

# Hide Hamburger
tools.hidehamburger()

# --- HEADER IMAGE AND INFO ---
st.image("assets/Racer Optimization Tool.png")
st.markdown(
    ":violet[Select priorities and filtering in the sidebar for more useful results.]"
)

# ----- Read In CSV Data -----
full_combosDF = tools.readData("data/MarioKart8D_Combos.csv")
combosDF = full_combosDF
combosDF = combosDF.reset_index(drop=True)

# Get unique values of each item:
options = tools.getOptions(full_combosDF)

# ----- OPTION BUTTONS -----
butt1, butt2, butt3, butt4, butt5 = st.columns(5)
optisortbutt = butt1.checkbox(
    "Optimized Sort", help="Sorts by MT+SL then total sum of all points"
)
statnamesbutt = butt2.checkbox("Show Stat Names")
heatmapbutt = butt3.checkbox("Show HeatMap")
gamestatsbutt = butt4.checkbox("Only In-Game Stats")
noglidersbutt = butt5.checkbox("Remove Gliders")

# ----- PRIORITIES and FILTERS FORM -----
with st.sidebar.form("filters_and_priorities"):
    # ----- PRIORITIES FORM -----
    st.subheader(":green[PRIORITIES:]")
    if gamestatsbutt:
        statchoices = tools.ingamestats
    else:
        statchoices = tools.allstats
    statpriorities = st.multiselect(
        "Stat Priorities (order matters):",
        statchoices,
        help="In-Game Stats:  \n:blue[Ground Speed (SL)], :violet[Acceleration (AC)], :green[Weight (WG)],  \n:orange[Ground Handling (TL)], and :red[Off-Road Traction (OF)]",
    )
    sortvals = [prt[-3:-1] for prt in statpriorities]
    # ----- FILTERS FORM -----
    st.subheader(":green[FILTERS:]")
    racer_filter = st.multiselect("Racers:", options.Driver)
    body_filter = st.multiselect("Body:", options.Body)
    tires_filter = st.multiselect("Tires:", options.Tires)
    glider_filter = []
    if not noglidersbutt:
        glider_filter = st.multiselect("Glider:", options.Glider)

    filterspriorities_submitted = st.form_submit_button("Submit", use_container_width=True,type='secondary')

if statpriorities != []:
    combosDF = tools.sortStats(combosDF, sortvals)

if racer_filter!=[] or body_filter!=[] or tires_filter!=[] or glider_filter!=[]:
    combosDF = tools.filterStats(
        combosDF, racer_filter, body_filter, tires_filter, glider_filter
    )


# ----- USE OPTION BUTTONS ON DATAFRAME -----

# -- Remove glider --
if noglidersbutt:    
    combosDF = tools.readData("data/MarioKart8D_Combos_nogliders.csv")

# -- Optimized Sort --
# Sorts by sum of mini-turbo and then total sum
if optisortbutt:
    opticols = ["MT+SL", "Total Pts"]
    combosDF[opticols[0]] = combosDF.iloc[:, 4:].sum(axis=1)
    combosDF[opticols[1]] = combosDF["MT"] + combosDF["SL"]
    combosDF = combosDF.sort_values(by=opticols, ascending=False)

combosDF, maxrows, numrows = tools.cutdownDF(combosDF) # make dataframe smaller

# -- In-Game Stats Only --
allcombocols = list(combosDF.columns)
setupcols = allcombocols[: allcombocols.index("WG")]
if gamestatsbutt:
    if optisortbutt:
        combosDF = combosDF[setupcols + tools.ingamestats_abrev + opticols]
    else:
        combosDF = combosDF[setupcols + tools.ingamestats_abrev]

# -- Stat Names --
if statnamesbutt:
    if gamestatsbutt:
        if optisortbutt:
            combosDF.columns = setupcols + tools.ingamestats + opticols
        else:
            combosDF.columns = setupcols + tools.ingamestats
    else:
        if optisortbutt:
            combosDF.columns = setupcols + tools.allstats + opticols
        else:
            combosDF.columns = setupcols + tools.allstats

# -- HeatMap --
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
    combosDF = heatstyler.set_properties(
        **{"text-align": "center"}).hide(axis="index")
        
if optisortbutt and statpriorities != []:
    st.warning('When Optimized Sort is selected, sidebar priorities will not be shown.')

# ----- DISPLAY MAIN DATAFRAME -----
st.dataframe(combosDF, use_container_width=True)

# Information below the dataframe
excol1, excol2 = st.columns(2)
st.markdown(
    "**:orange[Displaying]**  :green["
    + str(numrows)
    + "] **:orange[out of]** :blue["
    + str(maxrows)
    + "] **:orange[options]**"
)

# # -- BEST SETUPS --
# if excol1.button(
#     "What are the highest scored setups?", help="Scored by aggregate sum of all stats"
# ):
#     summedstats = full_combosDF.iloc[:, 4:].sum(axis=1)
#     maxsum = max(summedstats)
#     max_idxs = [idx for idx in summedstats.index if summedstats[idx] == maxsum]
#     bestsetups = full_combosDF.iloc[max_idxs]
#     st.dataframe(bestsetups)

# -- GRAPH MINI_TURBO TO GROUND SPEED --
if excol2.button("I like graphs. Show me a Mini-Turbo vs Ground Speed one"):
    dualstats = full_combosDF[["MT", "SL"]]

    fig = px.scatter(
        dualstats,
        x="MT",
        y="SL",
        title="Mini-Turbo vs Ground Speed for All Data",
        labels={"MT": "Mini-Turbo", "SL": "Ground Speed"},
    )
    st.plotly_chart(fig, theme="streamlit")


# ----- BUY ME A COFFEE BUTTON -----
with st.sidebar:
    button(username="natebrawn", floating=False, width=221)

# ----- PROMPT TO PULL IN MARIO KART DATA ---
st.sidebar.subheader(":orange[Stats out-of-date? ↓]")
getnewdatabutt = st.sidebar.button("Get New Data")
if getnewdatabutt:
    st.sidebar.write("Your request has been sent to the developer")

st.sidebar.markdown(
    ":violet[All data is from www.mariowiki.com/Mario_Kart_8_Deluxe_in-game_statistics]"
)
