import altair as alt
import streamlit as st

from penn_chime.defaults import RateLos
from penn_chime.models import Parameters
from penn_chime.presentation import (
    additional_projections_chart,
    admitted_patients_chart,
    display_header,
    draw_census_table,
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
from penn_chime.settings import DEFAULTS


# This is somewhat dangerous:
# Hide the main menu with "Rerun", "run on Save", "clear cache", and "record a screencast"
# This should not be hidden in prod, but removed
# In dev, this should be shown
st.markdown(hide_menu_style, unsafe_allow_html=True)


def display_sidebar(st, d) -> Parameters:
    # Initialize variables
    # these functions create input elements and bind the values they are set to
    # to the variables they are set equal to
    # it's kindof like ember or angular if you are familiar with those

    if d.known_infected < 1:
        raise ValueError("Known cases must be larger than one to enable predictions.")

    current_hospitalized = st.sidebar.number_input(
        "Currently Hospitalized COVID-19 Patients",
        min_value=0,
        value=d.current_hospitalized,
        step=1,
        format="%i"
    )

    doubling_time = st.sidebar.number_input(
        "Doubling time before social distancing (days)",
        min_value=0,
        value=d.doubling_time,
        step=1,
        format="%i"
    )

    relative_contact_rate = (
        st.sidebar.number_input(
            "Social distancing (% reduction in social contact)",
            min_value=0,
            max_value=100,
            value=d.relative_contact_rate * 100,
            step=5,
            format="%i",
        )
        / 100.0
    )

    hospitalized_rate = (
        st.sidebar.number_input(
            "Hospitalization %(total infections)",
            min_value=0.001,
            max_value=100.0,
            value=d.hospitalized.rate * 100,
            step=1.0, format="%f",
        )
        / 100.0
    )
    icu_rate = (
        st.sidebar.number_input(
            "ICU %(total infections)",
            min_value=0.0,
            max_value=100.0,
            value=d.icu.rate * 100,
            step=1.0,
            format="%f"
        )
        / 100.0
    )
    ventilated_rate = (
        st.sidebar.number_input(
            "Ventilated %(total infections)",
            min_value=0.0,
            max_value=100.0,
            value=d.ventilated.rate * 100,
            step=1.0,
            format="%f"
        )
        / 100.0
    )

    hospitalized_los = st.sidebar.number_input(
        "Hospital Length of Stay",
        min_value=0,
        value=d.hospitalized.length_of_stay,
        step=1,
        format="%i",
    )
    icu_los = st.sidebar.number_input(
        "ICU Length of Stay",
        min_value=0,
        value=d.icu.length_of_stay,
        step=1,
        format="%i",
    )
    ventilated_los = st.sidebar.number_input(
        "Vent Length of Stay",
        min_value=0,
        value=d.ventilated.length_of_stay,
        step=1,
        format="%i",
    )

    market_share = (
        st.sidebar.number_input(
            "Hospital Market Share (%)",
            min_value=0.001,
            max_value=100.0,
            value=d.market_share * 100,
            step=1.0,
            format="%f"
        )
        / 100.0
    )
    susceptible = st.sidebar.number_input(
        "Regional Population",
        min_value=1,
        value=d.region.susceptible,
        step=100000,
        format="%i"
    )

    known_infected = st.sidebar.number_input(
        "Currently Known Regional Infections (only used to compute detection rate - does not change projections)",
        min_value=0,
        value=d.known_infected,
        step=10,
        format="%i",
    )

    return Parameters(
        current_hospitalized=current_hospitalized,
        doubling_time=doubling_time,
        known_infected=known_infected,
        market_share=market_share,
        relative_contact_rate=relative_contact_rate,
        susceptible=susceptible,

        hospitalized=RateLos(hospitalized_rate, hospitalized_los),
        icu=RateLos(icu_rate, icu_los),
        ventilated=RateLos(ventilated_rate, ventilated_los)
    )


p = display_sidebar(st, DEFAULTS)

# PRESENTATION
display_header(
    st,
    total_infections=p.infected,
    initial_infections=p.known_infected,
    detection_prob=p.detection_probability,
    current_hosp=p.current_hospitalized,
    hosp_rate=p.hospitalized.rate,
    S=p.susceptible,
    market_share=p.market_share,
    recovery_days=p.recovery_days,
    r_naught=p.r_naught,
    doubling_time=p.doubling_time,
    relative_contact_rate=p.relative_contact_rate,
    r_t=p.r_t,
    doubling_time_t=p.doubling_time_t,
)
if st.checkbox("Show more info about this tool"):
    notes = "The total size of the susceptible population will be the entire catchment area for Penn Medicine entities (HUP, PAH, PMC, CCH)"
    show_more_info_about_this_tool(
        st=st,
        recovery_days=p.recovery_days,
        doubling_time=p.doubling_time,
        r_naught=p.r_naught,
        relative_contact_rate=p.relative_contact_rate,
        doubling_time_t=p.doubling_time_t,
        r_t=p.r_t,
        inputs=DEFAULTS,
        notes=notes

    )

# PRESENTATION
# One more combination variable initialization / input element creation
p.n_days = st.slider(
    "Number of days to project",
    min_value=30,
    max_value=200,
    value=DEFAULTS.n_days,
    step=1,
    format="%i"
)

# format data
projection_admits = build_admissions_df(p.n_days, *p.dispositions)
census_df = build_census_df(projection_admits, *p.lengths_of_stay)

# PRESENTATION
st.subheader("New Admissions")
st.markdown("Projected number of **daily** COVID-19 admissions at Penn hospitals")
st.altair_chart(
    new_admissions_chart(alt, projection_admits, p.n_days - 10), use_container_width=True,
)
if st.checkbox("Show Projected Admissions in tabular form"):
    draw_projected_admissions_table(st, projection_admits)
st.subheader("Admitted Patients (Census)")
st.markdown(
    "Projected **census** of COVID-19 patients, accounting for arrivals and discharges at Penn hospitals"
)
st.altair_chart(admitted_patients_chart(alt, census_df, p.n_days - 10), use_container_width=True)
if st.checkbox("Show Projected Census in tabular form"):
    draw_census_table(st, census_df)
st.markdown(
    """**Click the checkbox below to view additional data generated by this simulation**"""
)
if st.checkbox("Show Additional Projections"):
    show_additional_projections(st, alt, additional_projections_chart, p.infected_v, p.recovered_v)
    if st.checkbox("Show Raw SIR Simulation Data"):
        draw_raw_sir_simulation_table(st, p.n_days, p.susceptible_v, p.infected_v, p.recovered_v)
write_definitions(st)
write_footer(st)
