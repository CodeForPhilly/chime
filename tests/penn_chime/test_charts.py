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


def test_admits_chart(admits_df):
    chart = build_admits_chart(alt=alt, admits_df=admits_df)
    assert isinstance(chart, (alt.Chart, alt.LayerChart))
    assert round(chart.data.iloc[40].icu, 0) == 39

    # test fx call with no params
    with pytest.raises(TypeError):
        build_admits_chart()


def test_build_descriptions(admits_df, param):
    chart = build_admits_chart(alt=alt, admits_df=admits_df)
    description = build_descriptions(chart=chart, labels=param.labels)

    hosp, icu, vent = description.split("\n\n")  # break out the description into lines

    max_hosp = chart.data["hospitalized"].max()
    assert str(ceil(max_hosp)) in hosp


def test_no_asterisk(admits_df, param):
    param.n_days = 600

    chart = build_admits_chart(alt=alt, admits_df=admits_df)
    description = build_descriptions(chart=chart, labels=param.labels)
    assert "*" not in description


def test_census(census_df, param):
    chart = build_census_chart(alt=alt, census_df=census_df)
    description = build_descriptions(chart=chart, labels=param.labels)

    assert str(ceil(chart.data["ventilated"].max())) in description
    assert str(chart.data["icu"].idxmax()) not in description
    assert (
        datetime.strftime(chart.data.iloc[chart.data["icu"].idxmax()].date, "%b %d")
        in description
    )


def test_census_chart(census_df):
    chart = build_census_chart(alt=alt, census_df=census_df)
    assert isinstance(chart, (alt.Chart, alt.LayerChart))
    assert chart.data.iloc[1].hospitalized == 3
    assert chart.data.iloc[49].ventilated == 365

    # test fx call with no params
    with pytest.raises(TypeError):
        build_census_chart()