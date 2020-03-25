"""Combines all components

The `sidebar` component combines all the inputs while other components potentially
have callbacks.

To add or remove components, adjust the `setup`.
If callbacks are present, also adjust `CALLBACK_INPUTS`, `CALLBACK_OUTPUTS` and
`callback_body`.
"""
from collections import OrderedDict

from dash_bootstrap_components import Row, Col
from dash_bootstrap_components.themes import BOOTSTRAP
from dash_html_components import Script, Div

from penn_chime.defaults import Constants
from penn_chime.models import SimSirModel


from chime_dash.app.components.base import Component, HTMLComponentError
from chime_dash.app.components.sidebar import Sidebar
from chime_dash.app.components.header import Header
from chime_dash.app.components.intro import Intro, ToolDetails
from chime_dash.app.components.additions import Additions
from chime_dash.app.components.visualizations import Visualizations
from chime_dash.app.components.definitions import Definitions
from chime_dash.app.components.footer import Footer
from chime_dash.app.components.navbar import Navbar


class Body(Component):
    """
    """

    external_stylesheets = [
        "https://www1.pennmedicine.org/styles/shared/penn-medicine-header.css",
        BOOTSTRAP,
    ]

    def __init__(self, language, defaults):
        """
        """
        super().__init__(language, defaults)
        self.components = OrderedDict(
            sidebar=Sidebar(language, defaults),
            header=Header(language, defaults),
            intro=Intro(language, defaults),
            tool_details=ToolDetails(language, defaults),
            visualizations=Visualizations(language, defaults),
            additions=Additions(language, defaults),
            definitions=Definitions(language, defaults),
            footer=Footer(language, defaults),
            navbar=Navbar(language, defaults),
        )
        self.callback_outputs = []
        self.callback_inputs = OrderedDict()
        self.callback_keys = []
        for component in self.components.values():
            self.callback_outputs += component.callback_outputs
            self.callback_inputs.update(component.callback_inputs)

    def get_html(self):
        """Glues individual setup components together
        """
        return Div(
            children=self.components["navbar"].html
            + [
                Row(
                    children=[
                        Col(
                            id="sidebar",
                            children=self.components["sidebar"].html,
                            width=3,
                            className="mt-4",
                        ),
                        Col(width=1),
                        Col(
                            self.components["header"].html
                            + self.components["intro"].html
                            + self.components["tool_details"].html
                            + self.components["visualizations"].html
                            + self.components["additions"].html
                            + self.components["definitions"].html
                            + self.components["footer"].html,
                            width=8,
                            className="mt-4",
                        ),
                    ],
                    className="container",
                ),
            ]
        )

    def callback(self, *args, **kwargs):
        """
        """
        kwargs = dict(zip(self.callback_inputs, args))
        pars = self.components["sidebar"].parse_form_parameters(**kwargs)
        kwargs["model"] = SimSirModel(pars)
        kwargs["pars"] = pars

        callback_returns = []
        for component in self.components.values():
            try:
                callback_returns += component.callback(**kwargs)
            except Exception as error:
                raise HTMLComponentError(component, error)

        return callback_returns
