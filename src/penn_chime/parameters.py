"""Parameters."""

from .utils import RateLos


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

        market_share: float = 1.0,
        max_y_axis: int = None,
        n_days: int = 0,
        recovery_days: int = 14,
    ):
        """
        __init__.
        """
        self.current_hospitalized = current_hospitalized
        self.doubling_time = doubling_time
        self.known_infected = known_infected
        self.relative_contact_rate = relative_contact_rate
        self.susceptible = susceptible

        self.market_share = market_share
        self.max_y_axis = max_y_axis
        self.n_days = n_days
        self.recovery_days = recovery_days

        self.hospitalized = hospitalized
        self.icu = icu
        self.ventilated = ventilated

        # TODO dataframe
        self.dispositions = {
            "hospitalized": hospitalized,
            "icu": icu,
            "ventilated": ventilated,
        }

