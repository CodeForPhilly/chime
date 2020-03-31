"""the callable validator design pattern"""

from .validators import Bounded, Rate

EPSILON = 1.e-7

StrictlyPositive = Bounded(lower_bound=EPSILON)
Positive = Bounded(lower_bound=-EPSILON)
Rate = Rate()  # type: ignore
