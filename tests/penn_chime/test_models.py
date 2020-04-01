import pytest
import pandas as pd
import numpy as np

from src.penn_chime.models import (
    sir,
    sim_sir_df,
    get_growth_rate,
)


def test_sir():
    """
    Someone who is good at testing, help
    """
    sir_test = sir(100, 1, 0, 0.2, 0.5, 1)
    assert sir_test == (
        0.7920792079207921,
        0.20297029702970298,
        0.0049504950495049506,
    ), "This contrived example should work"

    assert isinstance(sir_test, tuple)
    for v in sir_test:
        assert isinstance(v, float)
        assert v >= 0

    # Certain things should *not* work
    with pytest.raises(TypeError) as error:
        sir("S", 1, 0, 0.2, 0.5, 1)
    assert str(error.value) == "can't multiply sequence by non-int of type 'float'"

    with pytest.raises(TypeError) as error:
        sir(100, "I", 0, 0.2, 0.5, 1)
    assert str(error.value) == "can't multiply sequence by non-int of type 'float'"

    with pytest.raises(TypeError) as error:
        sir(100, 1, "R", 0.2, 0.5, 1)
    assert str(error.value) == "unsupported operand type(s) for +: 'float' and 'str'"

    with pytest.raises(TypeError) as error:
        sir(100, 1, 0, "beta", 0.5, 1)
    assert str(error.value) == "bad operand type for unary -: 'str'"

    with pytest.raises(TypeError) as error:
        sir(100, 1, 0, 0.2, "gamma", 1)
    assert str(error.value) == "unsupported operand type(s) for -: 'float' and 'str'"

    with pytest.raises(TypeError) as error:
        sir(100, 1, 0, 0.2, 0.5, "N")
    assert str(error.value) == "unsupported operand type(s) for /: 'str' and 'float'"

    # Zeros across the board should fail
    with pytest.raises(ZeroDivisionError):
        sir(0, 0, 0, 0, 0, 0)


def test_sim_sir():
    """
    Rounding to move fast past decimal place issues
    """
    raw_df = sim_sir_df(
        5, 6, 7, 0.1, 0, 0.1, 40,  # s  # i  # r  # gamma  # i_day  # beta1  # n_days1
    )

    first = raw_df.iloc[0, :]
    last = raw_df.iloc[-1, :]

    assert round(first.susceptible, 0) == 5
    assert round(first.infected, 2) == 6
    assert round(first.recovered, 0) == 7
    assert round(last.susceptible, 2) == 0
    assert round(last.infected, 2) == 0.18
    assert round(last.recovered, 2) == 17.82

    assert isinstance(raw_df, pd.DataFrame)


def test_growth_rate():
    assert np.round(get_growth_rate(5) * 100.0, decimals=4) == 14.8698
    assert np.round(get_growth_rate(0) * 100.0, decimals=4) == 0.0
    assert np.round(get_growth_rate(-4) * 100.0, decimals=4) == -15.9104
