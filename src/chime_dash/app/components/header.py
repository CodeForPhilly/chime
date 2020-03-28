"""Initializes the Penn Medicine masthead
#! consider moving this into navbar or static
"""
from typing import List

from dash.development.base_component import ComponentMeta
from dash_html_components import Div, A

from chime_dash.app.utils.components import Component


class Header(Component):
    """
    """

    localization_file = "header.yml"

    def get_html(self) -> List[ComponentMeta]:
        """Initializes the header dash html
        """
        content = self.content
        return [
            Div(
                className="penn-medicine-header__content",
                children=[

                    A(
                        className="penn-medicine-header__title",
                        id="title",
                        children=content["title"],
                    ),
                ],
            )
        ]
