"""components/additions
currently handles both view and logic should be separated
graph activated via "Show additional projections"
"""
from typing import List

from dash.development.base_component import ComponentMeta
from dash_html_components import H4, Div
from dash_core_components import Graph

from chime_dash.app.components.base import Component


class Additions(Component):
    """
    """

    localization_file = "additions.yml"

    def get_html(self) -> List[ComponentMeta]:
        """Initializes the header dash html
        """
        return [Div(
            id="additions",
            children=[
                H4(self.content["infected-v-revovered-title"]),
                Graph(id="infected_v_revovered_graph"),
                Div(id="infected_v_revovered_table")
            ]
        )]
