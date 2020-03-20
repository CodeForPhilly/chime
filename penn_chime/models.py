from typing import Generator, Tuple

import numpy as np
import pandas as pd
import streamlit as st


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
    beta: float, gamma: float, n_days: int, beta_decay: float = 0.0
) -> Generator[Tuple[float, float, float], None, None]:
    """Simulate SIR model forward in time yielding tuples."""
    s, i, r = (float(v) for v in (s, i, r))
    n = s + i + r
    f = 1.0 - beta_decay  # okay even if beta_decay is 0.0
    for _ in range(n_days + 1):
        yield s, i, r
        s, i, r = sir(s, i, r, beta, gamma, n)
        beta *= f


@st.cache
def sim_sir(
    s: float, i: float, r: float,
    beta: float, gamma: float, n_days: int, beta_decay: float = 0.0
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Simulate the SIR model forward in time."""
    s, i, r = (float(v) for v in (s, i, r))
    n = s + i + r
    f = 1.0 - beta_decay  # okay even if beta_decay is 0.0
    s_v, i_v, r_v = [s], [i], [r]
    for day in range(n_days):
        s, i, r = sir(s, i, r, beta, gamma, n)
        beta *= f
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
    beta: float, gamma: float, n_days: int, beta_decay: float = 0.0
) -> pd.DataFrame:
    """Simulate the SIR model forward in time."""
    return pd.DataFrame(
        data=gen_sir(s, i, r, beta, gamma, n_days, beta_decay),
        columns=("S", "I", "R"),
    )


@st.cache
def get_hospitalizations2(
    infected: np.ndarray, rates: Tuple[float, ...], market_share: float = 1.0
) -> Tuple[np.ndarray, ...]:
    """Get hopitalizations adjusted by rate and market_share."""
    return (*(infected * rate * market_share for rate in rates),)


@st.cache
def get_hospitalizations(
    infected: np.ndarray, rates: Tuple[float, float, float], market_share: float
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Get hopitalizations adjusted by rate and market_share."""
    hosp_rate, icu_rate, vent_rate = rates

    hosp = infected * hosp_rate * market_share
    icu = infected * icu_rate * market_share
    vent = infected * vent_rate * market_share
    return hosp, icu, vent
