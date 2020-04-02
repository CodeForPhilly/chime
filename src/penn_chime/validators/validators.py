"""design pattern via https://youtu.be/S_ipdVNSFlo?t=2153"""

from typing import Optional
from datetime import date, datetime

from .base import Validator


class Bounded(Validator):
    """A bounded number."""
    def __init__(
            self,
            lower_bound: Optional[float] = None,
            upper_bound: Optional[float] = None) -> None:
        assert lower_bound is not None or upper_bound is not None, "Do not use this object to create an unbounded validator."
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.message = {
            (lower_bound, upper_bound): f"in ({self.lower_bound}, {self.upper_bound})",
            (None, upper_bound): f"less than {self.upper_bound}",
            (lower_bound, None): f"greater than {self.lower_bound}",
        }

    def validate(self, value):
        """This method implicitly validates isinstance(value, (float, int)) because it will throw a TypeError on comparison"""
        if (self.upper_bound is not None and value > self.upper_bound) \
           or (self.lower_bound is not None and value < self.lower_bound):
            raise ValueError(f"{value} needs to be {self.message[(self.lower_bound, self.upper_bound)]}.")


class OptionalBounded(Bounded):
    """a bounded number or a None."""
    def __init__(
            self,
            lower_bound: Optional[float] = None,
            upper_bound: Optional[float] = None) -> None:
        super().__init__(lower_bound=lower_bound, upper_bound=upper_bound)

    def validate(self, value):
        if value is None:
            return None
        super().validate(value)

class Rate(Validator):
    """A rate in [0,1]."""
    def __init__(self) -> None:
        pass
   
    def validate(self, value):
        if 0 > value or value > 1:
            raise ValueError(f"{value} needs to be a rate (i.e. in [0,1]).")

class Date(Validator):
    """A date of some sort."""
    def __init__(self) -> None:
        pass

    def validate(self, value):
        if not isinstance(value, (date, datetime)):
            raise (ValueError(f"{value} must be a date or datetime object."))

class OptionalDate(Date):
    def __init__(self) -> None:
        super().__init__()

    def validate(self, value):
        if value is None:
            return None
        super().validate(value)
