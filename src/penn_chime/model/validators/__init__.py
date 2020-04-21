"""the callable validator design pattern"""

from ...constants import EPSILON
from .validators import (
    OptionalValue as ValOptionalValue,
    Bounded as ValBounded,
    OptionalBounded as ValOptionalBounded,
    Rate as ValRate,
    Date as ValDate,
    OptionalDate as ValOptionalDate,
    ValDisposition as ValValDisposition,
)

OptionalValue = ValOptionalValue()
OptionalStrictlyPositive = ValOptionalBounded(lower_bound=EPSILON)
StrictlyPositive = ValBounded(lower_bound=EPSILON)
Positive = ValBounded(lower_bound=-EPSILON)
GteOne = ValBounded(lower_bound=1)
Rate = ValRate()
Date = ValDate()
OptionalDate = ValOptionalDate()
ValDisposition = ValValDisposition()
# # rolling a custom validator for doubling time in case DS wants to add upper bound
# DoublingTime = OptionalBounded(lower_bound=0-EPSILON, upper_bound=None)
