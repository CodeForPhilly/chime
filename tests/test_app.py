"""Tests."""

from math import ceil  # type: ignore
import datetime  # type: ignore
import pytest  # type: ignore
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
import altair as alt  # type: ignore

from src.penn_chime.charts import new_admissions_chart, admitted_patients_chart, chart_descriptions
from src.penn_chime.models import SimSirModel, sir, sim_sir_df, build_admits_df
from src.penn_chime.parameters import Parameters
from src.penn_chime.presentation import display_header
from src.penn_chime.settings import DEFAULTS
from src.penn_chime.defaults import RateLos

PARAM = Parameters(
    current_hospitalized=100,
    doubling_time=6.0,
    known_infected=5000,
    market_share=0.05,
    relative_contact_rate=0.15,
    susceptible=500000,
    hospitalized=RateLos(0.05, 7),
    icu=RateLos(0.02, 9),
    ventilated=RateLos(0.01, 10),
    n_days=60,
)

MODEL = SimSirModel(PARAM)


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


def test_penn_logo_in_header():
    penn_css = '<link rel="stylesheet" href="https://www1.pennmedicine.org/styles/shared/penn-medicine-header.css">'
    display_header(st, MODEL, PARAM)
    assert len(
        list(filter(lambda s: penn_css in s, st.render_store))
    ), "The Penn Medicine header should be printed"


def test_the_rest_of_header_shows_up():
    random_part_of_header = "implying an effective $R_t$ of"
    assert len(
        list(filter(lambda s: random_part_of_header in s, st.render_store))
    ), "The whole header should render"


def test_mitigation_statement():
    st.cleanup()
    expected_doubling = "outbreak **reduces the doubling time to 7.8** days"
    display_header(st, MODEL, PARAM)
    assert [s for s in st.render_store if expected_doubling in s]
    # assert len((list(filter(lambda s: expected_doubling in s, st.render_store))))
    st.cleanup()
    expected_halving = "outbreak **halves the infections every 51.9** days"
    halving_params = Parameters(
        current_hospitalized=100,
        doubling_time=6.0,
        known_infected=5000,
        market_share=0.05,
        relative_contact_rate=0.7,
        susceptible=500000,
        hospitalized=RateLos(0.05, 7),
        icu=RateLos(0.02, 9),
        ventilated=RateLos(0.01, 10),
        n_days=60,
    )
    halving_model = SimSirModel(halving_params)
    display_header(st, halving_model, halving_params)
    assert [s for s in st.render_store if expected_halving in s]
    #assert len((list(filter(lambda s: expected_halving in s, st.render_store))))
    st.cleanup()


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
    raw_df = sim_sir_df(5, 6, 7, 0.1, 0.1, 40)

    first = raw_df.iloc[0, :]
    last = raw_df.iloc[-1, :]

    assert round(first.susceptible, 0) == 5
    assert round(first.infected, 2) == 6
    assert round(first.recovered, 0) == 7
    assert round(last.susceptible, 2) == 0
    assert round(last.infected, 2) == 0.18
    assert round(last.recovered, 2) == 17.82

    assert isinstance(raw_df, pd.DataFrame)


def test_new_admissions_chart():
    projection_admits = pd.read_csv("tests/projection_admits.csv")
    chart = new_admissions_chart(alt, projection_admits, PARAM)
    assert isinstance(chart, alt.Chart)
    assert chart.data.iloc[1].hospitalized < 1
    assert round(chart.data.iloc[40].icu, 0) == 25

    # test fx call with no params
    with pytest.raises(TypeError):
        new_admissions_chart()

    empty_chart = new_admissions_chart(alt, pd.DataFrame(), PARAM)
    assert empty_chart.data.empty


def test_admitted_patients_chart():
    census_df = pd.read_csv("tests/census_df.csv")
    chart = admitted_patients_chart(alt, census_df, PARAM)
    assert isinstance(chart, alt.Chart)
    assert chart.data.iloc[1].hospitalized == 1
    assert chart.data.iloc[49].ventilated == 203

    # test fx call with no params
    with pytest.raises(TypeError):
        admitted_patients_chart()

    empty_chart = admitted_patients_chart(alt, pd.DataFrame(), PARAM)
    assert empty_chart.data.empty


def test_model(model=MODEL, param=PARAM):
    # test the Model

    assert model.infected == 40000.0
    assert isinstance(model.infected, float)  # based off note in models.py

    # test the class-calculated attributes
    assert model.detection_probability == 0.125
    assert model.intrinsic_growth_rate == 0.12246204830937302
    assert model.beta == 3.2961405355450555e-07
    assert model.r_t == 2.307298374881539
    assert model.r_naught == 2.7144686763312222
    assert model.doubling_time_t == 7.764405988534983

    # test the things n_days creates, which in turn tests sim_sir, sir, and get_dispositions
    assert len(model.raw_df) == param.n_days + 1 == 61

    raw_df = model.raw_df
    first = raw_df.iloc[0, :]
    second = raw_df.iloc[1, :]
    last = raw_df.iloc[-1, :]

    assert first.susceptible == 500000.0
    assert round(second.infected, 0) == 43735

    assert round(last.susceptible, 0) == 67202
    assert round(raw_df.recovered[30], 0) == 224048

    assert [d[0] for d in model.dispositions.values()] == [100.0, 40.0, 20.0]
    assert [round(d[60], 0) for d in model.dispositions.values()] == [1182.0, 473.0, 236.0]

    # test that admissions are being properly calculated (thanks @PhilMiller)
    admissions = build_admits_df(param.n_days, model.dispositions)
    cumulative_admissions = admissions.cumsum()
    diff = cumulative_admissions["hospitalized"][1:-1] - (
        0.05 * 0.05 * (raw_df.infected[1:-1] + raw_df.recovered[1:-1]) - 100
    )
    assert (diff.abs() < 0.1).all()


def test_chart_descriptions(p=PARAM):
    # new admissions chart
    projection_admits = pd.read_csv('tests/projection_admits.csv')
    chart = new_admissions_chart(alt, projection_admits, p)
    description = chart_descriptions(chart, p.labels)

    hosp, icu, vent, asterisk = description.split("\n\n")  # break out the description into lines

    max_hosp = chart.data['hospitalized'].max()
    assert str(ceil(max_hosp)) in hosp

    max_icu_ix = chart.data['icu'].idxmax()
    assert max_icu_ix + 1 == len(chart.data)
    assert "*" in icu

    # test asterisk
    param = PARAM
    param.n_days = 600

    projection_admits = pd.read_csv('tests/projection_admits.csv')
    # projection_admits = projection_admits.rename(columns={'hospitalized': 'Hospitalized', 'icu': 'ICU', 'ventilated': 'Ventilated'})
    chart = new_admissions_chart(alt, projection_admits, p)
    description = chart_descriptions(chart, p.labels)
    assert "*" not in description

    # census chart
    census_df = pd.read_csv('tests/census_df.csv')
    # census_df = census_df.rename(columns={'hospitalized': 'Hospitalized', 'icu': 'ICU', 'ventilated': 'Ventilated'})
    PARAM.as_date = True
    chart = admitted_patients_chart(alt, census_df, p)
    description = chart_descriptions(chart, p.labels)

    assert str(ceil(chart.data['ventilated'].max())) in description
    assert str(chart.data['icu'].idxmax()) not in description
    assert datetime.datetime.strftime(chart.data.iloc[chart.data['icu'].idxmax()].date, '%b %d') in description
