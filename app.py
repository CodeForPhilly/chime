import altair as alt
import numpy as np
import streamlit as st

from penn_chime.models import get_hospitalizations, sim_sir
from penn_chime.presentation import (
    additional_projections_chart,
    admitted_patients_chart,
    display_header,
    draw_projected_admissions_table,
    draw_raw_sir_simulation_table,
    hide_menu_style,
    new_admissions_chart,
    show_additional_projections,
    show_more_info_about_this_tool,
    write_definitions,
    write_footer,
)
from penn_chime.utils import build_admissions_df, build_census_df

# TODO: Pull out constants, ideally this should come from config/env
# Constants
delaware = 564696
chester = 519293
montgomery = 826075
bucks = 628341
philly = 1581000

# TODO: These need to go into key-storage
# initial values
S_default = delaware + chester + montgomery + bucks + philly
known_infections = 91  # update daily
known_cases = 4  # update daily

# This is somewhat dangerous:
# Hide the main menu with "Rerun", "run on Save", "clear cache", and "record a screencast"
# This should not be hidden in prod, but removed
# In dev, this should be shown
st.markdown(hide_menu_style, unsafe_allow_html=True)


# Initialize variables
# these functions create input elements and bind the values they are set to
# to the variables they are set equal to
# it's kindof like ember or angular if you are familiar with those

# TODO: Refactor all the sidebar stuff into a single function/file
current_hosp = st.sidebar.number_input(
    "Currently Hospitalized COVID-19 Patients", value=known_cases, step=1, format="%i"
)

doubling_time = st.sidebar.number_input(
    "Doubling time before social distancing (days)", value=6, step=1, format="%i"
)

relative_contact_rate = (
    st.sidebar.number_input(
        "Social distancing (% reduction in social contact)",
        0,
        100,
        value=0,
        step=5,
        format="%i",
    )
    / 100.0
)

hosp_rate = (
    st.sidebar.number_input(
        "Hospitalization %(total infections)",
        0.0,
        100.0,
        value=5.0,
        step=1.0,
        format="%f",
    )
    / 100.0
)
icu_rate = (
    st.sidebar.number_input(
        "ICU %(total infections)", 0.0, 100.0, value=2.0, step=1.0, format="%f"
    )
    / 100.0
)
vent_rate = (
    st.sidebar.number_input(
        "Ventilated %(total infections)", 0.0, 100.0, value=1.0, step=1.0, format="%f"
    )
    / 100.0
)
hosp_los = st.sidebar.number_input(
    "Hospital Length of Stay", value=7, step=1, format="%i"
)
icu_los = st.sidebar.number_input("ICU Length of Stay", value=9, step=1, format="%i")
vent_los = st.sidebar.number_input("Vent Length of Stay", value=10, step=1, format="%i")
market_share = (
    st.sidebar.number_input(
        "Hospital Market Share (%)", 0.0, 100.0, value=15.0, step=1.0, format="%f"
    )
    / 100.0
)
S = st.sidebar.number_input(
    "Regional Population", value=S_default, step=100000, format="%i"
)

initial_infections = st.sidebar.number_input(
    "Currently Known Regional Infections (only used to compute detection rate - does not change projections)",
    value=known_infections,
    step=10,
    format="%i",
)
# END combination input element creation and data binding


# Now, derive other variable values from the inputs created above
hospitalization_rates = (hosp_rate, icu_rate, vent_rate)

total_infections = current_hosp / market_share / hosp_rate
detection_prob = initial_infections / total_infections

# TODO: Pull out the rest of this math code into models.py
# S := Susceptible, able to be infected
# I := Infected, currently infected with the virus
# R := Recovered, no longer infected with the virus
S, I, R = S, total_infections, 0

intrinsic_growth_rate = 2 ** (1 / doubling_time) - 1

# @TODO make this configurable, or more nuanced
recovery_days = 14.0

gamma = 1 / recovery_days  # mean recovery rate, in 1/days

# Contact rate, beta
beta = (
    (intrinsic_growth_rate + gamma) / S * (1 - relative_contact_rate)
)  # {rate based on doubling time} / {initial S}

r_t = beta / gamma * S  # r_t is r_0 after distancing
r_naught = r_t / (1 - relative_contact_rate)
doubling_time_t = 1 / np.log2(beta * S - gamma + 1)  # doubling time after distancing

beta_decay = 0.0


# PRESENTATION
display_header(
    st,
    total_infections=total_infections,
    initial_infections=initial_infections,
    detection_prob=detection_prob,
    current_hosp=current_hosp,
    hosp_rate=hosp_rate,
    S=S,
    market_share=market_share,
    recovery_days=recovery_days,
    r_naught=r_naught,
    doubling_time=doubling_time,
    relative_contact_rate=relative_contact_rate,
    r_t=r_t,
    doubling_time_t=doubling_time_t,
)
if st.checkbox("Show more info about this tool"):
    show_more_info_about_this_tool(
        st=st,
        recovery_days=recovery_days,
        doubling_time=doubling_time,
        r_naught=r_naught,
        relative_contact_rate=relative_contact_rate,
        doubling_time_t=doubling_time_t,
        r_t=r_t,
        delaware=delaware,
        chester=chester,
        montgomery=montgomery,
        bucks=bucks,
        philly=philly,
    )

# PRESENTATION
# One more combination variable initialization / input element creation
n_days = st.slider("Number of days to project", 30, 200, 60, 1, "%i")

# derive more variables
# predict future values, n_days out
s, i, r = sim_sir(S, I, R, beta, gamma, n_days, beta_decay=beta_decay)
hosp, icu, vent = get_hospitalizations(i, hospitalization_rates, market_share)

# format data
projection_admits = build_admissions_df(n_days, hosp, icu, vent)
census_table = build_census_df(projection_admits, hosp_los, icu_los, vent_los)

# PRESENTATION
st.subheader("New Admissions")
st.markdown("Projected number of **daily** COVID-19 admissions at Penn hospitals")
st.altair_chart(
    new_admissions_chart(alt, projection_admits, n_days - 10), use_container_width=True,
)
if st.checkbox("Show Projected Admissions in tabular form"):
    draw_projected_admissions_table(st, projection_admits)
st.subheader("Admitted Patients (Census)")
st.markdown(
    "Projected **census** of COVID-19 patients, accounting for arrivals and discharges at Penn hospitals"
)
st.altair_chart(admitted_patients_chart(alt, census_table), use_container_width=True)
if st.checkbox("Show Projected Census in tabular form"):
    st.table(census_table)
st.markdown(
    """**Click the checkbox below to view additional data generated by this simulation**"""
)
if st.checkbox("Show Additional Projections"):
    show_additional_projections(st, alt, additional_projections_chart, i, r)
    if st.checkbox("Show Raw SIR Simulation Data"):
        draw_raw_sir_simulation_table(st, n_days, s, i, r)
write_definitions(st)
write_footer(st)
