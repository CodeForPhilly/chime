from typing import List

from dash_html_components import Div
from dash.development.base_component import ComponentMeta
from dash_core_components import Markdown

from chime_dash.app.components.base import Component


class ToolDetails(Component):
    """
    """
    localization_file = "tool-details.md"

    def get_html(self) -> List[ComponentMeta]:
        """Initializes the header dash html
        """
        return [Div(
            id="more_intro_wrapper",
            children=[Markdown(id="more_intro", dangerously_allow_html=True)]
        )]

    def build(self, model, pars):
        result = None
        if model and pars:
            tool_details = self.content
            result = tool_details.format(
                recovery_days=int(pars.doubling_time),
                doubling_time=pars.doubling_time,
                r_naught=model.r_naught,
                relative_contact_rate=pars.relative_contact_rate,
                doubling_time_t=model.doubling_time_t,
                r_t=model.r_t,
            )
        return [result]
