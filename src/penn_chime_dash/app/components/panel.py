import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from .widgets import FeatureWidgets

PANEL_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

place = FeatureWidgets()

horizontal = dbc.Row(
    [
        dbc.Col([
            html.Span(
                'Current Statistics',
                className='mr-3'
            ),
            dbc.Row([
                place.current_hospitalized,
                place.doubling_time,
                place.relative_contact_rate,
            ]),
        ]
        ),
        dbc.Col([
            html.Span(
                'Severity of Interventions',
                className='mr-3'
            ),
            place.hospitilization_rate,
            place.icu_rate,
            place.ventilated_rate,
        ]
        ),
        dbc.Col([
                html.Span(
                    'Care Duraton',
                    className='mr-3'
                ),
                place.hospitalized_los,
                place.icu_los,
                place.ventilated_los,
                ]
                ),
        dbc.Col([
                html.Span(
                    'Regional Stats',
                    className='mr-3'
                ),
                place.market_share,
                place.current_hospitalized,
                place.known_infected,

                ]
                )
    ]
)
