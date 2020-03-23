"""Initializes the  dash html
"""
from typing import List, Any

from dash.dependencies import Output
from dash.development.base_component import ComponentMeta
from dash_core_components import Markdown

from penn_chime.models import Parameters

from chime_dash.utils import read_localization_markdown

LOCALIZATION_FILE = "intro.md"


def setup(language: str) -> List[ComponentMeta]:  # pylint: disable=W0613
    """Initializes the header dash html
    """

    return [Markdown(id="intro")]


CALLBACK_OUTPUTS = [Output(component_id="intro", component_property="children")]


def render(language: str, pars: Parameters) -> List[Any]:
    """Renders the parameter dependent values in the introduction markdown
    """
    content = read_localization_markdown(LOCALIZATION_FILE, language)
    detection_prob_str = (
        "{detection_probability:.0%}".format(
            detection_probability=pars.detection_probability
        )
        if pars.detection_probability is not None
        else "?"
    )
    return (
        content.format(
            total_infections=pars.infected,
            initial_infections=pars.known_infected,
            detection_prob_str=detection_prob_str,
            current_hosp=pars.current_hospitalized,
            hosp_rate=pars.hospitalized.rate,
            S=pars.susceptible,
            market_share=pars.market_share,
            recovery_days=pars.recovery_days,
            r_naught=pars.r_naught,
            doubling_time=pars.doubling_time,
            relative_contact_rate=pars.relative_contact_rate,
            r_t=pars.r_t,
            doubling_time_t=pars.doubling_time_t,
        ),
    )
