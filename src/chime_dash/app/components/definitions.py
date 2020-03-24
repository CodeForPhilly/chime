"""Initializes the  dash html
"""
from typing import List

from dash.development.base_component import ComponentMeta

from dash_core_components import Markdown

from chime_dash.app.components.base import Component


class Definitions(Component):
    """
    """

    localization_file = "definitions.md"

    def get_html(self) -> List[ComponentMeta]:
        """Initializes the header dash html
        """

        return [Markdown(self.content)]
