import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

"""
"""


class FeatureWidgets:
    def __init__(self):
        self.current_hospitalized = dbc.Input(
            id="current_hospitalized",
            min=0,
            step=1,
            type="number",
            placeholder="Currently Hospitalized COVID-19 Patients"

        )

        self.doubling_time = dbc.Input(
            id='doubling_time',
            min=0,
            step=1,
            type="number",
            placeholder="Doubling time before social distancing (days)"
        )

        self.relative_contact_rate = dbc.Input(
            id="relative_contact_rate",
            min=0,
            max=100,
            step=5,
            type="number",
            placeholder="Social distancing % (reduction in social contact)"
        )

        self.hospitilized_rate = dbc.Input(
            id="hospitaliz_rate",
            min=0.001,
            max=100.0,
            step=1.0,
            type="number",
            placeholder="Hospitalization % (total infections)"
        )

        self.icu_rate = dbc.Input(
            id="icu_rate",
            min=0.0,
            max=100.0,
            step=1.0,
            type="number",
            placeholder="ICU %(total infections)"
        )

        self.ventilated_rate = dbc.Input(
            id="ventilated_rate",
            min=0.0,
            max=100.0,
            type="number",
            placeholder="Ventilated %(total infections)"

        )

        self.hospitalized_los = dbc.Input(
            id="hospitalized_los",
            min=0,
            step=1,
            type="number",
            placeholder="Hospital Length of Stay"

        )

        self.icu_los = dbc.Input(
            id="icu_los",
            min=0,
            step=1,
            type="number",
            placeholder="ICU Length of Stay"

        )

        self.ventilated_los = dbc.Input(
            id="ventilated_los",
            min=0,
            step=1,
            type="number",
            placeholder="Ventilated Length of Stay"

        )

        self.market_share = dbc.Input(
            id="market_share",
            min=0.001,
            max=100.0,
            step=1.0,
            placeholder="Hospital Market Share (%)"
        )

        self.susceptible = dbc.Input(
            id="susceptible",
            min=1,
            step=100000,
            type="number",
            placeholder="Regional Population"
        )

        self.known_infected = dbc.Input(
            id="known_infected",
            min=0,
            step=10,
            type="number",
            placeholder="Currently Known Regionally Infected"
        )

        self.widget_dict = {
            "current_hospitalized": [self.current_hospitalized],
            "relative_contact_rate": [self.relative_contact_rate],
            "doubling_time": [self.doubling_time],
            "known_infected": [self.known_infected],
            "market_share": [self.market_share],
            "susceptible": [self.susceptible],
            "hospitalized_los": [self.hospitalized_los],
            "icu_los": [self.icu_los],
            "ventilated_los": [self.ventilated_los],
            "ventilated_rate": [self.ventilated_rate],
            "hostpitalized_rate": [self.hospitilized_rate],
            "icu_rate": [self.icu_rate]
        }

    def widget(self, feature: str) -> dcc.Input:
        """Returns widget for corresponding feature

        Arguments:
            feature {str} -- must be one of the keys in the widget dictionary

        Returns:
            dcc.Input -- dash core component allows for value inputs via field 
            and increments buttons
        """

        try:
            return self.widget_dict[feature][0]
        except KeyError:
            print("argument must correspond to an entry in the widget dictionary")
