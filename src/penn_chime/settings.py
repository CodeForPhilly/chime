#!/usr/bin/env python

from .defaults import Constants, Regions, RateLos

delaware = 564696
chester = 519293
montgomery = 826075
bucks = 628341
philly = 1581000

DEFAULTS = Constants(
    # EDIT YOUR DEFAULTS HERE
    region=Regions(
        delaware=delaware,
        chester=chester,
        montgomery=montgomery,
        bucks=bucks,
        philly=philly,
    ),
    current_hospitalized=14,
    doubling_time=4,
    known_infected=510,
    n_days=60,
    market_share=0.15,
    relative_contact_rate=0.3,
    hospitalized=RateLos(0.025, 7),
    icu=RateLos(0.0075, 9),
    ventilated=RateLos(0.005, 10),
)
