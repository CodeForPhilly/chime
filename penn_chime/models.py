from typing import Tuple

import numpy as np


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
def sim_sir(
    S, I, R, beta, gamma, n_days, beta_decay=0
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    N = S + I + R
    s, i, r = [S], [I], [R]
    for day in range(n_days):
        y = S, I, R
        S, I, R = sir(y, beta, gamma, N)
        beta = beta * (1 - beta_decay)  # okay even if beta_decay is 0
        s.append(S)
        i.append(I)
        r.append(R)

    s, i, r = np.array(s), np.array(i), np.array(r)
    return s, i, r


def get_hospitalizations(
    infected: np.ndarray, rates: Tuple[float, float, float], market_share: float
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    hosp_rate, icu_rate, vent_rate = rates

    hosp = infected * hosp_rate * market_share
    icu = infected * icu_rate * market_share
    vent = infected * vent_rate * market_share
    return hosp, icu, vent
