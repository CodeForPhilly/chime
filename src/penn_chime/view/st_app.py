"""App."""

import os

import altair as alt
import streamlit as st
import i18n

lang = os.environ.get('LANG') or 'en'
i18n.set('filename_format', '{locale}.{format}')
i18n.set('locale', lang)
i18n.set('fallback', 'en')
i18n.load_path.append(os.path.dirname(__file__) + '/../locales')

from ..model.parameters import Parameters
from ..model.sir import Sir
from ..model.ppe import PPE
from .charts import (
    build_admits_chart,
    build_census_chart,
    build_sim_sir_w_date_chart,
)
from .st_display import (
    display_download_link,
    display_excel_download_link,
    display_footer,
    display_header,
    display_sidebar,
    hide_menu_style,
)
from ..constants import (
    DOCS_URL,
)

def main():
    # This is somewhat dangerous:
    # Hide the main menu with "Rerun", "run on Save", "clear cache", and "record a screencast"
    # This should not be hidden in prod, but removed
    # In dev, this should be shown
    st.markdown(hide_menu_style, unsafe_allow_html=True)

    d = Parameters.create(os.environ, [])
    ppe = PPE(os.environ)

    p = display_sidebar(st, d)
    m = Sir(p)
    
    if not m.reasonable_model_parameters:
        st.subheader("Based on the current parameters, estimated pre-mitigation doubling time is greater than 15 days. Try different parameters.")
        return

    display_header(st, m, p)

    st.subheader(i18n.t("app-new-admissions-title"))
    st.markdown(i18n.t("app-new-admissions-text"))
    admits_chart = build_admits_chart(alt=alt, admits_floor_df=m.admits_floor_df, max_y_axis=p.max_y_axis, use_log_scale=p.use_log_scale)

    st.altair_chart(admits_chart, use_container_width=True)
    display_download_link(
        st,
        p,
        filename=f"{p.current_date}_projected_admits.csv",
        df=m.admits_df,
    )

    st.subheader(i18n.t("app-admitted-patients-title"))
    st.markdown(i18n.t("app-admitted-patients-text"))
    census_chart = build_census_chart(alt=alt, census_floor_df=m.census_floor_df, max_y_axis=p.max_y_axis, use_log_scale=p.use_log_scale)

    st.altair_chart(census_chart, use_container_width=True)
    display_download_link(
        st,
        p,
        filename=f"{p.current_date}_projected_census.csv",
        df=m.census_df,
    )

    st.subheader(i18n.t("app-PPE-title"))
    st.markdown(i18n.t("app-PPE-text"))
    display_excel_download_link(st, ppe.filename, ppe.src)
    st.markdown(i18n.t("app-PPE-text2"))
    display_download_link(
        st,
        p,
        filename=f"{p.current_date}_projected_census_for_ppe_calculator.csv",
        df=m.ppe_df,
    )
    st.markdown(
        i18n.t("app-PPE-documentation").format(
            link_to_docs="{docs_url}/ppe-calculator".format(docs_url=DOCS_URL),
            link_to_tutorial="{docs_url}/ppe-calculator/ppe-basic-tutorial".format(docs_url=DOCS_URL),
        ),
        unsafe_allow_html=True
    )

    st.subheader(i18n.t("app-SIR-title"))
    st.markdown(i18n.t("app-SIR-text"))
    sim_sir_w_date_chart = build_sim_sir_w_date_chart(alt=alt, sim_sir_w_date_floor_df=m.sim_sir_w_date_floor_df, use_log_scale=p.use_log_scale)

    st.altair_chart(sim_sir_w_date_chart, use_container_width=True)
    display_download_link(
        st,
        p,
        filename=f"{p.current_date}_sim_sir_w_date.csv",
        df=m.sim_sir_w_date_df,
    )
    display_footer(st)
