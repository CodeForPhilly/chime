"""App."""

import altair as alt  # type: ignore
import streamlit as st  # type: ignore

from penn_chime.presentation import (
    display_download_link,
    display_header,
    display_more_info,
    display_sidebar,
    hide_menu_style,
    write_definitions,
    write_footer,
)
from penn_chime.settings import DEFAULTS
from penn_chime.models import SimSirModel
from penn_chime.charts import (
    build_admits_chart,
    build_census_chart,
    build_descriptions,
    build_sim_sir_w_date_chart,
    build_table,
)

# This is somewhat dangerous:
# Hide the main menu with "Rerun", "run on Save", "clear cache", and "record a screencast"
# This should not be hidden in prod, but removed
# In dev, this should be shown
st.markdown(hide_menu_style, unsafe_allow_html=True)

p = display_sidebar(st, DEFAULTS)
m = SimSirModel(p)

display_header(st, m, p)

if st.checkbox("Show more info about this tool"):
    notes = "The total size of the susceptible population will be the entire catchment area for Penn Medicine entities (HUP, PAH, PMC, CCH)"
    display_more_info(st=st, model=m, parameters=p, defaults=DEFAULTS, notes=notes)

st.subheader("New Admissions")
st.markdown("Projected number of **daily** COVID-19 admissions at Penn hospitals")
admits_chart = build_admits_chart(alt=alt, admits_df=m.admits_df, max_y_axis=p.max_y_axis)
st.altair_chart(admits_chart, use_container_width=True)
st.markdown(build_descriptions(chart=admits_chart, labels=p.labels))
display_download_link(
    st,
    filename=f"{p.current_date}_projected_admits.csv",
    df=m.admits_df,
)

if st.checkbox("Show Projected Admissions in tabular form"):
    admits_modulo = 1
    if not st.checkbox("Show Daily Counts"):
        admits_modulo = 7
    table_df = build_table(
        df=m.admits_df,
        labels=p.labels,
        modulo=admits_modulo)
    st.table(table_df)


st.subheader("Admitted Patients (Census)")
st.markdown("Projected **census** of COVID-19 patients, accounting for arrivals and discharges at Penn hospitals")
census_chart = build_census_chart(alt=alt, census_df=m.census_df, max_y_axis=p.max_y_axis)
st.altair_chart(census_chart, use_container_width=True)
st.markdown(build_descriptions(chart=census_chart, labels=p.labels, suffix=" Census"))
display_download_link(
    st,
    filename=f"{p.current_date}_projected_census.csv",
    df=m.census_df,
)

if st.checkbox("Show Projected Census in tabular form"):
    census_modulo = 1
    if not st.checkbox("Show Daily Census Counts"):
        census_modulo = 7
    table_df = build_table(
        df=m.census_df,
        labels=p.labels,
        modulo=census_modulo)
    st.table(table_df)


st.subheader("Susceptible, Infected, and Recovered")
st.markdown("The number of susceptible, infected, and recovered individuals in the hospital catchment region at any given moment")
sim_sir_w_date_chart = build_sim_sir_w_date_chart(alt=alt, sim_sir_w_date_df=m.sim_sir_w_date_df)
st.altair_chart(sim_sir_w_date_chart, use_container_width=True)
display_download_link(
    st,
    filename=f"{p.current_date}_sim_sir_w_date.csv",
    df=m.sim_sir_w_date_df,
)

if st.checkbox("Show SIR Simulation in tabular form"):
    table_df = build_table(
        df=m.sim_sir_w_date_df,
        labels=p.labels)
    st.table(table_df)

write_definitions(st)
write_footer(st)
