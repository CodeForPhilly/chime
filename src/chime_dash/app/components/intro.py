"""Initializes the  dash html
"""
from typing import List, Any

from dash.dependencies import Output
from dash.development.base_component import ComponentMeta
from dash_core_components import Markdown

from penn_chime.parameters import Parameters

from chime_dash.app.utils.templates import read_localization_markdown
from chime_dash.app.components.base import Component

LOCALIZATION_FILE_1 = "intro.md"
LOCALIZATION_FILE_2 = "tool-details.md"


class Intro(Component):
    """
    """

    callback_outputs = [
        Output(component_id="intro", component_property="children"),
    ]

    def get_html(self) -> List[ComponentMeta]:  # pylint: disable=W0613
        """Initializes the header dash html
        """
        return [
            Markdown(id="intro", dangerously_allow_html=True, dedent=True),
        ]

    def callback(self, *args, **kwargs):
        """
        """
        pars = kwargs["pars"]
        intro = read_localization_markdown(LOCALIZATION_FILE_1, self.language)
        detection_prob_str = (
            "{detection_probability:.0%}".format(
                detection_probability=kwargs["model"].detection_probability
            )
            if kwargs["model"].detection_probability is not None
            else "?"
        )
        return [
            intro.format(
                total_infections=kwargs["model"].infected,
                initial_infections=pars.known_infected,
                detection_prob_str=detection_prob_str,
                current_hosp=pars.current_hospitalized,
                hosp_rate=pars.hospitalized.rate,
                S=pars.susceptible,
                market_share=pars.market_share,
                recovery_days=pars.recovery_days,
                r_naught=kwargs["model"].r_naught,
                doubling_time=kwargs["pars"].doubling_time,
                relative_contact_rate=pars.relative_contact_rate,
                r_t=kwargs["model"].r_t,
                doubling_time_t=kwargs["model"].doubling_time_t,
            )
        ]


class ToolDetails(Component):
    """
    """

    callback_outputs = [
        Output(component_id="more-intro", component_property="children"),
    ]

    def get_html(self) -> List[ComponentMeta]:  # pylint: disable=W0613
        """Initializes the header dash html
        """
        return [
            Markdown(id="more-intro", dangerously_allow_html=True),
        ]

    def callback(self, *args, **kwargs) -> List[Any]:
        """Renders the parameter dependent values in the introduction markdown
        """
        pars = kwargs["pars"]
        tool_details = read_localization_markdown(LOCALIZATION_FILE_2, self.language)
        regions = "- " + "| \n".join(
            f"{key} = {value} "
            for key, value in self.defaults.region.__dict__.items()
            if key != "_s"
        )
        return [
            tool_details.format(
                regions=regions,
                recovery_days=int(pars.doubling_time),
                doubling_time=pars.doubling_time,
                r_naught=kwargs["model"].r_naught,
                relative_contact_rate=pars.relative_contact_rate,
                doubling_time_t=kwargs["model"].doubling_time_t,
                r_t=kwargs["model"].r_t,
            )
            if kwargs["show_tool_details"]
            else ""
        ]
