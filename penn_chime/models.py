from typing import Generator, Tuple

import numpy as np
import pandas as pd
import streamlit as st

from .defaults import RateLos


class Parameters:

    def __init__(
        self, *,
        current_hospitalized: int,
        doubling_time: float,
        known_infected: int,
        market_share: float,
        relative_contact_rate: float,
        susceptible: int,

        hospitalized: RateLos,
        icu: RateLos,
        ventilated: RateLos,
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

        self.rates = tuple(
            each.rate
            for each in (hospitalized, icu, ventilated)
        )
        self.lengths_of_stay = tuple(
            each.length_of_stay
            for each in (hospitalized, icu, ventilated)
        )

        # Note: this should not be an integer.
        # We're appoximating infected from what we do know.
        # TODO market_share > 0, hosp_rate > 0
        self.infected = infected = \
            current_hospitalized / market_share / hospitalized.rate

        self.detection_probability = \
            known_infected / infected if infected > 1.e-7 else None

        # TODO missing initial recovered value
        self.recovered = 0.0

        self.intrinsic_growth_rate = intrinsic_growth_rate = \
            2.0 ** (1.0 / doubling_time) - 1.0 if doubling_time > 0.0 else 0.0

        # TODO make this configurable, or more nuanced
        self.recovery_days = recovery_days = 14.0

        self.gamma = gamma = 1.0 / recovery_days

        # Contact rate, beta
        self.beta = beta = (
            (intrinsic_growth_rate + gamma) /
            susceptible * (1.0 - relative_contact_rate)
        )  # {rate based on doubling time} / {initial susceptible}

        # r_t is r_0 after distancing
        self.r_t = beta / gamma * susceptible

        # Simplify equation to avoid division by zero:
        # self.r_naught = r_t / (1.0 - relative_contact_rate)
        self.r_naught = (intrinsic_growth_rate + gamma) / gamma

        # doubling time after distancing
        # TODO constrain values np.log2(...) > 0.0
        self.doubling_time_t = 1.0 / np.log2(beta * susceptible - gamma + 1)

    @property
    def n_days(self):
        return self._n_days

    @n_days.setter
    def n_days(self, n_days: int):
        self._n_days = n_days

        # s := Susceptible, able to be infected
        # i := Infected, currently infected with the virus
        # r := Recovered, no longer infected with the virus

        s_v, i_v, r_v = sim_sir(
            self.susceptible,
            self.infected,
            self.recovered,
            self.beta,
            self.gamma,
            n_days,
        )
        self.susceptible_v, self.infected_v, self.recovered_v = s_v, i_v, r_v

        self.dispositions = hospitalized_v, icu_v, ventilated_v = \
            get_dispositions(i_v, self.rates, self.market_share)
        self.hospitalized_v, self.icu_v, self.ventilated_v = \
            hospitalized_v, icu_v, ventilated_v


@st.cache
def sir(
    s: float, i: float, r: float,
    beta: float, gamma: float, n: float
) -> Tuple[float, float, float]:
    """The SIR model, one time step."""
    s_n = (-beta * s * i) + s
    i_n = (beta * s * i - gamma * i) + i
    r_n = gamma * i + r
    if s_n < 0.0:
        s_n = 0.0
    if i_n < 0.0:
        i_n = 0.0
    if r_n < 0.0:
        r_n = 0.0

    scale = n / (s_n + i_n + r_n)
    return s_n * scale, i_n * scale, r_n * scale


def gen_sir(
    s: float, i: float, r: float,
    beta: float, gamma: float, n_days: int
) -> Generator[Tuple[float, float, float], None, None]:
    """Simulate SIR model forward in time yielding tuples."""
    s, i, r = (float(v) for v in (s, i, r))
    n = s + i + r
    for _ in range(n_days + 1):
        yield s, i, r
        s, i, r = sir(s, i, r, beta, gamma, n)


@st.cache
def sim_sir(
    s: float, i: float, r: float,
    beta: float, gamma: float, n_days: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Simulate the SIR model forward in time."""
    s, i, r = (float(v) for v in (s, i, r))
    n = s + i + r
    s_v, i_v, r_v = [s], [i], [r]
    for day in range(n_days):
        s, i, r = sir(s, i, r, beta, gamma, n)
        s_v.append(s)
        i_v.append(i)
        r_v.append(r)

    return (
        np.array(s_v),
        np.array(i_v),
        np.array(r_v),
    )


@st.cache
def sim_sir_df(
    s: float, i: float, r: float,
    beta: float, gamma: float, n_days: int
) -> pd.DataFrame:
    """Simulate the SIR model forward in time."""
    return pd.DataFrame(
        data=gen_sir(s, i, r, beta, gamma, n_days),
        columns=("Susceptible", "Infected", "Recovered"),
    )


@st.cache
def get_dispositions(
    infected: np.ndarray, rates: Tuple[float, ...], market_share: float = 1.0
) -> Tuple[np.ndarray, ...]:
    """Get dispositions of infected adjusted by rate and market_share."""
    return (*(infected * rate * market_share for rate in rates),)
