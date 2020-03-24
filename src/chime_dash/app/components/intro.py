"""Initializes the  dash html
"""
from typing import List, Any, Dict

from dash.dependencies import Output
from dash.development.base_component import ComponentMeta
from dash_core_components import Markdown

from penn_chime.defaults import Constants
from penn_chime.parameters import Parameters

from chime_dash.app.utils import read_localization_markdown

LOCALIZATION_FILE_1 = "intro.md"
LOCALIZATION_FILE_2 = "tool-details.md"


def setup(language: str) -> List[ComponentMeta]:  # pylint: disable=W0613
    """Initializes the header dash html
    """

    return [
        Markdown(id="intro", dangerously_allow_html=True, dedent=True),
        Markdown(id="more-intro", dangerously_allow_html=True),
    ]


CALLBACK_OUTPUTS = [
    Output(component_id="intro", component_property="children"),
    Output(component_id="more-intro", component_property="children"),
]


def render(
    language: str, pars: Parameters, kwargs: Dict[str, Any], defaults: Constants
) -> List[Any]:
    """Renders the parameter dependent values in the introduction markdown
    """
    intro = read_localization_markdown(LOCALIZATION_FILE_1, language)
    tool_details = read_localization_markdown(LOCALIZATION_FILE_2, language)
    detection_prob_str = (
        "{detection_probability:.0%}".format(
            detection_probability=pars.detection_probability
        )
        if pars.detection_probability is not None
        else "?"
    )

    intro_kwargs = dict(
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
    )

    regions = "- " + "| \n".join(
        f"{key} = {value} "
        for key, value in defaults.region.__dict__.items()
        if key != "_s"
    )
    tool_kwargs = dict(
        regions=regions,
        recovery_days=int(pars.doubling_time),
        doubling_time=pars.doubling_time,
        r_naught=pars.r_naught,
        relative_contact_rate=pars.relative_contact_rate,
        doubling_time_t=pars.doubling_time_t,
        r_t=pars.r_t,
    )

    return (
        intro.format(**intro_kwargs),
        tool_details.format(**tool_kwargs) if kwargs["show_tool_details"] else "",
    )
