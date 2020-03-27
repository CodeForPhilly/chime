"""Models.

Changes affecting results or their presentation should also update
parameters.py `change_date`, so users can see when results have last
changed
"""

from __future__ import annotations

from typing import Dict, Generator, Tuple, Optional

import numpy as np  # type: ignore
import pandas as pd  # type: ignore

from .parameters import Parameters
from .utils import SimSirModelAttributes

class SimSirModel:

    def __init__(self, p: Parameters):
        # TODO missing initial non-zero 'recovered' value
        recovered = 0.0
        recovery_days = p.recovery_days

        rates = {
            key: d.rate
            for key, d in p.dispositions.items()
        }

        lengths_of_stay = {
            key: d.length_of_stay
            for key, d in p.dispositions.items()
        }

        self._rates = rates
        self._lengths_of_stay = lengths_of_stay

        # Note: this should not be an integer.
        # We're appoximating infected from what we do know.
        # TODO market_share > 0, hosp_rate > 0
        infected = (
            p.current_hospitalized / p.market_share / p.hospitalized.rate
        )

        susceptible = p.population - infected

        detection_probability = (
            p.known_infected / infected if infected > 1.0e-7 else None
        )

        # (2.0 ** (1.0 / p.doubling_time) - 1.0) if p.doubling_time > 0.0 else 0.0
        intrinsic_growth_rate = self._intrinsic_growth_rate(p.doubling_time)

        gamma = 1.0 / recovery_days

        # Contact rate, beta
        beta = (
            (intrinsic_growth_rate + gamma)
            / susceptible
            * (1.0 - p.relative_contact_rate)
        )  # {rate based on doubling time} / {initial susceptible}

        # r_t is r_0 after distancing
        r_t = beta / gamma * susceptible

        # Simplify equation to avoid division by zero:
        # self.r_naught = r_t / (1.0 - relative_contact_rate)
        r_naught = (intrinsic_growth_rate + gamma) / gamma
        doubling_time_t = 1.0 / np.log2(
            beta * susceptible - gamma + 1)

        raw_df = sim_sir_df(
            susceptible,
            infected,
            recovered,
            beta,
            gamma,
            p.n_days,
        )
        dispositions_df = build_dispositions_df(raw_df, rates, p.market_share)
        admits_df = build_admits_df(dispositions_df)
        census_df = build_census_df(admits_df, lengths_of_stay)

        self.susceptible = susceptible
        self.infected = infected
        self.recovered = recovered

        self.detection_probability = detection_probability
        self.recovered = recovered
        self.intrinsic_growth_rate = intrinsic_growth_rate
        self.gamma = gamma
        self.beta = beta
        self.r_t = r_t
        self.r_naught = r_naught
        self.doubling_time_t = doubling_time_t
        self.raw_df = raw_df
        self.dispositions_df = dispositions_df
        self.admits_df = admits_df
        self.census_df = census_df

        if p.n_days_since_first_hospitalized is not None and p.doubling_time is None:
            # optimize doubling_time
            argmin_dt = None
            min_loss = 2.0**99
            censes = dict()
            for dt in np.linspace(1,15,29):
                censes[dt] = self.run_projection(p, dt)
                self.census_df = censes[dt] # log it into state for loss
                loss_dt = self.loss_dt(p)
                if loss_dt < min_loss:
                    min_loss = loss_dt
                    argmin_dt = dt
            self.census_df = censes[dt]
            p.doubling_time = argmin_dt
            #
            # update all state dependent on doubling time.
            intrinsic_growth_rate = self._intrinsic_growth_rate(p.doubling_time)
            gamma = 1 / recovery_days
            beta = self._beta(intrinsic_growth_rate, gamma, susceptible, p.relative_contact_rate)
            r_t = beta / gamma * susceptible
            r_naught = (intrinsic_growth_rate + gamma) / gamma
            doubling_time_t = 1.0 / np.log2(beta * susceptible - gamma + 1)
            raw_df = sim_sir_df(
                susceptible,
                infected,
                recovered,
                beta,
                gamma,
                p.n_days
            )
            dispositions_df = build_dispositions_df(raw_df, rates, p.market_share)
            admits_df = build_admits_df(dispositions_df)
            census_df = build_census_df(admits_df, lengths_of_stay)

            self.intrinsic_growth_rate = intrinsic_growth_rate
            self.gamma = gamma
            self.beta = beta
            self.r_t = r_t
            self.r_naught = r_naught
            self.doubling_time_t = doubling_time_t
            self.raw_df = raw_df
            self.dispositions_df = dispositions_df
            self.admits_df = admits_df
            self.census_df = census_df

        self.daily_growth = daily_growth_helper(p.doubling_time)
        self.daily_growth_t = daily_growth_helper(doubling_time_t)

        return None

    def run_projection(self, p: Parameters, doubling_time: float) -> pd.DataFrame:
        intrinsic_growth_rate = self._intrinsic_growth_rate(doubling_time)

        recovery_days = p.recovery_days
        market_share = p.market_share
        initial_i = 1 / p.hospitalized.rate / market_share

        S, I, R = self.susceptible, self.infected, self.recovered

        # mean recovery rate (inv_recovery_days)
        gamma = 1 / recovery_days

        # contact rate
        beta = (intrinsic_growth_rate + gamma) / S

        n_days = p.n_days

        raw_df = sim_sir_df(S,I,R,beta,gamma,n_days)

        dispositions_df = build_dispositions_df(raw_df, self._rates, p.market_share)
        admits_df = build_admits_df(dispositions_df)
        census_df = build_census_df(admits_df, self._lengths_of_stay)
        return census_df

    def loss_dt(self, p: Parameters) -> float:
        """Squared error: predicted_current_hospitalized vs. actual current hospitalized

        gets prediction of current hospitalized from a census_df which
        is dependent on a given doubling_time in state.
        """
        # get the predicted number of hospitalized today
        predicted_current_hospitalized = self.census_df.hospitalized.loc[p.n_days_since_first_hospitalized]

        # compare against actual / user inputted number
        # we shall optimize squared distance
        return (p.current_hospitalized - predicted_current_hospitalized) ** 2


    @staticmethod
    def _intrinsic_growth_rate(doubling_time: Optional[float]) -> float:
        if doubling_time is not None:
            return (2.0 ** (1.0 / doubling_time) - 1.0) if doubling_time > 0.0 else 0.0
        return 0.0

    @staticmethod
    def _beta(
            intrinsic_growth_rate: float,
            gamma: float,
            susceptible: float,
            relative_contact_rate: float) -> float:
        return (
            (intrinsic_growth_rate + gamma)
            / susceptible
            * (1.0 - relative_contact_rate)
        )

###################
##  MODEL FUNCS  ##
###################
def sir(
    s: float, i: float, r: float, beta: float, gamma: float, n: float
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
    s: float, i: float, r: float, beta: float, gamma: float, n_days: int
) -> Generator[Tuple[int, float, float, float], None, None]:
    """Simulate SIR model forward in time yielding tuples."""
    s, i, r = (float(v) for v in (s, i, r))
    n = s + i + r
    for d in range(n_days + 1):
        yield d, s, i, r
        s, i, r = sir(s, i, r, beta, gamma, n)


def sim_sir_df(
    s: float, i: float, r: float, beta: float, gamma: float, n_days: int
) -> pd.DataFrame:
    """Simulate the SIR model forward in time."""
    return pd.DataFrame(
        data=gen_sir(s, i, r, beta, gamma, n_days),
        columns=("day", "susceptible", "infected", "recovered"),
    )

def build_dispositions_df(
    sim_sir_df: pd.DataFrame,
    rates: Dict[str, float],
    market_share: float,
) -> pd.DataFrame:
    """Get dispositions of patients adjusted by rate and market_share."""
    patients = sim_sir_df.infected + sim_sir_df.recovered
    return pd.DataFrame({
        "day": sim_sir_df.day,
        **{
            key: patients * rate * market_share
            for key, rate in rates.items()
        }
    })


def build_admits_df(dispositions_df: pd.DataFrame) -> pd.DataFrame:
    """Build admits dataframe from dispositions."""
    admits_df = dispositions_df.iloc[:-1, :] - dispositions_df.shift(1)
    admits_df.day = dispositions_df.day
    return admits_df


def build_census_df(
    admits_df: pd.DataFrame,
    lengths_of_stay: Dict[str, int],
) -> pd.DataFrame:
    """Average Length of Stay for each disposition of COVID-19 case (total guesses)"""
    return pd.DataFrame({
        'day': admits_df.day,
        **{
            key: (
                admits_df[key].cumsum().iloc[:-los]
                - admits_df[key].cumsum().shift(los).fillna(0)
            ).apply(np.ceil)
            for key, los in lengths_of_stay.items()
        }
    })


############################
##  ARGMIN DOUBLING_TIME  ##
############################


def observed_predicted_loss(self, doubling_time: float, p: Parameters) -> float:
    """Squared error between predicted value and actual value

    Won't be run if n_days_since_first_hospitalized is None
    """
    census_df = self.run_projection(p, dt=doubling_time)
    ## get the predicted number hospitalized today
    pred_current_hospitalized = self.census_df['hospitalized'].loc[p.n_days_since_first_hospitalized]

    ## compare against the actual (user inputed) number
    ## squared difference is the loss to be optimized
    return (p.current_hospitalized - pred_current_hospitalized)**2

def argmin_dt(self, doubling_times: np.ndarray, p: Parameters) -> float:
    """Argmin of the loss function with respect to doubling time."""
    loss = np.array([self.observed_predicted_loss(dt, p) for dt in doubling_times])
    fitted_doubling_time = doubling_times[loss.argmin()]
    return fitted_doubling_time


#############
##  UTILS  ##
#############
def daily_growth_helper(doubling_time: float) -> float:
    """Calculates average daily growth rate from doubling time"""
    result = 0
    if doubling_time != 0 and doubling_time is not None:
        result = (np.power(2, 1.0 / doubling_time) - 1) * 100
    return result
