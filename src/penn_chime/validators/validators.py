"""design pattern via https://youtu.be/S_ipdVNSFlo?t=2153"""

from typing import Optional

from .base import Validator


class Bounded(Validator):

    def __init__(
            self,
            lower_bound: Optional[float] = None,
            upper_bound: Optional[float] = None) -> None:
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.message = {
            (lower_bound, upper_bound): f"in ({self.lower_bound}, {self.upper_bound})",
            (None, upper_bound): f"less than {self.upper_bound}",
            (lower_bound, None): f"greater than {self.lower_bound}",
            (None, None): "ACTUALLY the value is unbounded"
        }

    def validate(self, value):
        if (self.upper_bound is not None and value > self.upper_bound) \
           or (self.lower_bound is not None and value < self.lower_bound):
            raise ValueError(f"{value} needs to be {self.message[(self.lower_bound, self.upper_bound)]}.")


class Rate(Validator):
    def __init__(self) -> None:
        pass
   
    def validate(self, value):
        if 0 >= value or value >= 1:
            raise ValueError(f"{value} needs to be a rate (i.e. in [0,1])")

