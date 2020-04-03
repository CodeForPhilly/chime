from math import ceil
from datetime import datetime

import altair as alt
import pytest

from src.penn_chime.charts import (
    build_admits_chart,
    build_census_chart,
    build_descriptions,
)

# TODO add test for asterisk


DISPOSITION_KEYS = ("hospitalized", "icu", "ventilated")


def test_admits_chart(admits_floor_df):
    chart = build_admits_chart(alt=alt, admits_floor_df=admits_floor_df)
    assert isinstance(chart, (alt.Chart, alt.LayerChart))
    assert round(chart.data.iloc[40].admits_icu, 0) == 38

    # test fx call with no params
    with pytest.raises(TypeError):
        build_admits_chart()


def test_build_descriptions(admits_floor_df, param):
    chart = build_admits_chart(alt=alt, admits_floor_df=admits_floor_df)
    description = build_descriptions(chart=chart, labels=param.labels, prefix="admits_")

    hosp, icu, vent = description.split("\n\n")  # break out the description into lines

    max_hosp = chart.data["admits_hospitalized"].max()
    assert str(ceil(max_hosp)) in hosp


def test_no_asterisk(admits_floor_df, param):
    param.n_days = 600

    chart = build_admits_chart(alt=alt, admits_floor_df=admits_floor_df)
    description = build_descriptions(chart=chart, labels=param.labels, prefix="admits_")
    assert "*" not in description


def test_census(census_floor_df, param):
    chart = build_census_chart(alt=alt, census_floor_df=census_floor_df)
    description = build_descriptions(chart=chart, labels=param.labels, prefix="census_")

    assert str(ceil(chart.data["census_ventilated"].max())) in description
    assert str(chart.data["census_icu"].idxmax()) not in description
    assert (
        datetime.strftime(chart.data.iloc[chart.data["census_icu"].idxmax()].date, "%b %d")
        in description
    )


def test_census_chart(census_floor_df):
    chart = build_census_chart(alt=alt, census_floor_df=census_floor_df)
    assert isinstance(chart, (alt.Chart, alt.LayerChart))
    assert chart.data.iloc[1].census_hospitalized == 3
    assert chart.data.iloc[49].census_ventilated == 365

    # test fx call with no params
    with pytest.raises(TypeError):
        build_census_chart()
