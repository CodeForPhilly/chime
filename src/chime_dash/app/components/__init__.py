"""Combines all components

The `sidbar` component cobines all the inputs while other components potentially
have callbacks.

To add or remove components, adjust the `setup`.
If callbacks are present, also adjust `CALLBACK_INPUTS`, `CALLBACK_OUTPUTS` and
`callback_body`.
"""
from dash_bootstrap_components import Row, Col
from dash_bootstrap_components.themes import BOOTSTRAP

from dash_html_components import Script

from penn_chime.defaults import Constants

from chime_dash.app.components import sidebar
from chime_dash.app.components import header
from chime_dash.app.components import intro
from chime_dash.app.components import additions
from chime_dash.app.components import visualizations
from chime_dash.app.components import definitions
from chime_dash.app.components import footer


EXTERNAL_STYLESHEETS = [
    "https://www1.pennmedicine.org/styles/shared/penn-medicine-header.css",
    BOOTSTRAP,
]
EXTERNAL_SCRIPTS = []


def setup(language: str, defaults: Constants):
    """Glues individual setup components together
    """
    return Row(
        children=[
            Col(
                id="sidebar",
                children=sidebar.setup(language, defaults),
                width=3,
                className="mt-4",
            ),
            Col(width=1),
            Col(
                children=header.setup(language)
                + intro.setup(language)
                + visualizations.setup(language)
                + additions.setup(language)
                + definitions.setup(language)
                + footer.setup(language),
                width=8,
                className="mt-4",
            ),
        ],
        className="container",
    )


CALLBACK_INPUTS = sidebar.CALLBACK_INPUTS
CALLBACK_OUTPUTS = (
    intro.CALLBACK_OUTPUTS
    + visualizations.CALLBACK_OUTPUTS
    + additions.CALLBACK_OUTPUTS
)


def callback_body(*args, language="en", defaults: Constants):
    """Glues together individual app callbacks

    Sidebar provides all of the inputs.
    """
    pars, kwargs = sidebar.parse_form_parameters(*args)

    intro_md = intro.render(language, pars, kwargs, defaults)
    visualizations_data = visualizations.render(
        language, pars, as_date=kwargs["as_date"], show_tables=kwargs["show_tables"]
    )
    additions_data = additions.render(
        language,
        pars,
        as_date=kwargs["as_date"],
        show_tables=kwargs["show_tables"],
        show_additions=kwargs["show_additional_projections"],
    )
    return intro_md + visualizations_data + additions_data
