from datetime import datetime

import pytest
import pandas as pd

from src.penn_chime.parameters import (
    Parameters,
    Disposition,
    Regions,
)
from src.penn_chime.models import SimSirModel


class MockStreamlit:
    """Mock implementation of streamlit

    We just want to verify that st _attempted_ to render the right stuff
    so we store the input, and make sure that it matches what we expect
    """

    def __init__(self):
        self.render_store = []
        self.markdown = self.just_store_instead_of_rendering
        self.latex = self.just_store_instead_of_rendering
        self.subheader = self.just_store_instead_of_rendering

    def just_store_instead_of_rendering(self, inp, *args, **kwargs):
        self.render_store.append(inp)
        return None


@pytest.fixture
def mock_st():
    return MockStreamlit()


# The defaults in settings will change and break the tests
@pytest.fixture
def DEFAULTS():
    return Parameters(
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


@pytest.fixture
def param():
    return Parameters(
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


@pytest.fixture
def halving_param():
    return Parameters(
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


@pytest.fixture
def model(param):
    return SimSirModel(param)


@pytest.fixture
def halving_model(halving_param):
    return SimSirModel(halving_param)


@pytest.fixture
def admits_df():
    return pd.read_csv(
        "tests/by_doubling_time/2020-03-28_projected_admits.csv", parse_dates=["date"]
    )


@pytest.fixture
def census_df():
    return pd.read_csv(
        "tests/by_doubling_time/2020-03-28_projected_census.csv", parse_dates=["date"]
    )
