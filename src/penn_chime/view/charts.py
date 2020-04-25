from typing import Dict, Optional

from altair import Chart
import pandas as pd
import i18n
import numpy as np

from ..constants import DATE_FORMAT


def build_admits_chart(
    *, alt, admits_floor_df: pd.DataFrame, max_y_axis: Optional[int] = None
) -> Chart:
    """Build admits chart."""
    y_scale = alt.Scale()
    if max_y_axis is not None:
        y_scale.domain = (0, max_y_axis)

    x = dict(shorthand="date:T", title=i18n.t("charts-date"), axis=alt.Axis(format=(DATE_FORMAT)))
    y = dict(shorthand="value:Q", title=i18n.t("charts-daily-admissions"), scale=y_scale)
    color = "key:N"
    tooltip = ["date:T", alt.Tooltip("value:Q", format=".0f", title="Admit"), "key:N"]

    # TODO fix the fold to allow any number of dispositions
    points = (
        alt.Chart()
        .transform_fold(fold=[i18n.t("admits_hospitalized"), i18n.t("admits_icu"), i18n.t("admits_ventilated")])
        .encode(x=alt.X(**x), y=alt.Y(**y), color=color, tooltip=tooltip)
        .mark_line(point=True)
        .encode(
            x=alt.X(**x),
            y=alt.Y(**y),
            color=color,
            tooltip=tooltip,
        )
    )
    bar = (
        alt.Chart()
        .encode(x=alt.X(**x))
        .transform_filter(alt.datum.day == 0)
        .mark_rule(color="black", opacity=0.35, size=2)
    )
    admits_floor_df_renamed = admits_floor_df.rename({
        "admits_hospitalized": i18n.t("admits_hospitalized"),
        "admits_icu": i18n.t("admits_icu"),
        "admits_ventilated": i18n.t("admits_ventilated")
    }, axis=1)
    return (
        alt.layer(points, bar, data=admits_floor_df_renamed)
        .configure_legend(orient="bottom")
        .interactive()
    )


def build_census_chart(
    *, alt, census_floor_df: pd.DataFrame, max_y_axis: Optional[int] = None
) -> Chart:
    """Build census chart."""
    y_scale = alt.Scale()
    if max_y_axis:
        y_scale.domain = (0, max_y_axis)

    x = dict(shorthand="date:T", title=i18n.t("charts-date"), axis=alt.Axis(format=(DATE_FORMAT)))
    y = dict(shorthand="value:Q", title=i18n.t("charts-census"), scale=y_scale)
    color = "key:N"
    tooltip = ["date:T", alt.Tooltip("value:Q", format=".0f", title="Census"), "key:N"]

    # TODO fix the fold to allow any number of dispositions
    points = (
        alt.Chart()
        .transform_fold(fold=[i18n.t("census_hospitalized"), i18n.t("census_icu"), i18n.t("census_ventilated")])
        .encode(x=alt.X(**x), y=alt.Y(**y), color=color, tooltip=tooltip)
        .mark_line(point=True)
        .encode(
            x=alt.X(**x),
            y=alt.Y(**y),
            color=color,
            tooltip=tooltip,
        )
    )
    bar = (
        alt.Chart()
        .encode(x=alt.X(**x))
        .transform_filter(alt.datum.day == 0)
        .mark_rule(color="black", opacity=0.35, size=2)
    )
    census_floor_df_renamed = census_floor_df.rename({
        "census_hospitalized": i18n.t("census_hospitalized"),
        "census_icu": i18n.t("census_icu"),
        "census_ventilated": i18n.t("census_ventilated")
    }, axis=1)
    return (
        alt.layer(points, bar, data=census_floor_df_renamed)
        .configure_legend(orient="bottom")
        .interactive()
    )


def build_sim_sir_w_date_chart(
    *, alt, sim_sir_w_date_floor_df: pd.DataFrame, max_y_axis: Optional[int] = None
) -> Chart:
    """Build sim sir w date chart."""
    y_scale = alt.Scale()
    if max_y_axis is not None:
        y_scale.domain = (0, max_y_axis)

    x = dict(shorthand="date:T", title=i18n.t("charts-date"), axis=alt.Axis(format=(DATE_FORMAT)))
    y = dict(shorthand="value:Q", title=i18n.t("charts-count"), scale=y_scale)
    color = "key:N"
    tooltip = ["key:N", "value:Q"]

    # TODO fix the fold to allow any number of dispositions
    points = (
        alt.Chart()
        .transform_fold(fold=[i18n.t("susceptible"), i18n.t("infected"), i18n.t("recovered")])
        .encode(x=alt.X(**x), y=alt.Y(**y), color=color, tooltip=tooltip)
        .mark_line()
        .encode(
            x=alt.X(**x),
            y=alt.Y(**y),
            color=color,
            tooltip=tooltip,
        )
    )
    bar = (
        alt.Chart()
        .encode(x=alt.X(**x))
        .transform_filter(alt.datum.day == 0)
        .mark_rule(color="black", opacity=0.35, size=2)
    )
    sim_sir_w_date_floor_df_renamed = sim_sir_w_date_floor_df.rename({
        "susceptible": i18n.t("susceptible"),
        "infected": i18n.t("infected"),
        "recovered": i18n.t("recovered")
    }, axis=1)
    return (
        alt.layer(points, bar, data=sim_sir_w_date_floor_df_renamed)
        .configure_legend(orient="bottom")
        .interactive()
    )

def build_table(
    *, df: pd.DataFrame, labels: Dict[str, str], modulo: int = 1
) -> pd.DataFrame:
    table_df = df[np.mod(df.day, modulo) == 0].copy()
    table_df.date = table_df.date.dt.strftime(DATE_FORMAT)
    table_df_renamed = table_df.rename(labels, axis=1)
    return table_df_renamed
