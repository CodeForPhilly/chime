import altair as alt
import pytest
import math
import os
import i18n

i18n.set('filename_format', '{locale}.{format}')
i18n.set('locale', 'en')
i18n.set('fallback', 'en')
i18n.load_path.append(os.path.dirname(__file__) + '/../../../src/penn_chime/locales')

from penn_chime.view.charts import (
    build_admits_chart,
    build_census_chart,
)

DISPOSITION_KEYS = ("hospitalized", "icu", "ventilated")

# These are the localized column names for the dataframe sent to the charting library.
admits_icu_key = i18n.t("admits_icu")
admits_hospitalized_key = i18n.t("admits_hospitalized")
admits_ventilated_key = i18n.t("admits_ventilated")
census_icu_key = i18n.t("census_icu")
census_hospitalized_key = i18n.t("census_hospitalized")
census_ventilated_key = i18n.t("census_ventilated")

def test_admits_chart(admits_floor_df):
    chart = build_admits_chart(alt=alt, admits_floor_df=admits_floor_df)
    assert isinstance(chart, (alt.Chart, alt.LayerChart))
    assert round(chart.data.iloc[40][admits_icu_key], 0) == 38

    # test fx call with no params
    with pytest.raises(TypeError):
        build_admits_chart()


def test_census_chart(census_floor_df):
    chart = build_census_chart(alt=alt, census_floor_df=census_floor_df)
    assert isinstance(chart, (alt.Chart, alt.LayerChart))
    assert chart.data.iloc[1][census_hospitalized_key] == 3
    assert chart.data.iloc[49][census_ventilated_key] == 365

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
    assert chart.data.iloc[1][admits_hospitalized_key] == 2
    assert math.isnan(chart.data.iloc[1][admits_icu_key])
    assert math.isnan(chart.data.iloc[1][admits_ventilated_key])

    assert chart.data.iloc[2][admits_hospitalized_key] == 2
    assert math.isnan(chart.data.iloc[2][admits_icu_key])
    assert math.isnan(chart.data.iloc[2][admits_ventilated_key])

    assert chart.data.iloc[3][admits_hospitalized_key] == 3
    assert math.isnan(chart.data.iloc[3][admits_icu_key])
    assert math.isnan(chart.data.iloc[3][admits_ventilated_key])

    assert chart.data.iloc[4][admits_hospitalized_key] == 3
    assert chart.data.iloc[4][admits_icu_key] == 1
    assert math.isnan(chart.data.iloc[4][admits_ventilated_key])

def test_census_chart_log_scale(census_floor_df):
    """
    Verifies that if the log scale is used, then the values on the chart are adjusted appropriately.

    Args:
        census_floor_df: Sample census data.

    """
    chart = build_census_chart(alt=alt, census_floor_df=census_floor_df, use_log_scale=True)

    # We check a few values to verify that zero was replaced with NaN.
    assert math.isnan(chart.data.iloc[0][census_hospitalized_key])
    assert math.isnan(chart.data.iloc[0][census_icu_key])
    assert math.isnan(chart.data.iloc[0][census_ventilated_key])

    assert chart.data.iloc[1][census_hospitalized_key] == 3
    assert chart.data.iloc[1][census_icu_key] == 1
    assert chart.data.iloc[1][census_ventilated_key] == 1

    assert chart.data.iloc[2][census_hospitalized_key] == 6
    assert chart.data.iloc[2][census_icu_key] == 2
    assert chart.data.iloc[2][census_ventilated_key] == 2

