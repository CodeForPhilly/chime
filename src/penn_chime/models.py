"""Models.

Changes affecting results or their presentation should also update
constants.py `change_date`,
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from logging import INFO, basicConfig, getLogger
from sys import stdout
from typing import Dict, Generator, Tuple, Sequence, Optional

import numpy as np
import pandas as pd

from .constants import EPSILON, CHANGE_DATE
from .parameters import Parameters


basicConfig(
    level=INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=stdout,
)
logger = getLogger(__name__)


class SimSirModel:

    def __init__(self, p: Parameters):

        self.rates = {
            key: d.rate
            for key, d in p.dispositions.items()
        }

        self.days = {
            key: d.days
            for key, d in p.dispositions.items()
        }

        self.keys = ("susceptible", "infected", "recovered")

        # An estimate of the number of infected people on the day that
        # the first hospitalized case is seen
        #
        # Note: this should not be an integer.
        infected = (
            1.0 / p.market_share / p.hospitalized.rate
        )

        susceptible = p.population - infected

        gamma = 1.0 / p.infectious_days
        self.gamma = gamma

        self.susceptible = susceptible
        self.infected = infected
        self.recovered = p.recovered

        if p.date_first_hospitalized is None and p.doubling_time is not None:
            # Back-projecting to when the first hospitalized case would have been admitted
            logger.info('Using doubling_time: %s', p.doubling_time)

            intrinsic_growth_rate = get_growth_rate(p.doubling_time)

            self.beta = get_beta(intrinsic_growth_rate,  gamma, self.susceptible, 0.0)
            self.beta_t = get_beta(intrinsic_growth_rate, self.gamma, self.susceptible, p.relative_contact_rate)

            self.i_day = 0 # seed to the full length
            self.run_projection(p, [(self.beta, p.n_days)])
            self.i_day = i_day = int(get_argmin_ds(self.census_df, p.current_hospitalized))

            self.run_projection(p, self.gen_policy(p))

            logger.info('Set i_day = %s', i_day)
            p.date_first_hospitalized = p.current_date - timedelta(days=i_day)
            logger.info(
                'Estimated date_first_hospitalized: %s; current_date: %s; i_day: %s',
                p.date_first_hospitalized,
                p.current_date,
                self.i_day)

        elif p.date_first_hospitalized is not None and p.doubling_time is None:
            # Fitting spread parameter to observed hospital census (dates of 1 patient and today)
            self.i_day = (p.current_date - p.date_first_hospitalized).days
            self.current_hospitalized = p.current_hospitalized
            logger.info(
                'Using date_first_hospitalized: %s; current_date: %s; i_day: %s, current_hospitalized: %s',
                p.date_first_hospitalized,
                p.current_date,
                self.i_day,
                p.current_hospitalized,
            )

            # Make an initial coarse estimate
            dts = np.linspace(1, 15, 15)
            min_loss = self.get_argmin_doubling_time(p, dts)

            # Refine the coarse estimate
            for iteration in range(4):
                dts = np.linspace(dts[min_loss-1], dts[min_loss+1], 15)
                min_loss = self.get_argmin_doubling_time(p, dts)

            p.doubling_time = dts[min_loss]

            logger.info('Estimated doubling_time: %s', p.doubling_time)
            intrinsic_growth_rate = get_growth_rate(p.doubling_time)
            self.beta = get_beta(intrinsic_growth_rate, self.gamma, self.susceptible, 0.0)
            self.beta_t = get_beta(intrinsic_growth_rate, self.gamma, self.susceptible, p.relative_contact_rate)
            self.run_projection(p, self.gen_policy(p))

            self.population = p.population
        else:
            logger.info(
                'doubling_time: %s; date_first_hospitalized: %s',
                p.doubling_time,
                p.date_first_hospitalized,
            )
            raise AssertionError('doubling_time or date_first_hospitalized must be provided.')

        logger.info('len(np.arange(-i_day, n_days+1)): %s', len(np.arange(-self.i_day, p.n_days+1)))
        logger.info('len(raw_df): %s', len(self.raw_df))

        self.infected = self.raw_df['infected'].values[self.i_day]
        self.susceptible = self.raw_df['susceptible'].values[self.i_day]
        self.recovered = self.raw_df['recovered'].values[self.i_day]

        self.intrinsic_growth_rate = intrinsic_growth_rate

        # r_t is r_0 after distancing
        self.r_t = self.beta_t / gamma * susceptible
        self.r_naught = self.beta / gamma * susceptible

        doubling_time_t = 1.0 / np.log2(
            self.beta_t * susceptible - gamma + 1)
        self.doubling_time_t = doubling_time_t

        self.sim_sir_w_date_df = build_sim_sir_w_date_df(self.raw_df, p.current_date, self.keys)

        self.sim_sir_w_date_floor_df = build_floor_df(self.sim_sir_w_date_df, self.keys)
        self.admits_floor_df = build_floor_df(self.admits_df, p.dispositions.keys())
        self.census_floor_df = build_floor_df(self.census_df, p.dispositions.keys())

        self.daily_growth_rate = get_growth_rate(p.doubling_time)
        self.daily_growth_rate_t = get_growth_rate(self.doubling_time_t)

    def get_argmin_doubling_time(self, p: Parameters, dts):
        losses = np.full(dts.shape[0], np.inf)
        for i, i_dt in enumerate(dts):
            intrinsic_growth_rate = get_growth_rate(i_dt)
            self.beta = get_beta(intrinsic_growth_rate, self.gamma, self.susceptible, 0.0)
            self.beta_t = get_beta(intrinsic_growth_rate, self.gamma, self.susceptible, p.relative_contact_rate)

            self.run_projection(p, self.gen_policy(p))

            # Skip values the would put the fit past peak
            peak_admits_day = self.admits_df.hospitalized.argmax()
            if peak_admits_day < 0:
                continue

            loss = self.get_loss()
            losses[i] = loss

        min_loss = pd.Series(losses).argmin()
        return min_loss

    def gen_policy(self, p: Parameters) -> Sequence[Tuple[float, int]]:
        if p.mitigation_date is not None:
            mitigation_day = -(p.current_date - p.mitigation_date).days
        else:
            mitigation_day = 0

        total_days = self.i_day + p.n_days

        if mitigation_day < -self.i_day:
            mitigation_day = -self.i_day

        pre_mitigation_days = self.i_day + mitigation_day
        post_mitigation_days = total_days - pre_mitigation_days

        return [
            (self.beta,   pre_mitigation_days),
            (self.beta_t, post_mitigation_days),
        ]

    def run_projection(self, p: Parameters, policy: Sequence[Tuple[float, int]]):
        self.raw_df = sim_sir_df(
            self.susceptible,
            self.infected,
            p.recovered,
            self.gamma,
            -self.i_day,
            policy
        )

        self.dispositions_df = build_dispositions_df(self.raw_df, self.rates, p.market_share, p.current_date)
        self.admits_df = build_admits_df(self.dispositions_df)
        self.census_df = build_census_df(self.admits_df, self.days)
        self.current_infected = self.raw_df.infected.loc[self.i_day]

    def get_loss(self) -> float:
        """Squared error: predicted vs. actual current hospitalized."""
        predicted = self.census_df.hospitalized.loc[self.i_day]
        return (self.current_hospitalized - predicted) ** 2.0


def get_argmin_ds(census_df: pd.DataFrame, current_hospitalized: float) -> float:
    # By design, this forbids choosing a day after the peak
    # If that's a problem, see #381
    peak_day = census_df.hospitalized.argmax()
    losses_df = (census_df.hospitalized[:peak_day] - current_hospitalized) ** 2.0
    return losses_df.argmin()


def get_beta(
    intrinsic_growth_rate: float,
    gamma: float,
    susceptible: float,
    relative_contact_rate: float
) -> float:
    return (
        (intrinsic_growth_rate + gamma)
        / susceptible
        * (1.0 - relative_contact_rate)
    )


def get_growth_rate(doubling_time: Optional[float]) -> float:
    """Calculates average daily growth rate from doubling time."""
    if doubling_time is None or doubling_time == 0.0:
        return 0.0
    return (2.0 ** (1.0 / doubling_time) - 1.0)


def sir(
    s: float, i: float, r: float, beta: float, gamma: float, n: float
) -> Tuple[float, float, float]:
    """The SIR model, one time step."""
    s_n = (-beta * s * i) + s
    i_n = (beta * s * i - gamma * i) + i
    r_n = gamma * i + r

    # TODO:
    #   Post check dfs for negative values and
    #   warn the user that their input data is bad.
    #   JL: I suspect that these adjustments covered bugs.

    #if s_n < 0.0:
    #    s_n = 0.0
    #if i_n < 0.0:
    #    i_n = 0.0
    #if r_n < 0.0:
    #    r_n = 0.0
    scale = n / (s_n + i_n + r_n)
    return s_n * scale, i_n * scale, r_n * scale


def gen_sir(
    s: float, i: float, r: float, gamma: float, i_day: int, policies: Sequence[Tuple[float, int]]
) -> Generator[Tuple[int, float, float, float], None, None]:
    """Simulate SIR model forward in time yielding tuples.
    Parameter order has changed to allow multiple (beta, n_days)
    to reflect multiple changing social distancing policies.
    """
    s, i, r = (float(v) for v in (s, i, r))
    n = s + i + r
    d = i_day
    for beta, n_days in policies:
        for _ in range(n_days):
            yield d, s, i, r
            s, i, r = sir(s, i, r, beta, gamma, n)
            d += 1
    yield d, s, i, r


def sim_sir_df(
    s: float, i: float, r: float,
    gamma: float, i_day: int, policies: Sequence[Tuple[float, int]]
) -> pd.DataFrame:
    """Simulate the SIR model forward in time."""
    return pd.DataFrame(
        data=gen_sir(s, i, r, gamma, i_day, policies),
        columns=("day", "susceptible", "infected", "recovered"),
    )


def build_sim_sir_w_date_df(
    raw_df: pd.DataFrame,
    current_date: datetime,
    keys: Sequence[str],
) -> pd.DataFrame:
    day = raw_df.day
    return pd.DataFrame({
        "day": day,
        "date": day.astype('timedelta64[D]') + np.datetime64(current_date),
        **{
            key: raw_df[key]
            for key in keys
        }
    })


def build_floor_df(df, keys):
    """Build floor sim sir w date."""
    return pd.DataFrame({
        "day": df.day,
        "date": df.date,
        **{
            key: np.floor(df[key])
            for key in keys
        }
    })


def build_dispositions_df(
    raw_df: pd.DataFrame,
    rates: Dict[str, float],
    market_share: float,
    current_date: datetime,
) -> pd.DataFrame:
    """Build dispositions dataframe of patients adjusted by rate and market_share."""
    patients = raw_df.infected + raw_df.recovered
    day = raw_df.day
    return pd.DataFrame({
        "day": day,
        "date": day.astype('timedelta64[D]') + np.datetime64(current_date),
        **{
            key: patients * rate * market_share
            for key, rate in rates.items()
        }
    })


def build_admits_df(dispositions_df: pd.DataFrame) -> pd.DataFrame:
    """Build admits dataframe from dispositions."""
    admits_df = dispositions_df - dispositions_df.shift(1)
    admits_df.day = dispositions_df.day
    admits_df.date = dispositions_df.date
    return admits_df


def build_census_df(
    admits_df: pd.DataFrame,
    lengths_of_stay: Dict[str, int],
) -> pd.DataFrame:
    """Average Length of Stay for each disposition of COVID-19 case (total guesses)"""
    return pd.DataFrame({
        'day': admits_df.day,
        'date': admits_df.date,
        **{
            key: (
                admits_df[key].cumsum()
                - admits_df[key].cumsum().shift(los).fillna(0)
            )
            for key, los in lengths_of_stay.items()
        }
    })
