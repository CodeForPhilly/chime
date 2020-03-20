#!/usr/bin/env python
"""Set defaults for your fork/locality here

   after we merge this in we can set defaults in a `config/env` type of file
"""

from collections import namedtuple

# (0.02, 7) is 2%, 7 days
# be sure to multiply by 100 when using as a default to the pct widgets!
RateLos = namedtuple('RateLos', ('rate', 'length_of_stay'))

class Regions:
    """Arbitrary number of counties."""
    def __init__(self, **kwargs):
        s = 0
        for key, value in kwargs.items():
            setattr(self, key, value)
            s += value
        self._s = s

    @property
    def s(self):
        return self._s


class Constants:
    def __init__(self,
                 region: Regions,
                 known_infections: int,
                 known_cases: int,
                 doubling_time: int,
                 relative_contact_rate: int,
                 hosp: RateLos,
                 icu: RateLos,
                 vent: RateLos,
                 market_share: float
    ):
        self.region = region
        self.known_infections = known_infections
        self.known_cases = known_cases
        self.doubling_time = doubling_time
        self.relative_contact_rate = relative_contact_rate
        self.hosp = hosp
        self.icu = icu
        self.vent = vent
        self.market_share = market_share

    def __repr__(self) -> str:
        return f"Constants(susceptible_default: {self.region.s}, known_infections: {self.known_infections})"

