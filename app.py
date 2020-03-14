import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

Delaware = 564696
Chester = 519293
Montgomery = 826075
Bucks = 628341
philly = 1581000
S_default = Delaware + Chester + Montgomery + Bucks + philly

# Widgets
initial_infections = st.sidebar.number_input(
    "Current Known Infections", value=31, step=10, format="%i"
)
detection_prob = (
    st.sidebar.number_input(
        "Probability of Detection (%)", 0, 100, value=5, step=1, format="%i"
    )
    / 100.0
)
doubling_time = st.sidebar.number_input(
    "Doubling Time (days)", value=6, step=1, format="%i"
)
hosp_rate = (
    st.sidebar.number_input("Hospitalization %", 0, 100, value=5, step=1, format="%i")
    / 100.0
)
icu_rate = (
    st.sidebar.number_input("ICU %", 0, 100, value=2, step=1, format="%i") / 100.0
)
vent_rate = (
    st.sidebar.number_input("Ventilated %", 0, 100, value=1, step=1, format="%i")
    / 100.0
)
hosp_los = st.sidebar.number_input("Hospital LOS", value=5, step=1, format="%i")
icu_los = st.sidebar.number_input("ICU LOS", value=7, step=1, format="%i")
vent_los = st.sidebar.number_input("Vent LOS", value=14, step=1, format="%i")
S = st.sidebar.number_input(
    "Regional Population", value=S_default, step=100000, format="%i"
)
Penn_market_share = (
    st.sidebar.number_input(
        "Hospital Market Share (%)", 0, 100, value=15, step=1, format="%i"
    )
    / 100.0
)

st.title("COVID Hospital Impact Model for Epidemics")
st.subheader("SIR modeling of infections/recovery")
st.markdown(
    """Disrete-time SIR model

The model consists of individuals who are either Susceptible ( S ), Infected ( I ), or Recovered ( R ).

The epidemic proceeds via a growth and decline process. This is the core model of infectious disease spread and has been in use in epidemiology for many years."""
)

# The SIR model, one time step
def sir(y, beta, gamma, N):
    S, I, R = y
    Sn = (-beta * S * I) + S
    In = (beta * S * I - gamma * I) + I
    Rn = gamma * I + R
    if Sn < 0:
        Sn = 0
    if In < 0:
        In = 0
    if Rn < 0:
        Rn = 0

    scale = N / (Sn + In + Rn)
    return Sn * scale, In * scale, Rn * scale


# Run the SIR model forward in time
def sim_sir(S, I, R, beta, gamma, n_days, beta_decay=None):
    N = S + I + R
    s, i, r = [S], [I], [R]
    for day in range(n_days):
        y = S, I, R
        S, I, R = sir(y, beta, gamma, N)
        if beta_decay:
            beta = beta * (1 - beta_decay)
        s.append(S)
        i.append(I)
        r.append(R)

    s, i, r = np.array(s), np.array(i), np.array(r)
    return s, i, r


## RUN THE MODEL

S, I, R = S, initial_infections / detection_prob, 0

intrinsic_growth_rate = 2 ** (1 / doubling_time) - 1

recovery_days = 14.0
# mean recovery rate, gamma, (in 1/days).
gamma = 1 / recovery_days

# Contact rate, beta
beta = (
    intrinsic_growth_rate + gamma
) / S  # {rate based on doubling time} / {initial S}

n_days = 60

s, i, r = sim_sir(S, I, R, beta, gamma, n_days, beta_decay=0.005)


st.subheader("Projected Hospital Impact")
st.markdown("The number of individuals requiring hospitalization in a region")

hosp = i * hosp_rate * Penn_market_share
icu = i * icu_rate * Penn_market_share
vent = i * vent_rate * Penn_market_share
fig, ax = plt.subplots(1, 1, figsize=(10, 4))
ax.plot(hosp, ".-", label="Hospitalized")
ax.plot(icu, ".-", label="ICU")
ax.plot(vent, ".-", label="Ventilated")
ax.legend(loc=0)
ax.set_xlabel("days from today")
ax.set_ylabel("Patients")
ax.grid("on")
st.pyplot()

days = np.array(range(0, n_days + 1))
data_list = [days, hosp, icu, vent]
data_dict = dict(zip(["days", "hosp", "icu", "vent"], data_list))

projection = pd.DataFrame.from_dict(data_dict)

impact_table = (projection.iloc[::7, :]).apply(np.floor)
impact_table.index = range(impact_table.shape[0])

if st.checkbox("Show Hospital Impact Data"):
    st.dataframe(impact_table)

st.subheader("Admissions")
st.markdown("The number of new admissions")

# New cases
projection_admits = projection.iloc[:-1, :] - projection.shift(1)
projection_admits[projection_admits < 0] = 0

plot_projection_days = 50
projection_admits["days"] = range(projection_admits.shape[0])

fig, ax = plt.subplots(1, 1, figsize=(10, 4))
ax.plot(
    projection_admits.head(plot_projection_days)["hosp"], ".-", label="Hospitalized"
)
ax.plot(projection_admits.head(plot_projection_days)["icu"], ".-", label="ICU")
ax.plot(projection_admits.head(plot_projection_days)["vent"], ".-", label="Ventilated")
ax.legend(loc=0)
ax.set_xlabel("Days from today")
ax.grid("on")
ax.set_ylabel("Daily Admissions")
st.pyplot()

admits_table = projection_admits[np.mod(projection_admits.index, 7) == 0].copy()
admits_table["days"] = admits_table.index
admits_table.index = range(admits_table.shape[0])
admits_table = admits_table.fillna(0)

if st.checkbox("Show Admissions Data"):
    st.dataframe(admits_table)

st.subheader("Census")
st.markdown("Running census accounting for arrivals and discharges")

# ALOS for each category of COVID-19 case (total guesses)

los_dict = {
    "hosp": hosp_los,
    "icu": icu_los,
    "vent": vent_los,
}

fig, ax = plt.subplots(1, 1, figsize=(10, 4))

census_dict = {}
for k, los in los_dict.items():
    census = (
        projection_admits.cumsum().iloc[:-los, :]
        - projection_admits.cumsum().shift(los).fillna(0)
    ).apply(np.ceil)
    census_dict[k] = census[k]
    ax.plot(census.head(plot_projection_days)[k], ".-", label=k + " census")
    ax.legend(loc=0)

ax.set_xlabel("Days from today")
ax.grid("on")
ax.set_ylabel("Census")
st.pyplot()

census_df = pd.DataFrame(census_dict)
census_df["days"] = census_df.index
census_df = census_df[["days", "hosp", "icu", "vent"]]

census_table = census_df[np.mod(census_df.index, 7) == 0].copy()
census_table.index = range(census_table.shape[0])
census_table.loc[0, :] = 0
census_table = census_table.dropna()

if st.checkbox("Show Census Data"):
    st.dataframe(census_table)

st.markdown("""**Click the checkbox below to view the raw SIR similation data**""")
if st.checkbox("Show Infection Rate Data"):
    fig, ax = plt.subplots(1, 1, figsize=(10, 4))
    # ax.plot(s,label='S')
    ax.plot(i, label="Infected")
    ax.plot(r, label="Recovered")
    ax.legend(loc=0)
    ax.set_xlabel("days from today")
    ax.set_ylabel("Case Volume")
    ax.grid("on")
    st.pyplot()

    # Show data
    days = np.array(range(0, n_days + 1))
    data_list = [days, i, r]
    data_dict = dict(zip(["days", "infections", "recovered"], data_list))
    projection_area = pd.DataFrame.from_dict(data_dict)
    infect_table = (projection_area.iloc[::7, :]).apply(np.floor)
    infect_table.index = range(infect_table.shape[0])

    st.dataframe(infect_table)
