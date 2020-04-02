"""Parameters.

Changes affecting results or their presentation should also update
constants.py `change_date``.
"""

from collections import namedtuple
from datetime import date
from typing import Optional

from .validators import (
    Positive, OptionalStrictlyPositive, StrictlyPositive, Rate, Date, OptionalDate
    )

# Parameters for each disposition (hospitalized, icu, ventilated)
#   The rate of disposition within the population of infected
#   The average number days a patient has such disposition

# Hospitalized:
#   2.5 percent of the infected population are hospitalized: hospitalized.rate is 0.025
#   Average hospital length of stay is 7 days: hospitalized.days = 7

# ICU:
#   0.75 percent of the infected population are in the ICU: icu.rate is 0.0075
#   Average number of days in an ICU is 9 days: icu.days = 9

# Ventilated:
#   0.5 percent of the infected population are on a ventilator: ventilated.rate is 0.005
#   Average number of days on a ventilator: ventilated.days = 10

# Be sure to multiply by 100 when using the parameter as a default to a percent widget!


Disposition = namedtuple("Disposition", ("rate", "days"))


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
        hospitalized: Disposition,
        icu: Disposition,
        relative_contact_rate: float,
        mitigation_date: Optional[date] = None,
        ventilated: Disposition,
        current_date: date = date.today(),
        date_first_hospitalized: Optional[date] = None,
        doubling_time: Optional[float] = None,
        infectious_days: int = 14,
        market_share: float = 1.0,
        max_y_axis: Optional[int] = None,
        n_days: int = 100,
        population: Optional[int] = None,
        recovered: int = 0,
        region: Optional[Regions] = None,
    ):
        self.current_hospitalized = Positive(value=current_hospitalized)

        Rate(value=hospitalized.rate), Rate(value=icu.rate), Rate(value=ventilated.rate)
        StrictlyPositive(value=hospitalized.days), StrictlyPositive(value=icu.days),
        StrictlyPositive(value=ventilated.days)

        self.hospitalized = hospitalized
        self.icu = icu
        self.ventilated = ventilated

        if region is not None and population is None:
            self.region = region
            self.population = StrictlyPositive(value=region.population)
        elif population is not None:
            self.region = None
            self.population = StrictlyPositive(value=population)
        else:
            raise AssertionError('population or regions must be provided.')

        self.current_date = Date(value=current_date)
       
        self.date_first_hospitalized = OptionalDate(value=date_first_hospitalized)
        self.doubling_time = OptionalStrictlyPositive(value=doubling_time)

        self.relative_contact_rate = Rate(value=relative_contact_rate)
        self.mitigation_date = OptionalDate(value=mitigation_date)

        self.infectious_days = StrictlyPositive(value=infectious_days)
        self.market_share = Rate(value=market_share)
        self.max_y_axis = OptionalStrictlyPositive(value=max_y_axis)
        self.n_days = StrictlyPositive(value=n_days)
        self.recovered = Positive(value=recovered)

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
