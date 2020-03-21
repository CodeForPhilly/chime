"""Models."""

from typing import Generator, Tuple

import numpy as np  # type: ignore
import pandas as pd  # type: ignore


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


def sim_sir_df(p) -> pd.DataFrame:
    """Simulate the SIR model forward in time.

    p is a Parameters instance. for circuluar dependency reasons i can't annotate it.
    """
    return pd.DataFrame(
        data=gen_sir(p.susceptible, p.infected, p.recovered, p.beta, p.gamma, p.n_days),
        columns=("Susceptible", "Infected", "Recovered"),
    )


def get_dispositions(
    infected: np.ndarray, rates: Tuple[float, ...], market_share: float = 1.0
) -> Tuple[np.ndarray, ...]:
    """Get dispositions of infected adjusted by rate and market_share."""
    return (*(infected * rate * market_share for rate in rates),)



def build_admissions_df(p) -> pd.DataFrame:
    """Build admissions dataframe from Parameters."""
    days = np.array(range(0, p.n_days + 1))
    data_dict = dict(zip(["day", "Hospitalized", "ICU", "Ventilated"],
                         [days] + [disposition for disposition in p.dispositions]
    ))
    projection = pd.DataFrame.from_dict(data_dict)
    # New cases
    projection_admits = projection.iloc[:-1, :] - projection.shift(1)
    projection_admits[projection_admits < 0] = 0
    projection_admits["day"] = range(projection_admits.shape[0])
    return projection_admits


def build_census_df(
        projection_admits: pd.DataFrame,
        parameters
) -> pd.DataFrame:
    """ALOS for each category of COVID-19 case (total guesses)"""
    n_days = np.shape(projection_admits)[0]
    hosp_los, icu_los, vent_los = parameters.lengths_of_stay
    los_dict = {
        "Hospitalized": hosp_los,
        "ICU": icu_los,
        "Ventilated": vent_los,
    }

    census_dict = dict()
    for k, los in los_dict.items():
        census = (
            projection_admits.cumsum().iloc[:-los, :]
            - projection_admits.cumsum().shift(los).fillna(0)
        ).apply(np.ceil)
        census_dict[k] = census[k]

    census_df = pd.DataFrame(census_dict)
    census_df["day"] = census_df.index
    census_df = census_df[["day", "Hospitalized", "ICU", "Ventilated"]]
    census_df = census_df.head(n_days)
    census_df = census_df.rename(
        columns={disposition: f"{disposition} Census"
                 for disposition
                 in ("Hospitalized", "ICU", "Ventilated")}
    )
    return census_df
