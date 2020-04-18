import altair as alt
import pytest
import math

from penn_chime.view.charts import (
    build_admits_chart,
    build_census_chart,
)

DISPOSITION_KEYS = ("hospitalized", "icu", "ventilated")

def test_admits_chart(admits_floor_df):
    chart = build_admits_chart(alt=alt, admits_floor_df=admits_floor_df)
    assert isinstance(chart, (alt.Chart, alt.LayerChart))
    assert round(chart.data.iloc[40].admits_icu, 0) == 38

    # test fx call with no params
    with pytest.raises(TypeError):
        build_admits_chart()


def test_census_chart(census_floor_df):
    chart = build_census_chart(alt=alt, census_floor_df=census_floor_df)
    assert isinstance(chart, (alt.Chart, alt.LayerChart))
    assert chart.data.iloc[1].census_hospitalized == 3
    assert chart.data.iloc[49].census_ventilated == 365

    # test fx call with no params
    with pytest.raises(TypeError):
        build_census_chart()

def test_admits_chart_log_scale(admits_floor_df):
    """
    Verifies that if the log scale is used, then the values on the chart are adjusted appropriately.

    Args:
        admits_floor_df: Sample admission data.

    """
    chart = build_admits_chart(alt=alt, admits_floor_df=admits_floor_df, use_log_scale=True)

    # We check a few values to verify that zero was replaced with NaN.
    assert chart.data.iloc[1].admits_hospitalized == 2
    assert math.isnan(chart.data.iloc[1].admits_icu)
    assert math.isnan(chart.data.iloc[1].admits_ventilated)

    assert chart.data.iloc[2].admits_hospitalized == 2
    assert math.isnan(chart.data.iloc[2].admits_icu)
    assert math.isnan(chart.data.iloc[2].admits_ventilated)

    assert chart.data.iloc[3].admits_hospitalized == 3
    assert math.isnan(chart.data.iloc[3].admits_icu)
    assert math.isnan(chart.data.iloc[3].admits_ventilated)

    assert chart.data.iloc[4].admits_hospitalized == 3
    assert chart.data.iloc[4].admits_icu == 1
    assert math.isnan(chart.data.iloc[4].admits_ventilated)

def test_census_chart_log_scale(census_floor_df):
    """
    Verifies that if the log scale is used, then the values on the chart are adjusted appropriately.

    Args:
        census_floor_df: Sample census data.

    """
    chart = build_census_chart(alt=alt, census_floor_df=census_floor_df, use_log_scale=True)

    # We check a few values to verify that zero was replaced with NaN.
    assert math.isnan(chart.data.iloc[0].census_hospitalized)
    assert math.isnan(chart.data.iloc[0].census_icu)
    assert math.isnan(chart.data.iloc[0].census_ventilated)

    assert chart.data.iloc[1].census_hospitalized == 3
    assert chart.data.iloc[1].census_icu == 1
    assert chart.data.iloc[1].census_ventilated == 1

    assert chart.data.iloc[2].census_hospitalized == 6
    assert chart.data.iloc[2].census_icu == 2
    assert chart.data.iloc[2].census_ventilated == 2

