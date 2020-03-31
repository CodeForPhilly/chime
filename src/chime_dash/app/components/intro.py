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
            infected_population_warning_str = (
                "(Warning:"
                " The number of estimated infections is greater than"
                " the total regional population."
                " Please verify the values entered in the sidebar.)"
                ""
                if model.infected > pars.population
                else ""
            )
            result = intro.format(
                total_infections=model.infected,
                current_hosp=pars.current_hospitalized,
                hosp_rate=pars.hospitalized.rate,
                S=pars.population,
                market_share=pars.market_share,
                recovery_days=pars.infectious_days,
                r_naught=model.r_naught,
                doubling_time=pars.doubling_time,
                relative_contact_rate=pars.relative_contact_rate,
                r_t=model.r_t,
                doubling_time_t=model.doubling_time_t,
                impact_statement=(
                    "halves the infections every"
                    if model.r_t < 1
                    else "reduces the doubling time to"
                ),
                daily_growth=model.daily_growth_rate * 100.0,
                daily_growth_t=model.daily_growth_rate_t * 100.0,
                infected_population_warning_str=infected_population_warning_str,
            )
        return [result]
