"""components/intro
initializes the leading text as of right now

currently both classes handle control and view this should be separated
with the logic for dynamic text moving to services.
"""
from typing import List, Any

from dash.dependencies import Output
from dash.development.base_component import ComponentMeta
from dash_core_components import Markdown

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
        intro = read_localization_markdown(LOCALIZATION_FILE_1, self.language)
        infected_population_warning_str = (
            "(Warning:"
            " The number of estimated infections is greater than"
            " the total regional population."
            " Please verify the values entered in the sidebar.)"
            ""
            if kwargs["model"].infected > kwargs["pars"].population
            else ""
        )
        return [
            intro.format(
                total_infections=kwargs["model"].infected,
                current_hosp=kwargs["pars"].current_hospitalized,
                hosp_rate=kwargs["pars"].hospitalized.rate,
                S=kwargs["pars"].population,
                market_share=kwargs["pars"].market_share,
                recovery_days=kwargs["pars"].infectious_days,
                r_naught=kwargs["model"].r_naught,
                doubling_time=kwargs["pars"].doubling_time,
                relative_contact_rate=kwargs["pars"].relative_contact_rate,
                r_t=kwargs["model"].r_t,
                doubling_time_t=abs(kwargs["model"].doubling_time_t),
                impact_statement=(
                    "halves the infections every"
                    if kwargs["model"].r_t < 1
                    else "reduces the doubling time to"
                ),
                daily_growth=kwargs["model"].daily_growth_rate * 100.0,
                daily_growth_t=kwargs["model"].daily_growth_rate_t * 100.0,
                infected_population_warning_str=infected_population_warning_str,
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
        tool_details = read_localization_markdown(LOCALIZATION_FILE_2, self.language)
        return [
            tool_details.format(
                recovery_days=int(kwargs["pars"].doubling_time),
                doubling_time=kwargs["pars"].doubling_time,
                r_naught=kwargs["model"].r_naught,
                relative_contact_rate=kwargs["pars"].relative_contact_rate,
                doubling_time_t=kwargs["model"].doubling_time_t,
                r_t=kwargs["model"].r_t,
            )
            if kwargs["show_tool_details"]
            else ""
        ]
