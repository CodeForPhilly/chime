#!/usr/bin/env python
import streamlit as st  # type: ignore

from constants import KNOWN_INFECTIONS, S_DEFAULT


# Widgets
def _initial_infections():
    return st.sidebar.number_input(
        "Currently Known Regional Infections", value=KNOWN_INFECTIONS, step=10, format="%i"
    )
def _current_hosp():
    return st.sidebar.number_input(
        "Currently Hospitalized COVID-19 Patients", value=2, step=1, format="%i"
    )
def _doubling_time():
    return st.sidebar.number_input(
        "Doubling Time (days)", value=6, step=1, format="%i"
    )
def _hosp_rate():
    return (
        st.sidebar.number_input("Hospitalization %", 0, 100, value=5, step=1, format="%i")
        / 100.0
    )
def _icu_rate():
    return (
        st.sidebar.number_input("ICU %", 0, 100, value=2, step=1, format="%i") / 100.0
    )
def _vent_rate():
    return (
        st.sidebar.number_input("Ventilated %", 0, 100, value=1, step=1, format="%i")
        / 100.0
    )
def _hosp_los():
    return st.sidebar.number_input("Hospital LOS", value=7, step=1, format="%i")
def _icu_los():
    return st.sidebar.number_input("ICU LOS", value=9, step=1, format="%i")
def _vent_los():
    return st.sidebar.number_input("Vent LOS", value=10, step=1, format="%i")
def _Penn_market_share():
    return (
        st.sidebar.number_input(
            "Hospital Market Share (%)", 0.0, 100.0, value=15.0, step=1.0, format="%f"
        )
        / 100.0
    )
def _S():
    return st.sidebar.number_input(
        "Regional Population", value=S_DEFAULT, step=100000, format="%i"
    )

def _total_infections(current_hosp, Penn_market_share, hosp_rate):
    return current_hosp / Penn_market_share / hosp_rate

def _detection_prob(initial_infections, current_hosp, Penn_market_share, hosp_rate):
    return initial_infections / _total_infections(current_hosp, Penn_market_share, hosp_rate)

def _los_dict(hosp_los, icu_los, vent_los):
    return {
        "hosp": hosp_los,
        "icu": icu_los,
        "vent": vent_los,
    }
