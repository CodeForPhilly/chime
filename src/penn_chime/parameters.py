"""Parameters."""

from numpy import log2  # type: ignore

from .utils import RateLos
from .models import (
    get_dispositions,
    sim_sir,
)


class Parameters:
    def __init__(
        self,
        *,
        current_hospitalized: int,
        doubling_time: float,
        known_infected: int,
        market_share: float,
        relative_contact_rate: float,
        susceptible: int,
        hospitalized: RateLos,
        icu: RateLos,
        ventilated: RateLos,
        max_y_axis: int = None,
        n_days: int = None
    ):
        self.current_hospitalized = current_hospitalized
        self.doubling_time = doubling_time
        self.known_infected = known_infected
        self.market_share = market_share
        self.relative_contact_rate = relative_contact_rate
        self.susceptible = susceptible
        self._n_days = 0

        self.hospitalized = hospitalized
        self.icu = icu
        self.ventilated = ventilated

        self.max_y_axis = max_y_axis

        self.rates = tuple(each.rate for each in (hospitalized, icu, ventilated))
        self.lengths_of_stay = tuple(
            each.length_of_stay for each in (hospitalized, icu, ventilated)
        )

        # Note: this should not be an integer.
        # We're appoximating infected from what we do know.
        # TODO market_share > 0, hosp_rate > 0
        self.infected = infected = (
            current_hospitalized / market_share / hospitalized.rate
        )

        self.detection_probability = (
            known_infected / infected if infected > 1.0e-7 else None
        )

        # TODO missing initial recovered value
        self.recovered = 0.0

        self.intrinsic_growth_rate = intrinsic_growth_rate = (
            2.0 ** (1.0 / doubling_time) - 1.0 if doubling_time > 0.0 else 0.0
        )

        # TODO make this configurable, or more nuanced
        self.recovery_days = recovery_days = 14.0

        self.gamma = gamma = 1.0 / recovery_days

        # Contact rate, beta
        self.beta = beta = (
            (intrinsic_growth_rate + gamma)
            / susceptible
            * (1.0 - relative_contact_rate)
        )  # {rate based on doubling time} / {initial susceptible}

        # r_t is r_0 after distancing
        self.r_t = beta / gamma * susceptible

        # Simplify equation to avoid division by zero:
        # self.r_naught = r_t / (1.0 - relative_contact_rate)
        self.r_naught = (intrinsic_growth_rate + gamma) / gamma

        # doubling time after distancing
        # TODO constrain values np.log2(...) > 0.0
        self.doubling_time_t = 1.0 / log2(beta * susceptible - gamma + 1)

        self.dispositions = None
        self.susceptible_v = self.infected_v = self.recovered_v = None
        self.hospitalized_v = self.icu_v = self.ventilated_v = None

        if n_days is not None:
            self.n_days = n_days

    @property
    def n_days(self):
        return self._n_days

    @n_days.setter
    def n_days(self, n_days: int):
        self._n_days = n_days

        s_v, i_v, r_v = sim_sir(
            self.susceptible,
            self.infected,
            self.recovered,
            self.beta,
            self.gamma,
            n_days,
        )
        self.susceptible_v, self.infected_v, self.recovered_v = s_v, i_v, r_v

        i_hospitalized_v, i_icu_v, i_ventilated_v = get_dispositions(
            i_v, self.rates, self.market_share
        )
        r_hospitalized_v, r_icu_v, r_ventilated_v = get_dispositions(
            r_v, self.rates, self.market_share
        )

        self.dispositions = (
            i_hospitalized_v + r_hospitalized_v,
            i_icu_v + r_icu_v,
            i_ventilated_v + r_ventilated_v,
        )

        self.hospitalized_v, self.icu_v, self.ventilated_v = (
            i_hospitalized_v,
            i_icu_v,
            i_ventilated_v,
        )
