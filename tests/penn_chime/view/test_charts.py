import altair as alt
import pytest
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

def test_admits_chart(admits_floor_df):
    chart = build_admits_chart(alt=alt, admits_floor_df=admits_floor_df)
    assert isinstance(chart, (alt.Chart, alt.LayerChart))
    assert round(chart.data.iloc[40][i18n.t("admits_icu")], 0) == 38

    # test fx call with no params
    with pytest.raises(TypeError):
        build_admits_chart()


def test_census_chart(census_floor_df):
    chart = build_census_chart(alt=alt, census_floor_df=census_floor_df)
    assert isinstance(chart, (alt.Chart, alt.LayerChart))
    assert chart.data.iloc[1][i18n.t("census_hospitalized")] == 3
    assert chart.data.iloc[49][i18n.t("census_ventilated")] == 365

    # test fx call with no params
    with pytest.raises(TypeError):
        build_census_chart()
