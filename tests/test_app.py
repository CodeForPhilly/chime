from datetime import date
import pandas as pd  # type: ignore
import numpy as np  # type: ignore

EPSILON = 1.e-7

# set up

# we just want to verify that st _attempted_ to render the right stuff
# so we store the input, and make sure that it matches what we expect


def test_defaults_repr(DEFAULTS):
    """
    Test DEFAULTS.repr
    """
    repr(DEFAULTS)
    # TODO: Add assertions here


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
    assert list(model.dispositions_df.iloc[0, :]) == [-43, date(year=2020, month=2, day=14), 1.0, 0.4, 0.2]
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
    assert (raw_df.recovered  [1:] - raw_df.recovered.  shift(1)[1:] >= 0).all()


def test_model_cumulative_census(param, model):
    # test that census is being properly calculated
    raw_df = model.raw_df
    admits_df = model.admits_df
    df = pd.DataFrame({
        "hospitalized": admits_df.hospitalized,
        "icu": admits_df.icu,
        "ventilated": admits_df.ventilated
    })
    admits = df.cumsum()

    # TODO: is 1.0 for ceil function?
    diff = admits.hospitalized[1:-1] - (
        0.05 * 0.05 * (raw_df.infected[1:-1] + raw_df.recovered[1:-1]) - 1.0
    )
    assert (diff.abs() < 0.1).all()
