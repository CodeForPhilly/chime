"""Tests."""

import pytest  # type: ignore
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
import altair as alt  # type: ignore

from src.penn_chime.charts import new_admissions_chart, admitted_patients_chart
from src.penn_chime.models import sir, sim_sir
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
        n_days=60
    )


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
    display_header(st, PARAM)
    assert len(
        list(filter(lambda s: penn_css in s, st.render_store))
    ), "The Penn Medicine header should be printed"


def test_the_rest_of_header_shows_up():
    random_part_of_header = "implying an effective $R_t$ of"
    assert len(
        list(filter(lambda s: random_part_of_header in s, st.render_store))
    ), "The whole header should render"


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
    sim_sir_test = sim_sir(5, 6, 7, 0.1, 0.1, 40)
    s, i, r = sim_sir_test

    assert round(s[0], 0) == 5
    assert round(i[0], 2) == 6
    assert round(r[0], 0) == 7
    assert round(s[-1], 2) == 0
    assert round(i[-1], 2) == 0.18
    assert round(r[-1], 2) == 17.82

    assert isinstance(sim_sir_test, tuple)
    for v in sim_sir_test:
        assert isinstance(v, np.ndarray)


def test_new_admissions_chart():
    projection_admits = pd.read_csv('tests/projection_admits.csv')
    chart = new_admissions_chart(alt, projection_admits, PARAM)
    assert isinstance(chart, alt.Chart)
    assert chart.data.iloc[1].hosp < 1
    assert round(chart.data.iloc[40].icu, 0) == 25

    # test fx call with no params
    with pytest.raises(TypeError):
        new_admissions_chart()

    empty_chart = new_admissions_chart(alt, pd.DataFrame(), PARAM)
    assert empty_chart.data.empty


def test_admitted_patients_chart():
    census_df = pd.read_csv('tests/census_df.csv')
    chart = admitted_patients_chart(alt, census_df, PARAM)
    assert isinstance(chart, alt.Chart)
    assert chart.data.iloc[1].hosp == 1
    assert chart.data.iloc[49].vent == 203

    # test fx call with no params
    with pytest.raises(TypeError):
        admitted_patients_chart()

    empty_chart = admitted_patients_chart(alt, pd.DataFrame(), PARAM)
    assert empty_chart.data.empty


def test_parameters():
    param = Parameters(
        current_hospitalized=100,
        doubling_time=6.0,
        known_infected=5000,
        market_share=0.05,
        relative_contact_rate=0.15,
        susceptible=500000,
        hospitalized=RateLos(0.05, 7),
        icu=RateLos(0.02, 9),
        ventilated=RateLos(0.01, 10),
        n_days=60
    )

    # test the Parameters

    # hospitalized, icu, ventilated
    assert param.rates == (0.05, 0.02, 0.01)
    assert param.lengths_of_stay == (7, 9, 10)

    assert param.infected == 40000.0
    assert isinstance(param.infected, float)  # based off note in models.py

    # test the class-calculated attributes
    assert param.detection_probability == 0.125
    assert param.intrinsic_growth_rate == 0.12246204830937302
    assert param.beta == 3.2961405355450555e-07
    assert param.r_t == 2.307298374881539
    assert param.r_naught == 2.7144686763312222
    assert param.doubling_time_t == 7.764405988534983

    # test the things n_days creates, which in turn tests sim_sir, sir, and get_dispositions
    assert len(param.susceptible_v) == len(param.infected_v) == len(param.recovered_v) == param.n_days + 1 == 61

    assert param.susceptible_v[0] == 500000.0
    assert round(param.susceptible_v[-1], 0) == 67202
    assert round(param.infected_v[1], 0) == 43735
    assert round(param.recovered_v[30], 0) == 224048
    assert [d[0] for d in param.dispositions] == [100.0, 40.0, 20.0]
    assert [round(d[-1], 0) for d in param.dispositions] == [115.0, 46.0, 23.0]

    # change n_days, make sure it cascades
    param.n_days = 2
    assert len(param.susceptible_v) == len(param.infected_v) == len(param.recovered_v) == param.n_days + 1 == 3
