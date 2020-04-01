from datetime import date

import pytest
import pandas as pd
import numpy as np

from src.penn_chime.models import (
    sir,
    sim_sir_df,
    get_growth_rate,
)

from src.penn_chime.constants import EPSILON


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


def test_model(model, param):
    # test the Model

    assert round(model.infected, 0) == 45810.0
    assert isinstance(model.infected, float)  # based off note in models.py

    # test the class-calculated attributes
    # we're talking about getting rid of detection probability
    # assert model.detection_probability == 0.125
    assert model.intrinsic_growth_rate == 0.12246204830937302
    assert abs(model.beta - 4.21501347256401e-07) < EPSILON
    assert model.r_t == 2.307298374881539
    assert model.r_naught == 2.7144686763312222
    assert model.doubling_time_t == 7.764405988534983


def test_model_raw_start(model, param):
    raw_df = model.raw_df

    # test the things n_days creates, which in turn tests sim_sir, sir, and get_dispositions

    # print('n_days: %s; i_day: %s' % (param.n_days, model.i_day))
    assert len(raw_df) == (len(np.arange(-model.i_day, param.n_days + 1))) == 104

    first = raw_df.iloc[0, :]
    second = raw_df.iloc[1, :]

    assert first.susceptible == 499600.0
    assert round(second.infected, 0) == 449.0
    assert list(model.dispositions_df.iloc[0, :]) == [
        -43,
        date(year=2020, month=2, day=14),
        1.0,
        0.4,
        0.2,
    ]
    assert round(raw_df.recovered[30], 0) == 7083.0

    d, dt, s, i, r = list(model.dispositions_df.iloc[60, :])
    assert dt == date(year=2020, month=4, day=14)
    assert [round(v, 0) for v in (d, s, i, r)] == [17, 549.0, 220.0, 110.0]


def test_model_conservation(param, model):
    raw_df = model.raw_df

    assert (0.0 <= raw_df.susceptible).all()
    assert (0.0 <= raw_df.infected).all()
    assert (0.0 <= raw_df.recovered).all()

    diff = raw_df.susceptible + raw_df.infected + raw_df.recovered - param.population
    assert (diff < 0.1).all()

    assert (raw_df.susceptible <= param.population).all()
    assert (raw_df.infected <= param.population).all()
    assert (raw_df.recovered <= param.population).all()


def test_model_raw_end(param, model):
    raw_df = model.raw_df
    last = raw_df.iloc[-1, :]
    assert round(last.susceptible, 0) == 83391.0


def test_model_monotonicity(param, model):
    raw_df = model.raw_df

    # Susceptible population should be non-increasing, and Recovered non-decreasing
    assert (raw_df.susceptible[1:] - raw_df.susceptible.shift(1)[1:] <= 0).all()
    assert (raw_df.recovered[1:] - raw_df.recovered.shift(1)[1:] >= 0).all()


def test_model_cumulative_census(param, model):
    # test that census is being properly calculated
    raw_df = model.raw_df
    admits_df = model.admits_df
    df = pd.DataFrame(
        {
            "hospitalized": admits_df.hospitalized,
            "icu": admits_df.icu,
            "ventilated": admits_df.ventilated,
        }
    )
    admits = df.cumsum()

    # TODO: is 1.0 for ceil function?
    diff = admits.hospitalized[1:-1] - (
        0.05 * 0.05 * (raw_df.infected[1:-1] + raw_df.recovered[1:-1]) - 1.0
    )
    assert (diff.abs() < 0.1).all()
