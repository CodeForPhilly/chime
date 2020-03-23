"""Combines all components
"""
from dash_bootstrap_components import Row, Col
from dash_bootstrap_components.themes import BOOTSTRAP

from penn_chime.defaults import Constants

from chime_dash.layout import sidebar
from chime_dash.layout import header
from chime_dash.layout import intro
from chime_dash.layout import additions
from chime_dash.layout import visualizations
from chime_dash.layout import definitions
from chime_dash.layout import footer


EXTERNAL_STYLESHEETS = [
    "https://www1.pennmedicine.org/styles/shared/penn-medicine-header.css",
    BOOTSTRAP,
]


def setup(language: str, defaults: Constants):
    """Glues individual setup components together
    """
    return Row(
        children=[
            Col(
                id="sidebar",
                children=sidebar.setup(language, defaults),
                width=4,
                className="mt-4",
            ),
            Col(
                children=header.setup(language) + intro.setup(language)
                # + additions.setup(language)
                # + visualizations.setup(language)
                + definitions.setup(language) + footer.setup(language),
                width=8,
                className="mt-4",
            ),
        ],
        className="container",
    )


CALLBACK_INPUTS = []
CALLBACK_OUTPUTS = []


def callback_body(*args):
    """Glues together individual app callbacks

    Sidebar provides all of the inputs.
    """
    pars, as_date = sidebar.parse_form_parameters(*args)
    return None
