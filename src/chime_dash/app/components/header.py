"""Initializes the Penn Medicine masthead
#! consider moving this into navbar or static
"""
from typing import List

from dash.development.base_component import ComponentMeta
from dash_html_components import Div, H1
from dash_core_components import Markdown

from chime_dash.app.components.base import Component


class Header(Component):
    """
    """

    localization_file = "header.yml"

    def get_html(self) -> List[ComponentMeta]:
        """Initializes the header dash html
        """
        content = self.content
        return [Div(
            children=[
                H1(className="penn-medicine-header__title", id="title", children=content["title"]),
                Markdown(content["description"])
          ]
        )]
