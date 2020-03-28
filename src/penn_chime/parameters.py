"""Parameters.

Changes affecting results or their presentation should also update
`change_date`, so users can see when results have last changed
"""

from collections import namedtuple
from datetime import date
from typing import Optional


# (0.02, 7) is 2%, 7 days
# be sure to multiply by 100 when using as a default to the percent widgets!
RateLos = namedtuple("RateLos", ("rate", "length_of_stay"))


class Regions:
    """Arbitrary regions to sum population."""

    def __init__(self, **kwargs):
        population = 0
        for key, value in kwargs.items():
            setattr(self, key, value)
            population += value
        self.population = population


class Parameters:
    """Parameters."""

    def __init__(
        self,
        *,
        current_hospitalized: int,
        hospitalized: RateLos,
        icu: RateLos,
        known_infected: int,
        relative_contact_rate: float,
        ventilated: RateLos,

        current_date: date = date.today(),
        date_first_hospitalized: Optional[date] = None,
        doubling_time: Optional[float] = None,
        infectious_days: int = 14,
        market_share: float = 1.0,
        max_y_axis: Optional[int] = None,
        n_days: int = 60,
        population: Optional[int] = None,
        recovered: int = 0,
        region: Optional[Regions] = None,
    ):

        self.current_hospitalized = current_hospitalized
        self.known_infected = known_infected
        self.relative_contact_rate = relative_contact_rate

        self.hospitalized = hospitalized
        self.icu = icu
        self.ventilated = ventilated

        if region is not None and population is None:
            self.region = region
            self.population = region.population
        elif population is not None:
            self.region = None
            self.population = population
        else:
            raise AssertionError('Population or Regions required')

        self.current_date = current_date
        self.date_first_hospitalized = date_first_hospitalized
        self.doubling_time = doubling_time
        self.infectious_days = infectious_days
        self.market_share = market_share
        self.max_y_axis = max_y_axis
        self.n_days = n_days
        self.recovered = recovered

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
