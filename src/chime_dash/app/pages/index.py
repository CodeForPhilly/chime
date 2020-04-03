"""pages/index
Homepage
"""
from collections import OrderedDict

from dash_html_components import Main
from dash_bootstrap_components import Container

from chime_dash.app.components.base import Page
from chime_dash.app.components.footer import Footer
from chime_dash.app.components.header import Header
from chime_dash.app.components.intro import Intro
from chime_dash.app.components.visualizations import Visualizations
from chime_dash.app.services.callbacks import IndexCallbacks


class Index(Page):
    """
    """
    callbacks_cls = IndexCallbacks

    def __init__(self, language, defaults):
        """
        """
        super().__init__()
        self.components = OrderedDict(
            header=Header(language, defaults),
            intro=Intro(language, defaults),
            visualizations=Visualizations(language, defaults),
            footer=Footer(language, defaults),
        )

    def get_html(self):
        """Initializes the content container dash html
        """
        content = Main(
            className="py-5",
            style={
                "marginLeft": "320px",
                "marginTop": "56px"
            },
            children=[Container(
                children=self.components["header"].html
                + self.components["intro"].html
            )]
            + self.components["visualizations"].html
            + [Container(
                children=self.components["footer"].html
            )],
        )

        return [content]
