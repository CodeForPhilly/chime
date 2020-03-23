import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

"""
"""


class FeatureWidgets:
    def __init__(self):
        self.current_hospitalized = dcc.Input(
            id="current_hospitalized",
            min=0,
            step=1,
            type="number"

        )

        self.doubling_time = dcc.Input(
            id='doubling_time',
            min=0,
            step=1,
            type="number"
        )

        self.relative_contact_rate = dcc.Input(
            id="relative_contact_rate",
            min=0,
            max=100,
            step=5,
            type="number"
        )

        self.hospitilization_rate = dcc.Input(
            id="hospitalization_rate",
            min=0.001,
            max=100.0,
            step=1.0,
            type="number"
        )

        self.icu_rate = dcc.Input(
            id="icu_rate",
            min=0.0,
            max=100.0,
            step=1.0,
            type="number"
        )

        self.ventilated_rate = dcc.Input(
            id="ventilated_rate",
            min=0.0,
            max=100.0,
            type="number"

        )

        self.hospitalized_los = dcc.Input(
            id="hospitalized_los",
            min=0,
            step=1,
            type="number"

        )

        self.icu_los = dcc.Input(
            id="icu_los",
            min=0,
            step=1,
            type="number"

        )

        self.ventilated_los = dcc.Input(
            id="ventilated_los",
            min=0,
            step=1,
            type="number"

        )

        self.market_share = dcc.Input(
            id="market_share",
            min=0.001,
            max=100.0,
            step=1.0,
        )

        self.susceptible = dcc.Input(
            id="susceptible",
            min=1,
            step=100000,
            type="number"
        )

        self.known_infected = dcc.Input(
            id="known_infected",
            min=0,
            step=10,
            type="number"
        )

        self.widget_dict = {
            "n_hospitalized": [self.current_hospitalized],
            "doubling_time": [self.doubling_time],
            "known_infected": [self.known_infected],
            "market_share": [self.market_share],
            "relative_contact_rate": [self.relative_contact_rate],
            "susceptible": [self.susceptible],
            "hospitalized_los": [self.hospitalized_los],
            "icu_los": [self.icu_los],
            "ventilated_los": [self.ventilated_los],
        }

    def generate(self, feature: str) -> dcc.Input:
        """Returns widget for corresponding feature

        Arguments:
            feature {str} -- must be one of the keys in the widget dictionary

        Returns:
            dcc.Input -- dash core component allows for value inputs via field 
            and increments buttons
        """

        try:
            return self.widget_dict[feature].value[0]
        except KeyError:
            print("argument must correspond to an entry in the widget dictionary")
