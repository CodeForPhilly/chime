"""components/intro
initializes the leading text as of right now

currently both classes handle control and view this should be separated
with the logic for dynamic text moving to services.
"""
from typing import List

from dash.development.base_component import ComponentMeta
from dash_core_components import Markdown

from chime_dash.app.components.base import Component


class Intro(Component):
    """
    """
    localization_file = "intro.md"

    def get_html(self) -> List[ComponentMeta]:  # pylint: disable=W0613
        """Initializes the header dash html
        """
        return [Markdown(id="intro", dangerously_allow_html=True, dedent=True)]

    def build(self, model, pars):
        result = None
        if model and pars:
            intro = self.content
            detection_prob_str = (
                "{detection_probability:.0%}".format(detection_probability=model.detection_probability)
                if model.detection_probability is not None else "?"
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
