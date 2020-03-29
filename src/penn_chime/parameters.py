"""Parameters.

Changes affecting results or their presentation should also update
`change_date`, so users can see when results have last changed
"""

from .utils import RateLos
from json import dumps, loads


class Parameters:
    """Parameters."""

    def __init__(
        self,
        *,
        current_hospitalized: int,
        doubling_time: float,
        known_infected: int,
        relative_contact_rate: float,
        susceptible: int,

        hospitalized: RateLos,
        icu: RateLos,
        ventilated: RateLos,

        as_date: bool = False,
        market_share: float = 1.0,
        max_y_axis: int = None,
        n_days: int = 60,
        recovery_days: int = 14,
    ):
        self.current_hospitalized = current_hospitalized
        self.doubling_time = doubling_time
        self.known_infected = known_infected
        self.relative_contact_rate = relative_contact_rate
        self.susceptible = susceptible

        self.hospitalized = hospitalized
        self.icu = icu
        self.ventilated = ventilated

        self.as_date = as_date
        self.market_share = market_share
        self.max_y_axis = max_y_axis
        self.n_days = n_days
        self.recovery_days = recovery_days

        self.labels = {
            "hospitalized": "Hospitalized",
            "icu": "ICU",
            "ventilated": "Ventilated",
            "day": "Day",
            "date": "Date",
            "susceptible": "Susceptible",
            "infected": "Infected",
            "recovered": "Recovered",
        }

        self.dispositions = {
            "hospitalized": hospitalized,
            "icu": icu,
            "ventilated": ventilated,
        }

    @staticmethod
    def change_date():
        """
        This reflects a date from which previously-run reports will no
        longer match current results, indicating when users should
        re-run their reports
        """
        return "March 23 2020"

    @property
    def json(self):
        return dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    @classmethod
    def from_json(cls, json):
        values = loads(json)
        result = cls(
            current_hospitalized=values["current_hospitalized"],
            doubling_time=values["doubling_time"],
            known_infected=values["known_infected"],
            relative_contact_rate=values["relative_contact_rate"],
            susceptible=values["susceptible"],
            hospitalized=RateLos(*values["hospitalized"]),
            icu=RateLos(*values["icu"]),
            ventilated=RateLos(*values["ventilated"])
        )

        for key, value in values.items():
            if result.__dict__[key] != value and key not in ["hospitalized", "icu", "ventilated", "dispositions"]:
                result.__dict__[key] = value

        return result
