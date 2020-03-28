"""Builds the root component
"""
from collections import OrderedDict

import dash_html_components as dhc
from chime_dash.app.components.base import Component, HTMLComponentError
from dash_bootstrap_components.themes import BOOTSTRAP
from chime_dash.app.components.navbar import Navbar
from chime_dash.app.components.container import Container
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
            container=Container(language, defaults),
        )

    def get_html(self):
        """Glues individual setup components together
        """
        return dhc.Div(self.components["navbar"].html + self.components["container"].html)


root = Body(LANGUAGE, DEFAULTS)
