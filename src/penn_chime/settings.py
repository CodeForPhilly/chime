#!/usr/bin/env python

from datetime import date

from .parameters import Parameters, Regions, Disposition

DEFAULTS = Parameters(
    region=Regions(
        delaware=564696,
        chester=519293,
        montgomery=826075,
        bucks=628341,
        philly=1581000,
    ),
    current_hospitalized=32,
    date_first_hospitalized=date(2020,3,7),
    doubling_time=4.0,
    hospitalized=Disposition(0.025, 7),
    icu=Disposition(0.0075, 9),
    infectious_days=14,
    market_share=0.15,
    n_days=60,
    relative_contact_rate=0.3,
    ventilated=Disposition(0.005, 10),
)
