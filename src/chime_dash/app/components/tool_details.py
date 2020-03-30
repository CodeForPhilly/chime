from typing import List
from collections import OrderedDict

from dash_html_components import Div
from dash.development.base_component import ComponentMeta
from dash_core_components import Markdown

from chime_dash.app.utils.callbacks import ChimeCallback
from chime_dash.app.utils.templates import read_localization_markdown
from chime_dash.app.components.base import Component

from penn_chime.models import SimSirModel
from penn_chime.parameters import Parameters


class ToolDetails(Component):
    """
    """
    @staticmethod
    def toggle_show_hide(show_additional_projections):
        return [not show_additional_projections]

    @staticmethod
    def update_tool_details(model_json, pars_json, region, language):
        result = None
        if model_json and pars_json:
            model = SimSirModel.from_json(model_json)
            pars = Parameters.from_json(pars_json)
            tool_details = read_localization_markdown("tool-details.md", language)
            regions = "- " + "| \n".join(
                f"{key} = {value} "
                for key, value in region.__dict__.items()
                if key != "_s"
            )
            result = tool_details.format(
                regions=regions,
                recovery_days=int(pars.doubling_time),
                doubling_time=pars.doubling_time,
                r_naught=model.r_naught,
                relative_contact_rate=pars.relative_contact_rate,
                doubling_time_t=model.doubling_time_t,
                r_t=model.r_t,
            )
        return [result]

    def __init__(self, language, defaults):
        def update_tool_details_helper(model_json, pars_json):
            return ToolDetails.update_tool_details(model_json, pars_json, defaults.region, language)
        super().__init__(language, defaults, [
            ChimeCallback(  # If user toggles show_additional_projections, show/hide the additions content
                changed_elements=OrderedDict(show_tool_details="value"),
                dom_updates=OrderedDict(more_intro_wrapper="hidden"),
                callback_fn=ToolDetails.toggle_show_hide
            ),
            ChimeCallback(  # If the parameters or model change, update the text
                changed_elements=OrderedDict(model="children", pars="children"),
                dom_updates=OrderedDict(more_intro="children"),
                callback_fn=update_tool_details_helper
            )
        ])

    def get_html(self) -> List[ComponentMeta]:
        """Initializes the header dash html
        """
        return [Div(
            id="more_intro_wrapper",
            children=[Markdown(id="more_intro", dangerously_allow_html=True)]
        )]
