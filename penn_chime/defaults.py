#!/usr/bin/env python
"""Set defaults for your fork/locality here

   after we merge this in we can set defaults in a `config/env` type of file
"""

class Constants:
    def __init__(self,
                 S_default: int, # regional population
                 known_infections: int,
                 known_cases: int,
                 doubling_time: int,
                 relative_contact_rate: int,
                 hosp_rate: float,
                 icu_rate: float,
                 vent_rate: float,
                 hosp_los: int,
                 icu_los: int,
                 vent_los: int,
                 market_share: float
    ):
        self.S_default = S_default
        self.known_infections = known_infections
        self.known_cases = known_cases
        self.doubling_time = doubling_time
        self.relative_contact_rate = relative_contact_rate
        self.hosp_rate = hosp_rate
        self.icu_rate = icu_rate
        self.vent_rate = vent_rate
        self.hosp_los = hosp_los
        self.icu_los = icu_los
        self.vent_los = vent_los
        self.market_share = market_share
        return None

    def __repr__(self) -> str:
        return f"Constants(susceptible_default: {self.S_default}, known_infections: {self.known_infections})"


delaware = 564696
chester = 519293
montgomery = 826075
bucks = 628341
philly = 1581000

DEFAULTS = Constants(
    ## EDIT YOUR DEFAULTS HERE
    S_default=delaware + chester + montgomery + bucks + philly,
    known_infections=91,
    known_cases=4,
    doubling_time=6,
    relative_contact_rate=0,
    hosp_rate=5.0,
    icu_rate=2.0,
    vent_rate=1.0,
    hosp_los=7,
    icu_los=9,
    vent_los=10,
    market_share=15.0
)
