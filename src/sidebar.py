#!/usr/bin/env python
import streamlit as st  # type: ignore

from constants import KNOWN_INFECTIONS, S_DEFAULT


# Widgets
initial_infections = st.sidebar.number_input(
    "Currently Known Regional Infections", value=KNOWN_INFECTIONS, step=10, format="%i"
)
current_hosp = st.sidebar.number_input(
    "Currently Hospitalized COVID-19 Patients", value=2, step=1, format="%i"
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
hosp_los = st.sidebar.number_input("Hospital LOS", value=7, step=1, format="%i")
icu_los = st.sidebar.number_input("ICU LOS", value=9, step=1, format="%i")
vent_los = st.sidebar.number_input("Vent LOS", value=10, step=1, format="%i")
Penn_market_share = (
    st.sidebar.number_input(
        "Hospital Market Share (%)", 0.0, 100.0, value=15.0, step=1.0, format="%f"
    )
    / 100.0
)
S = st.sidebar.number_input(
    "Regional Population", value=S_DEFAULT, step=100000, format="%i"
)

total_infections = current_hosp / Penn_market_share / hosp_rate
detection_prob = initial_infections / total_infections

los_dict = {
    "hosp": hosp_los,
    "icu": icu_los,
    "vent": vent_los,
}
