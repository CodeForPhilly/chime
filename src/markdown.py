#!/usr/bin/env python

import streamlit as st  # type: ignore

from constants import (
    DELAWARE, CHESTER, MONTGOMERY, BUCKS, PHILLY
)

def show_more_info_about_this_tool(initial_infections, detection_prob):
    """Show more info about this tool"""
    st.subheader(
        "[Discrete-time SIR modeling](https://mathworld.wolfram.com/SIRModel.html) of infections/recovery"
    )
    st.markdown(
        """The model consists of individuals who are either _Susceptible_ ($S$), _Infected_ ($I$), or _Recovered_ ($R$).

The epidemic proceeds via a growth and decline process. This is the core model of infectious disease spread and has been in use in epidemiology for many years."""
    )
    st.markdown("""The dynamics are given by the following 3 equations.""")

    st.latex("S_{t+1} = (-\\beta S_t I_t) + S_t")
    st.latex("I_{t+1} = (\\beta S_t I_t - \\gamma I_t) + I_t")
    st.latex("R_{t+1} = (\\gamma I_t) + R_t")

    st.markdown(
        """To project the expected impact to Penn Medicine, we estimate the terms of the model.

To do this, we use a combination of estimates from other locations, informed estimates based on logical reasoning, and best guesses from the American Hospital Association.


### Parameters
First, we need to express the two parameters $\\beta$ and $\\gamma$ in terms of quantities we can estimate.

- The $\\gamma$ parameter represents 1 over the mean recovery time in days. Since the CDC is recommending 14 days of self-quarantine, we'll use $\\gamma = 1/14$.
- Next, the AHA says to expect a doubling time $T_d$ of 7-10 days. That means an early-phase rate of growth can be computed by using the doubling time formula:
"""
    )
    st.latex("g = 2^{1/T_d} - 1")

    st.markdown(
        """
- Since the rate of new infections in the SIR model is $g = \\beta S - \\gamma$, and we've already computed $\\gamma$, $\\beta$ becomes a function of the initial population size of susceptible individuals.
$$\\beta = (g + \\gamma)/s$$

### Initial Conditions

- The total size of the susceptible population will be the entire catchment area for Penn Medicine entities (HUP, PAH, PMC, CCH)
  - Delaware = {delaware}
  - Chester = {chester}
  - Montgomery = {montgomery}
  - Bucks = {bucks}
  - Philly = {philly}
- The initial number of infected will be the total number of confirmed cases in the area ({initial_infections}), divided by some detection probability to account for under testing {detection_prob:.2f}.""".format(
            delaware=DELAWARE,
            chester=CHESTER,
            montgomery=MONTGOMERY,
            bucks=BUCKS,
            philly=PHILLY,
            initial_infections=initial_infections,
            detection_prob=detection_prob,
        )
    )
    return None
