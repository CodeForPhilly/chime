"""Builds the root component
"""
from collections import OrderedDict

from dash_bootstrap_components import Container, Row
from dash_bootstrap_components.themes import BOOTSTRAP
from dash_html_components import Div

from chime_dash.app.components.base import Component
from chime_dash.app.components.navbar import Navbar
from chime_dash.app.pages.index import Index
from chime_dash.app.pages.sidebar import Sidebar


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return get_instance


@singleton
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
        return Div(children=
                   self.components["navbar"].html
                   + [Container(
                       children=Row(self.components["sidebar"].html + [Div(
                           id="page-wrapper",
                           children=self.components["index"].html
                       )]),
                       fluid=True,
                       className="mt-5",
                   )])
