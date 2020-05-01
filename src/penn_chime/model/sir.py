"""Models.

Changes affecting results or their presentation should also update
constants.py `change_date`,
"""

from __future__ import annotations

from datetime import datetime, timedelta
from logging import INFO, basicConfig, getLogger
from sys import stdout
from typing import Dict, Tuple, Sequence, Optional

import numpy as np
import pandas as pd

from ..constants import PREFIT_ADDITIONAL_DAYS
from .parameters import Parameters


basicConfig(
    level=INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=stdout,
)
logger = getLogger(__name__)


class Sir:

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

        self.reasonable_model_parameters = True

        if p.date_first_hospitalized is None and p.doubling_time is not None:
            # Back-projecting to when the first hospitalized case would have been admitted
            logger.info('Using doubling_time: %s', p.doubling_time)

            intrinsic_growth_rate = get_growth_rate(p.doubling_time)
            self.beta = get_beta(intrinsic_growth_rate,  gamma, self.susceptible, 0.0)
            self.beta_t = get_beta(intrinsic_growth_rate, self.gamma, self.susceptible, p.relative_contact_rate)

            if p.mitigation_date is None:
                self.i_day = 0 # seed to the full length
                raw = self.run_projection(p, [
                    (self.beta, p.n_days + PREFIT_ADDITIONAL_DAYS)])
                self.i_day = i_day = int(get_argmin_ds(raw["census_hospitalized"], p.current_hospitalized))

                self.raw = self.run_projection(p, self.get_policies(p))

                logger.info('Set i_day = %s', i_day)
            else:
                best_i_day = -1
                best_i_day_loss = float('inf')
                for self.i_day in range(p.n_days + PREFIT_ADDITIONAL_DAYS):
                    mitigation_day = -(p.current_date - p.mitigation_date).days
                    if mitigation_day < -self.i_day:
                        mitigation_day = -self.i_day

                    total_days = self.i_day + p.n_days + PREFIT_ADDITIONAL_DAYS
                    pre_mitigation_days = self.i_day + mitigation_day
                    post_mitigation_days = total_days - pre_mitigation_days

                    raw = self.run_projection(p, [
                            (self.beta,   pre_mitigation_days),
                            (self.beta_t, post_mitigation_days),
                        ]
                    )

                    # Don't fit against results that put the peak before the present day
                    if raw["census_hospitalized"].argmax() < self.i_day:
                        continue

                    loss = get_loss(raw["census_hospitalized"][self.i_day], p.current_hospitalized)
                    if loss < best_i_day_loss:
                        best_i_day_loss = loss
                        best_i_day = self.i_day

                self.i_day = best_i_day
                self.raw = self.run_projection(p, self.get_policies(p))

            logger.info(
                'Estimated date_first_hospitalized: %s; current_date: %s; i_day: %s',
                p.current_date - timedelta(days=self.i_day),
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
            if min_loss >= 14:
                logger.info(
                    'Based on the current parameters, the estimated pre-mitigation doubling time is greater than 15 days. Try different parameters.'
                )
                self.reasonable_model_parameters = False
                return


            # Refine the coarse estimate
            for iteration in range(4):
                dts = np.linspace(dts[min_loss-1], dts[min_loss+1], 15)
                min_loss = self.get_argmin_doubling_time(p, dts)

            p.doubling_time = dts[min_loss]

            logger.info('Estimated doubling_time: %s', p.doubling_time)
            intrinsic_growth_rate = get_growth_rate(p.doubling_time)
            self.beta = get_beta(intrinsic_growth_rate, self.gamma, self.susceptible, 0.0)
            self.beta_t = get_beta(intrinsic_growth_rate, self.gamma, self.susceptible, p.relative_contact_rate)
            self.raw = self.run_projection(p, self.get_policies(p))

            self.population = p.population
        else:
            logger.info(
                'doubling_time: %s; date_first_hospitalized: %s',
                p.doubling_time,
                p.date_first_hospitalized,
            )
            raise AssertionError('doubling_time or date_first_hospitalized must be provided.')

        self.raw["date"] = self.raw["day"].astype("timedelta64[D]") + np.datetime64(p.current_date)

        self.raw_df = pd.DataFrame(data=self.raw)
        self.dispositions_df = pd.DataFrame(data={
            'day': self.raw['day'],
            'date': self.raw['date'],
            'ever_hospitalized': self.raw['ever_hospitalized'],
            'ever_icu': self.raw['ever_icu'],
            'ever_ventilated': self.raw['ever_ventilated'],
        })
        self.admits_df = pd.DataFrame(data={
            'day': self.raw['day'],
            'date': self.raw['date'],
            'admits_hospitalized': self.raw['admits_hospitalized'],
            'admits_icu': self.raw['admits_icu'],
            'admits_ventilated': self.raw['admits_ventilated'],
        })
        self.census_df = pd.DataFrame(data={
            'day': self.raw['day'],
            'date': self.raw['date'],
            'census_hospitalized': self.raw['census_hospitalized'],
            'census_icu': self.raw['census_icu'],
            'census_ventilated': self.raw['census_ventilated'],
        })
        self.ppe_df = pd.DataFrame(data={
            'day': self.raw['day'],
            'date': self.raw['date'],
            'census_hospitalized': self.raw['census_hospitalized'],
            'census_icu': self.raw['census_icu'],
            'census_ventilated': self.raw['census_ventilated'],
            'admits_hospitalized': self.raw['admits_hospitalized'],
        })
        self.ppe_df = self.ppe_df[self.ppe_df['day']>=0]

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

        self.sim_sir_w_date_floor_df = build_floor_df(self.sim_sir_w_date_df, self.keys, "")
        self.admits_floor_df = build_floor_df(self.admits_df, p.dispositions.keys(), "admits_")
        self.census_floor_df = build_floor_df(self.census_df, p.dispositions.keys(), "census_")

        self.daily_growth_rate = get_growth_rate(p.doubling_time)
        self.daily_growth_rate_t = get_growth_rate(self.doubling_time_t)

    def get_argmin_doubling_time(self, p: Parameters, dts):
        losses = np.full(dts.shape[0], np.inf)
        for i, i_dt in enumerate(dts):
            intrinsic_growth_rate = get_growth_rate(i_dt)
            self.beta = get_beta(intrinsic_growth_rate, self.gamma, self.susceptible, 0.0)
            self.beta_t = get_beta(intrinsic_growth_rate, self.gamma, self.susceptible, p.relative_contact_rate)

            raw = self.run_projection(p, self.get_policies(p))

            # Skip values the would put the fit past peak
            peak_admits_day = raw["admits_hospitalized"].argmax()
            if peak_admits_day < 0:
                continue

            predicted = raw["census_hospitalized"][self.i_day]
            loss = get_loss(self.current_hospitalized, predicted)
            losses[i] = loss

        min_loss = pd.Series(losses).argmin()
        return min_loss

    def get_policies(self, p: Parameters) -> Sequence[Tuple[float, int]]:
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
        raw = sim_sir(
            self.susceptible,
            self.infected,
            p.recovered,
            self.gamma,
            -self.i_day,
            policy
        )

        calculate_dispositions(raw, self.rates, p.market_share)
        calculate_admits(raw, self.rates)
        calculate_census(raw, self.days)

        return raw


def get_loss(current_hospitalized, predicted) -> float:
    """Squared error: predicted vs. actual current hospitalized."""
    return (current_hospitalized - predicted) ** 2.0


def get_argmin_ds(census, current_hospitalized: float) -> float:
    # By design, this forbids choosing a day after the peak
    # If that's a problem, see #381
    peak_day = census.argmax()
    losses = (census[:peak_day] - current_hospitalized) ** 2.0
    return losses.argmin()


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
    scale = n / (s_n + i_n + r_n)
    return s_n * scale, i_n * scale, r_n * scale


def sim_sir(
    s: float, i: float, r: float, gamma: float, i_day: int, policies: Sequence[Tuple[float, int]]
):
    """Simulate SIR model forward in time, returning a dictionary of daily arrays
    Parameter order has changed to allow multiple (beta, n_days)
    to reflect multiple changing social distancing policies.
    """
    s, i, r = (float(v) for v in (s, i, r))
    n = s + i + r
    d = i_day

    total_days = 1
    for beta, days in policies:
        total_days += days

    d_a = np.empty(total_days, "int")
    s_a = np.empty(total_days, "float")
    i_a = np.empty(total_days, "float")
    r_a = np.empty(total_days, "float")

    index = 0
    for beta, n_days in policies:
        for _ in range(n_days):
            d_a[index] = d
            s_a[index] = s
            i_a[index] = i
            r_a[index] = r
            index += 1

            s, i, r = sir(s, i, r, beta, gamma, n)
            d += 1

    d_a[index] = d
    s_a[index] = s
    i_a[index] = i
    r_a[index] = r
    return {
        "day": d_a,
        "susceptible": s_a,
        "infected": i_a,
        "recovered": r_a,
        "ever_infected": i_a + r_a
    }


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


def build_floor_df(df, keys, prefix):
    """Build floor sim sir w date."""
    return pd.DataFrame({
        "day": df.day,
        "date": df.date,
        **{
            prefix + key: np.floor(df[prefix+key])
            for key in keys
        }
    })


def calculate_dispositions(
    raw: Dict,
    rates: Dict[str, float],
    market_share: float,
):
    """Build dispositions dataframe of patients adjusted by rate and market_share."""
    for key, rate in rates.items():
        raw["ever_" + key] = raw["ever_infected"] * rate * market_share
        raw[key] = raw["ever_infected"] * rate * market_share


def calculate_admits(raw: Dict, rates):
    """Build admits dataframe from dispositions."""
    for key in rates.keys():
        ever = raw["ever_" + key]
        admit = np.empty_like(ever)
        admit[0] = np.nan
        admit[1:] = ever[1:] - ever[:-1]
        raw["admits_"+key] = admit
        raw[key] = admit


def calculate_census(
    raw: Dict,
    lengths_of_stay: Dict[str, int],
):
    """Average Length of Stay for each disposition of COVID-19 case (total guesses)"""
    n_days = raw["day"].shape[0]
    for key, los in lengths_of_stay.items():
        cumsum = np.empty(n_days + los)
        cumsum[:los+1] = 0.0
        cumsum[los+1:] = raw["admits_" + key][1:].cumsum()

        census = cumsum[los:] - cumsum[:-los]
        raw["census_" + key] = census
