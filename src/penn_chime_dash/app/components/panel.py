import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from .widgets import FeatureWidgets

# PANEL_STYLE = {
#     "position": "fixed",
#     "top": 0,
#     "left": 0,
#     "bottom": 0,
#     "width": "16rem",
#     "padding": "2rem 1rem",
#     "background-color": "#f8f9fa",
# }

place = FeatureWidgets()


horizontal = dbc.Container(dbc.Row(
    [
        dbc.Col(
            [
                html.H6("Current Statistics"),
                place.widget("current_hospitalized"),
                place.widget("relative_contact_rate"),
                place.widget("doubling_time"),
            ],
        ),
        dbc.Col(
            [
                html.H6("Outcomes (% total infected)"),
                place.widget("hospitalization_rate"),
                place.widget("icu_rate"),
                place.widget("ventilated_rate"),
            ]
        ),
        dbc.Col(
            [
                html.H6("Care Duration (days)"),
                place.widget("hospitalized_los"),
                place.widget("icu_los"),
                place.widget("ventilated_los"),
            ]
        ),
        dbc.Col(
            [
                html.H6("Regional Statistics"),
                place.widget("known_infected"),
                place.widget("susceptible"),
                place.widget("market_share")
            ],
        )
    ],

),
)
