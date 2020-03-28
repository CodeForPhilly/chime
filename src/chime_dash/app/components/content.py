"""Initializes the  dash html
"""
from collections import OrderedDict

import dash_bootstrap_components as dbc
from chime_dash.app.components.additions import Additions
from chime_dash.app.components.base import Component, HTMLComponentError
from chime_dash.app.components.footer import Footer
from chime_dash.app.components.header import Header
from chime_dash.app.components.intro import Intro, ToolDetails
from chime_dash.app.containers.visualizations import Visualizations


class Content(Component):
    """
    """

    def __init__(self, language, defaults):
        """
        """
        super().__init__(language, defaults)
        self.components = OrderedDict(
            header=Header(language, defaults),
            intro=Intro(language, defaults),
            tool_details=ToolDetails(language, defaults),
            visualizations=Visualizations(language, defaults),
            additions=Additions(language, defaults),
            footer=Footer(language, defaults),
        )

    def get_html(self):
        """Initializes the content container dash html
        """
        content = dbc.Col(
            children=self.components["header"].html
            + self.components["intro"].html
            + self.components["tool_details"].html
            + self.components["visualizations"].html
            + self.components["additions"].html
            + self.components["footer"].html,
            width=9,
            className="ml-sm-auto p-5",
        )

        return [content]
