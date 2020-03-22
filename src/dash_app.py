"""Script which launches dash app
"""
from dash import Dash
from dash.dependencies import Input, Output
from dash_core_components import Markdown, Checklist

import dash_bootstrap_components as dbc

from penn_chime.settings import DEFAULTS
from penn_chime.defaults import RateLos
from penn_chime.models import Parameters
from penn_chime.utils import build_admissions_df, build_census_df

from chime_dash.utils import (
    get_md_templates,
    get_yml_templates,
    render_yml,
)
from chime_dash.plotting import new_admissions_chart
from chime_dash.presentation import display_sidebar


EXTERNAL_STYLESHEETS = [
    "https://www1.pennmedicine.org/styles/shared/penn-medicine-header.css",
    dbc.themes.BOOTSTRAP,
]
LANGUAGE = "en"
MD_TEMPLATES = get_md_templates()
YML_TEMPLATES = get_yml_templates()


SIDEBAR_HTML, RENDER_KEYS = display_sidebar(LANGUAGE, DEFAULTS)

APP = Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)
APP.layout = dbc.Row(
    children=[
        dbc.Col(id="sidebar", children=SIDEBAR_HTML, width=4, className="mt-4",),
        dbc.Col(
            children=render_yml(YML_TEMPLATES[LANGUAGE]["header.yml"])
            + [Markdown(id="intro")]
            + render_yml(YML_TEMPLATES[LANGUAGE]["information.yml"])
            + render_yml(YML_TEMPLATES[LANGUAGE]["plots.yml"])
            + [
                Markdown(MD_TEMPLATES[LANGUAGE]["definitions.md"]),
                Markdown(MD_TEMPLATES[LANGUAGE]["footer.md"]),
            ],
            width=8,
            className="mt-4",
        ),
    ],
    className="container",
)


@APP.callback(
    # Output(component_id="intro", component_property="children"),
    Output(component_id="new-admissions-graph", component_property="figure"),
    [Input(component_id=key, component_property="value") for key in RENDER_KEYS],
)
def render_intro(*args):
    """Renders intro depending on parameter values
    """
    kwargs = {
        key: val / 100 if ("rate" in key or "share" in key) else val
        for key, val in zip(RENDER_KEYS, args)
    }
    pars = Parameters(
        current_hospitalized=kwargs["current_hospitalized"],
        doubling_time=kwargs["doubling_time"],
        known_infected=kwargs["known_infected"],
        market_share=kwargs["market_share"],
        relative_contact_rate=kwargs["relative_contact_rate"],
        susceptible=kwargs["susceptible"],
        hospitalized=RateLos(kwargs["hospitalized_rate"], kwargs["hospitalized_los"]),
        icu=RateLos(kwargs["icu_rate"], kwargs["icu_los"]),
        ventilated=RateLos(kwargs["ventilated_rate"], kwargs["ventilated_los"]),
        max_y_axis=None,
    )
    detection_prob_str = (
        "{detection_probability:.0%}".format(
            detection_probability=pars.detection_probability
        )
        if pars.detection_probability is not None
        else "unknown"
    )
    intro_md = MD_TEMPLATES[LANGUAGE]["intro.md"].format(
        total_infections=pars.infected,
        initial_infections=pars.known_infected,
        detection_prob_str=detection_prob_str,
        current_hosp=pars.current_hospitalized,
        hosp_rate=pars.hospitalized.rate,
        S=pars.susceptible,
        market_share=pars.market_share,
        recovery_days=pars.recovery_days,
        r_naught=pars.r_naught,
        doubling_time=pars.doubling_time,
        relative_contact_rate=pars.relative_contact_rate,
        r_t=pars.r_t,
        doubling_time_t=pars.doubling_time_t,
    )

    pars.n_days = 40
    projection_admits = build_admissions_df(pars.n_days, *pars.dispositions)

    as_date = False

    new_admissions_figure = new_admissions_chart(
        projection_admits, pars.n_days - 10, as_date=as_date, max_y_axis=pars.max_y_axis
    )

    return new_admissions_figure


def main():
    """Starts a dash app
    """
    APP.run_server(debug=True)


if __name__ == "__main__":
    main()
