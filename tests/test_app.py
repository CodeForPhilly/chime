"""Tests."""

from copy import copy
from math import ceil  # type: ignore
from datetime import date, datetime  # type: ignore
import pytest  # type: ignore
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
import altair as alt  # type: ignore

from src.penn_chime.charts import (
    build_admits_chart,
    build_census_chart,
    build_descriptions,
)
from src.penn_chime.models import (
    SimSirModel as Model,
    sir,
    sim_sir_df,
    build_admits_df,
    get_growth_rate,
)
from src.penn_chime.parameters import (
    Parameters,
    Disposition,
    Regions,
)
from src.penn_chime.presentation import display_header

EPSILON = 1.e-7

# The defaults in settings will change and break the tests
DEFAULTS = Parameters(
    region=Regions(
        delaware=564696,
        chester=519293,
        montgomery=826075,
        bucks=628341,
        philly=1581000,
    ),
    current_date=datetime(year=2020, month=3, day=28),
    current_hospitalized=14,
    date_first_hospitalized=datetime(year=2020, month=3, day=7),
    doubling_time=4.0,
    n_days=60,
    market_share=0.15,
    relative_contact_rate=0.3,
    hospitalized=Disposition(0.025, 7),
    icu=Disposition(0.0075, 9),
    ventilated=Disposition(0.005, 10),
)

PARAM = Parameters(
    current_date=datetime(year=2020, month=3, day=28),
    current_hospitalized=100,
    doubling_time=6.0,
    market_share=0.05,
    relative_contact_rate=0.15,
    population=500000,
    hospitalized=Disposition(0.05, 7),
    icu=Disposition(0.02, 9),
    ventilated=Disposition(0.01, 10),
    n_days=60,
)

HALVING_PARAM = Parameters(
    current_date=datetime(year=2020, month=3, day=28),
    current_hospitalized=100,
    doubling_time=6.0,
    market_share=0.05,
    relative_contact_rate=0.7,
    population=500000,
    hospitalized=Disposition(0.05, 7),
    icu=Disposition(0.02, 9),
    ventilated=Disposition(0.01, 10),
    n_days=60,
)

MODEL = Model(copy(PARAM))
HALVING_MODEL = Model(copy(HALVING_PARAM))


# set up

# we just want to verify that st _attempted_ to render the right stuff
# so we store the input, and make sure that it matches what we expect
class MockStreamlit:
    def __init__(self):
        self.render_store = []
        self.markdown = self.just_store_instead_of_rendering
        self.latex = self.just_store_instead_of_rendering
        self.subheader = self.just_store_instead_of_rendering

    def just_store_instead_of_rendering(self, inp, *args, **kwargs):
        self.render_store.append(inp)
        return None

    def cleanup(self):
        """
        Call this after every test, unless you intentionally want to accumulate stuff-to-render
        """
        self.render_store = []


st = MockStreamlit()


# test presentation


def header_test_helper(expected_str, model, param):
    st.cleanup()
    display_header(st, model, param)
    assert [s for s in st.render_store if expected_str in s],\
        "Expected the string '{expected}' in the display header".format(expected=expected_str)
    st.cleanup()


def test_penn_logo_in_header():
    penn_css = '<link rel="stylesheet" href="https://www1.pennmedicine.org/styles/shared/penn-medicine-header.css">'
    header_test_helper(penn_css, MODEL, PARAM)


def test_the_rest_of_header_shows_up():
    random_part_of_header = "implying an effective $R_t$ of"
    header_test_helper(random_part_of_header, MODEL, PARAM)


def test_mitigation_statement():
    expected_doubling = "outbreak **reduces the doubling time to 7.8** days"
    expected_halving = "outbreak **halves the infections every 51.9** days"
    header_test_helper(expected_doubling, MODEL, PARAM)
    header_test_helper(expected_halving, HALVING_MODEL, HALVING_PARAM)


def test_growth_rate():
    initial_growth = "and daily growth rate of **12.25%**."
    mitigated_growth = "and daily growth rate of **9.34%**."
    mitigated_halving = "and daily growth rate of **-1.33%**."
    header_test_helper(initial_growth, MODEL, PARAM)
    header_test_helper(mitigated_growth, MODEL, PARAM)
    header_test_helper(mitigated_halving, HALVING_MODEL, HALVING_PARAM)


st.cleanup()


@pytest.mark.xfail()
def test_header_fail():
    """
    Just proving to myself that these tests work
    """
    some_garbage = "ajskhlaeHFPIQONOI8QH34TRNAOP8ESYAW4"
    display_header(st, PARAM)
    assert len(
        list(filter(lambda s: some_garbage in s, st.render_store))
    ), "This should fail"
    st.cleanup()


def test_defaults_repr():
    """
    Test DEFAULTS.repr
    """
    repr(DEFAULTS)


# Test the math


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
        5, # s
        6, # i
        7, # r
        0.1, # gamma
        0, # i_day
        0.1, # beta1
        40, # n_days1
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


def test_admits_chart():
    admits_df = pd.read_csv("tests/by_doubling_time/2020-03-28_projected_admits.csv")
    chart = build_admits_chart(alt=alt, admits_df=admits_df)
    assert isinstance(chart, (alt.Chart, alt.LayerChart))
    assert round(chart.data.iloc[40].icu, 0) == 38

    # test fx call with no params
    with pytest.raises(TypeError):
        build_admits_chart()


def test_census_chart():
    census_df = pd.read_csv("tests/by_doubling_time/2020-03-28_projected_census.csv")
    chart = build_census_chart(alt=alt, census_df=census_df)
    assert isinstance(chart, (alt.Chart, alt.LayerChart))
    assert chart.data.iloc[1].hospitalized == 3
    assert chart.data.iloc[49].ventilated == 365

    # test fx call with no params
    with pytest.raises(TypeError):
        build_census_chart()


def test_model():
    # test the Model
    param = copy(PARAM)
    model = Model(param)

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


def test_model_raw_start():
    param = copy(PARAM)
    model = Model(param)
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


def test_model_conservation():
    p = copy(PARAM)
    m = Model(p)
    raw_df = m.raw_df

    assert (0.0 <= raw_df.susceptible).all()
    assert (0.0 <= raw_df.infected).all()
    assert (0.0 <= raw_df.recovered).all()

    diff = raw_df.susceptible + raw_df.infected + raw_df.recovered - p.population
    assert (diff < 0.1).all()

    assert (raw_df.susceptible <= p.population).all()
    assert (raw_df.infected <= p.population).all()
    assert (raw_df.recovered <= p.population).all()


def test_model_raw_end():
    param = copy(PARAM)
    model = Model(param)
    raw_df = model.raw_df

    last = raw_df.iloc[-1, :]
    assert round(last.susceptible, 0) == 83391.0


def test_model_monotonicity():
    param = copy(PARAM)
    model = Model(param)
    raw_df = model.raw_df

    # Susceptible population should be non-increasing, and Recovered non-decreasing
    assert (raw_df.susceptible[1:] - raw_df.susceptible.shift(1)[1:] <= 0).all()
    assert (raw_df.recovered  [1:] - raw_df.recovered.  shift(1)[1:] >= 0).all()


def test_model_cumulative_census():
    # test that census is being properly calculated
    param = copy(PARAM)
    model = Model(param)

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


def test_growth_rate():
    assert np.round(get_growth_rate(5) * 100.0, decimals=4) == 14.8698
    assert np.round(get_growth_rate(0) * 100.0, decimals=4) == 0.0
    assert np.round(get_growth_rate(-4) * 100.0, decimals=4) == -15.9104


def test_build_descriptions():
    param = copy(PARAM)

    admits_file = 'tests/by_doubling_time/2020-03-28_projected_admits.csv'
    census_file = 'tests/by_doubling_time/2020-03-28_projected_census.csv'

    admits_df = pd.read_csv(admits_file, parse_dates=['date'])
    chart = build_admits_chart(alt=alt, admits_df=admits_df)
    description = build_descriptions(chart=chart, labels=param.labels)

    hosp, icu, vent = description.split("\n\n")  # break out the description into lines

    max_hosp = chart.data['hospitalized'].max()
    assert str(ceil(max_hosp)) in hosp

    # TODO add test for asterisk

    # test no asterisk
    param.n_days = 600

    admits_df = pd.read_csv(admits_file, parse_dates=['date'])
    chart = build_admits_chart(alt=alt, admits_df=admits_df)
    description = build_descriptions(chart=chart, labels=param.labels)
    assert "*" not in description


    # census chart
    census_df = pd.read_csv(census_file, parse_dates=['date'])
    chart = build_census_chart(alt=alt, census_df=census_df)
    description = build_descriptions(chart=chart, labels=param.labels)

    assert str(ceil(chart.data['ventilated'].max())) in description
    assert str(chart.data['icu'].idxmax()) not in description
    assert datetime.strftime(chart.data.iloc[chart.data['icu'].idxmax()].date, '%b %d') in description
