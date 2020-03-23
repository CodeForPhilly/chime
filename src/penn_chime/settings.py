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
    current_hospitalized=6,
    doubling_time=6,
    known_infected=157,
    n_days=60,
    market_share=0.15,
    relative_contact_rate=0,
    hospitalized=RateLos(0.05, 7),
    icu=RateLos(0.02, 9),
    ventilated=RateLos(0.01, 10),
)
