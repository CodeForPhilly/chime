from datetime import datetime

import pytest
import pandas as pd

from src.penn_chime.parameters import (
    Parameters,
    Disposition,
    Regions,
)
from src.penn_chime.models import SimSirModel, build_floor_df


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


@pytest.fixture
def defaults():
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
        hospitalized=Disposition.create(rate=0.025, days=7),
        icu=Disposition.create(rate=0.0075, days=9),
        infectious_days=14,
        n_days=60,
        market_share=0.15,
        mitigation_date=datetime(year=2020, month=3, day=28),
        recovered=0,
        relative_contact_rate=0.3,
        ventilated=Disposition.create(rate=0.005, days=10),
    )


@pytest.fixture
def param():
    return Parameters(
        current_date=datetime(year=2020, month=3, day=28),
        current_hospitalized=100,
        doubling_time=6.0,
        hospitalized=Disposition.create(rate=0.05, days=7),
        infectious_days=14,
        icu=Disposition.create(rate=0.02, days=9),
        market_share=0.05,
        mitigation_date=datetime(year=2020, month=3, day=28),
        n_days=60,
        population=500000,
        recovered=0,
        relative_contact_rate=0.15,
        ventilated=Disposition.create(rate=0.01, days=10),
    )


@pytest.fixture
def halving_param():
    return Parameters(
        current_date=datetime(year=2020, month=3, day=28),
        current_hospitalized=100,
        doubling_time=6.0,
        hospitalized=Disposition.create(rate=0.05, days=7),
        icu=Disposition.create(rate=0.02, days=9),
        infectious_days=14,
        market_share=0.05,
        mitigation_date=datetime(year=2020, month=3, day=28),
        n_days=60,
        population=500000,
        recovered=0,
        relative_contact_rate=0.7,
        ventilated=Disposition.create(rate=0.01, days=10),
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
def admits_floor_df(param, admits_df):
    return build_floor_df(admits_df, param.dispositions.keys(), "admits_")


@pytest.fixture
def census_df():
    return pd.read_csv(
        "tests/by_doubling_time/2020-03-28_projected_census.csv", parse_dates=["date"]
    )

@pytest.fixture
def census_floor_df(param, census_df):
    return build_floor_df(census_df, param.dispositions.keys(), "census_")

