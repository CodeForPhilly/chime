#!/usr/bin/env python
import streamlit as st  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore

from sidebar import (
    _S, _initial_infections, _detection_prob, _doubling_time, _hosp_rate, _Penn_market_share,
    _vent_rate, _icu_rate, _vent_los, _current_hosp, _hosp_los, _icu_los, _vent_los,
)
from constants import RECOVERY_DAYS


# The SIR model, one time step
def sir(y, beta, gamma, N):
    S, I, R = y
    Sn = (-beta * S * I) + S
    In = (beta * S * I - gamma * I) + I
    Rn = gamma * I + R
    if Sn < 0:
        Sn = 0
    if In < 0:
        In = 0
    if Rn < 0:
        Rn = 0

    scale = N / (Sn + In + Rn)
    return Sn * scale, In * scale, Rn * scale


# Run the SIR model forward in time
def sim_sir(S, I, R, beta, gamma, n_days, beta_decay=None):
    N = S + I + R
    s, i, r = [S], [I], [R]
    for day in range(n_days):
        y = S, I, R
        S, I, R = sir(y, beta, gamma, N)
        if beta_decay:
            beta = beta * (1 - beta_decay)
        s.append(S)
        i.append(I)
        r.append(R)

    s, i, r = np.array(s), np.array(i), np.array(r)
    return s, i, r


def model(
        initial_infections, detection_prob, doubling_time,
        n_days, hosp_rate, icu_rate, vent_rate, Penn_market_share,
        S):
    # RUN THE MODEL
    S, I, R = S, initial_infections / detection_prob, 0

    intrinsic_growth_rate = 2 ** (1 / doubling_time) - 1

    # mean recovery rate, gamma, (in 1/days).
    gamma = 1 / RECOVERY_DAYS

    # Contact rate, beta
    beta = (
        intrinsic_growth_rate + gamma
    ) / S  # {rate based on doubling time} / {initial S}


    beta_decay = 0.0
    s, i, r = sim_sir(S, I, R, beta, gamma, n_days, beta_decay=beta_decay)

    hosp = i * hosp_rate * Penn_market_share
    icu = i * icu_rate * Penn_market_share
    vent = i * vent_rate * Penn_market_share

    days = np.array(range(0, n_days + 1))
    data_list = [days, hosp, icu, vent]
    data_dict = dict(zip(["day", "hosp", "icu", "vent"], data_list))

    projection = pd.DataFrame.from_dict(data_dict)

    return projection, s, i, r
