"""Combines all components
"""
from dash_bootstrap_components import Row, Col
from dash_bootstrap_components.themes import BOOTSTRAP

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


def setup(language):
    """Glues individual setup components together
    """
    return Row(
        children=[
            Col(
                id="sidebar",
                # children=sidebar.setup(language),
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
