"""Builds the root component
"""
from collections import OrderedDict

import dash_bootstrap_components as dbc
import dash_html_components as dhc
from chime_dash.app.components.base import Component
from chime_dash.app.components.navbar import Navbar
from chime_dash.app.pages.sidebar import Sidebar
from chime_dash.app.pages.index import Index
from dash_bootstrap_components.themes import BOOTSTRAP
from penn_chime.settings import DEFAULTS

LANGUAGE = "en"


class Body(Component):
    """
    """

    external_stylesheets = [
        BOOTSTRAP,
    ]

    def __init__(self, language, defaults):
        """
        """
        super().__init__(language, defaults)
        self.components = OrderedDict(
            navbar=Navbar(language, defaults),
            sidebar=Sidebar(language, defaults),
            # todo subscribe to changes to URL and select page appropriately
            index=Index(language, defaults),
        )

    def get_html(self):
        """Glues individual setup components together
        """
        return dhc.Div(children=
                       self.components["navbar"].html
                       + [dbc.Container(
                           children=dbc.Row(self.components["sidebar"].html + [dhc.Div(
                               id="page-wrapper",
                               children=self.components["index"].html
                           )]),
                           fluid=True,
                           className="mt-5",
                       )])


root = Body(LANGUAGE, DEFAULTS)
