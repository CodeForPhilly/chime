"""Defaults."""

from .utils import RateLos


class Regions:
    """Arbitrary number of counties."""
    def __init__(self, **kwargs):
        susceptible = 0
        for key, value in kwargs.items():
            setattr(self, key, value)
            susceptible += value
        self._susceptible = susceptible

    @property
    def susceptible(self):
        return self._susceptible


class Constants:
    def __init__(
        self, *,
        current_hospitalized: int,
        doubling_time: int,
        known_infected: int,
        n_days: int,
        relative_contact_rate: int,
        region: Regions,

        hospitalized: RateLos,
        icu: RateLos,
        ventilated: RateLos,
        market_share: float = 1.0
    ):
        self.region = region
        self.known_infected = known_infected
        self.current_hospitalized = current_hospitalized
        self.doubling_time = doubling_time
        self.market_share = market_share
        self.relative_contact_rate = relative_contact_rate

        self.hospitalized = hospitalized
        self.icu = icu
        self.ventilated = ventilated
        self.n_days = n_days

    def __repr__(self) -> str:
        return f"Constants(susceptible_default: {self.region.susceptible}, known_infected: {self.known_infected})"
