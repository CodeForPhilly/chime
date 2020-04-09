"""design pattern via https://youtu.be/S_ipdVNSFlo?t=2153"""

from typing import Optional
from datetime import date

from .base import Validator

EPSILON = 1.e-7


class OptionalValue(Validator):
    """Any value at all"""
    def __init__(self) -> None:
        pass

    def validate(self, key, value):
        pass


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

    def validate(self, key, value):
        """This method implicitly validates isinstance(value, (float, int)) because it will throw a TypeError on comparison"""
        if value is None:
            raise ValueError(f"{key} is required.")
        if (self.upper_bound is not None and value > self.upper_bound) \
           or (self.lower_bound is not None and value < self.lower_bound):
            raise ValueError(f"{key}: {value} needs to be {self.message[(self.lower_bound, self.upper_bound)]}.")


class OptionalBounded(Bounded):
    """a bounded number or a None."""
    def __init__(
            self,
            lower_bound: Optional[float] = None,
            upper_bound: Optional[float] = None) -> None:
        super().__init__(lower_bound=lower_bound, upper_bound=upper_bound)

    def validate(self, key, value):
        if value is None:
            return None
        super().validate(key, value)


class Rate(Validator):
    """A rate in [0,1]."""
    def __init__(self) -> None:
        pass

    def validate(self, key, value):
        if value is None:
            raise ValueError(f"{key} is required.")
        if 0.0 > value or value > 1.0:
            raise ValueError(
                f"{key}: {value} needs to be a rate (i.e. in [0,1]).")


class Date(Validator):
    """A date."""
    def __init__(self) -> None:
        pass

    def validate(self, key, value):
        if value is None:
            raise ValueError(f"{key} is required.")
        if not isinstance(value, (date,)):
            raise ValueError(f"{key}: {value} must be a date.")


class OptionalDate(Date):
    def __init__(self) -> None:
        super().__init__()

    def validate(self, key, value):
        if value is None:
            return None
        super().validate(key, value)


class ValDisposition(Validator):
    def __init__(self) -> None:
        pass

    def validate(self, key, value):
        if value is None:
            raise ValueError(f"{key} is required.")
        Bounded(lower_bound=EPSILON)(key=key + '_days', value=value.days)
        Rate()(key=key + '_rate', value=value.rate)
