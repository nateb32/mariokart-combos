from itertools import product

import pandas as pd
import requests

## ----- PULL IN MARIO KART DATA ---
html = requests.get(
    "https://www.mariowiki.com/Mario_Kart_8_Deluxe_in-game_statistics",
    verify=True,
    timeout=2,
)

dfs = pd.read_html(html.text, skiprows=1, header=0)

drivers = dfs[0][:-1].set_index(["Driver"]).astype("int")
vehicles = dfs[1].set_index(["Body"]).astype("int")
tires = dfs[2].set_index(["Tire"]).astype("int")
gliders = dfs[3].set_index(["Glider"]).astype("int")

# Format driver names
drivernames = list(drivers.index)
# remove any numbers
drivernames = [
    "".join([i for i in drivernames[ii] if not i.isdigit()])
    for ii in range(0, len(drivernames))
]
# remove spaces if they are the last character
drivernames = [
    "".join(drivernames[ii].rstrip()) for ii in range(0, len(drivernames))
]
# remove last word of each name (callsign) BUT only remove if it is not a parenthesis
drivernames = [ii.rsplit(" ", 1)[0] if ii[-1] != ")" else ii for ii in drivernames]

# Reset driver index
drivers.index = drivernames

combos = list(product(drivers.index, vehicles.index, tires.index, gliders.index))

combos_nogliders = list(product(drivers.index, vehicles.index, tires.index))

cStats_list = list(
    product(drivers.values, vehicles.values, tires.values, gliders.values)
)

cStats_list_nogliders = list(product(drivers.values, vehicles.values, tires.values))

cStats_summed = [(sum(cStats_list[ii]) + 3) / 4 for ii in range(len(cStats_list))]
cStats_summed_nogliders = [
    (sum(cStats_list_nogliders[ii]) + 3) / 4
    for ii in range(len(cStats_list_nogliders))
]

comboStats = pd.concat(
    [
        pd.DataFrame(combos, columns=["Driver", "Body", "Tires", "Glider"]),
        pd.DataFrame(cStats_summed, columns=list(drivers.columns)),
    ],
    axis=1,
)
comboStats_nogliders = pd.concat(
    [
        pd.DataFrame(combos_nogliders, columns=["Driver", "Body", "Tires"]),
        pd.DataFrame(cStats_summed_nogliders, columns=list(drivers.columns)),
    ],
    axis=1,
)

# Write to CSV if you want to
comboStats.to_csv("data/MarioKart8D_Combos.csv", index=False)
comboStats_nogliders.to_csv("data/MarioKart8D_Combos_nogliders.csv", index=False)
