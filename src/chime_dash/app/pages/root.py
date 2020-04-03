"""Combines all components

The `sidebar` component combines all the inputs while other components potentially
have callbacks.

To add or remove components, adjust the `setup`.
"""
from collections import OrderedDict

from dash_bootstrap_components.themes import BOOTSTRAP
from dash_html_components import Div
from dash_core_components import Location, Store

from chime_dash.app.components.base import Page
from chime_dash.app.components.navbar import Navbar
from chime_dash.app.pages.index import Index
from chime_dash.app.pages.sidebar import Sidebar
from chime_dash.app.utils import singleton
from chime_dash.app.services.callbacks import RootCallbacks

@singleton
class Root(Page):
    """
    """
    external_stylesheets = [
        BOOTSTRAP,
        'https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,400;0,600;1,400;1,600&display=swap',
    ]
    callbacks_cls = RootCallbacks

    def __init__(self, language, defaults):
        """
        """
        self.components = OrderedDict(
            navbar=Navbar(language, defaults),
            sidebar=Sidebar(language, defaults),
            # todo subscribe to changes to URL and select page appropriately
            index=Index(language, defaults),
        )
        super().__init__(language, defaults)

    def get_html(self):
        """Glues individual setup components together
        """
        return Div(
            className="app",
            children=self.components["navbar"].html + [
                Div(
                    className="app-content",
                    children=self.components["sidebar"].html
                             + self.components["index"].html
                ),
                Store(id="root-store"),
                Location(id='location')
            ]
        )
