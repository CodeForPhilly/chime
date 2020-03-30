"""components/intro
initializes the leading text as of right now

currently both classes handle control and view this should be separated
with the logic for dynamic text moving to services.
"""
from typing import List
from collections import OrderedDict

from dash.dependencies import Output
from dash.development.base_component import ComponentMeta
from dash_core_components import Markdown

from chime_dash.app.utils.callbacks import ChimeCallback
from chime_dash.app.utils.templates import read_localization_markdown
from chime_dash.app.components.base import Component

from penn_chime.models import SimSirModel
from penn_chime.parameters import Parameters


class Intro(Component):
    """
    """

    callback_outputs = [
        Output(component_id="intro", component_property="children"),
    ]

    @staticmethod
    def update_intro(model_json, pars_json, language):
        result = None
        if model_json and pars_json:
            model = SimSirModel.from_json(model_json)
            pars = Parameters.from_json(pars_json)
            intro = read_localization_markdown("intro.md", language)
            detection_prob_str = (
                "{detection_probability:.0%}".format(
                    detection_probability=model.detection_probability
                )
                if model.detection_probability is not None
                else "?"
            )
            result = intro.format(
                total_infections=model.infected,
                initial_infections=pars.known_infected,
                detection_prob_str=detection_prob_str,
                current_hosp=pars.current_hospitalized,
                hosp_rate=pars.hospitalized.rate,
                S=pars.susceptible,
                market_share=pars.market_share,
                recovery_days=pars.recovery_days,
                r_naught=model.r_naught,
                doubling_time=pars.doubling_time,
                relative_contact_rate=pars.relative_contact_rate,
                r_t=model.r_t,
                doubling_time_t=model.doubling_time_t,
            )
        return [result]

    def __init__(self, language, defaults):
        def update_intro_helper(model_json, pars_json):
            return Intro.update_intro(model_json, pars_json, language)
        super().__init__(language, defaults, [
            ChimeCallback(  # If the parameters or model change, update the text
                changed_elements=OrderedDict(model="children", pars="children"),
                dom_updates=OrderedDict(intro="children"),
                callback_fn=update_intro_helper
            )
        ])

    def get_html(self) -> List[ComponentMeta]:  # pylint: disable=W0613
        """Initializes the header dash html
        """
        return [Markdown(id="intro", dangerously_allow_html=True, dedent=True)]
