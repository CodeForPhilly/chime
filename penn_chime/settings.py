#!/usr/bin/env python

from .defaults import Constants, Regions, RateLos

delaware = 564696
chester = 519293
montgomery = 826075
bucks = 628341
philly = 1581000

DEFAULTS = Constants(
    ## EDIT YOUR DEFAULTS HERE
    region=Regions(
        delaware=delaware,
        chester=chester,
        montgomery=montgomery,
        bucks=bucks,
        philly=philly),
    known_infections=91,
    known_cases=4,
    doubling_time=6,
    relative_contact_rate=0,
    hosp=RateLos(0.05, 7),
    icu=RateLos(0.02, 9),
    vent=RateLos(0.01, 10),
    market_share=15.0
)
