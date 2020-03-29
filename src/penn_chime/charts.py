
from datetime import datetime
from math import ceil
from typing import Dict, Optional

from altair import Chart  # type: ignore
import pandas as pd  # type: ignore
import numpy as np

from .parameters import Parameters
from .presentation import DATE_FORMAT


def build_admits_chart(
    *,
    alt,
    admits_df: pd.DataFrame,
    max_y_axis: Optional[int] = None,
) -> Chart:
    """docstring"""
    y_scale = alt.Scale()

    if max_y_axis is not None:
        y_scale.domain = (0, max_y_axis)

    ceil_df = admits_df.copy()
    ceil_df.hospitalized = np.ceil(ceil_df.hospitalized)
    ceil_df.icu = np.ceil(ceil_df.icu)
    ceil_df.ventilated = np.ceil(ceil_df.ventilated)

    # TODO fix the fold to allow any number of dispositions
    return (
        alt.Chart(ceil_df)
        .transform_fold(fold=["hospitalized", "icu", "ventilated"])
        .mark_line(point=True)
        .encode(
            x=alt.X("date:T", title="Date", axis=alt.Axis(format=(DATE_FORMAT))),
            y=alt.Y("value:Q", title="Daily admissions", scale=y_scale),
            color="key:N",
            tooltip=[
                "date:T",
                alt.Tooltip("value:Q", format=".0f", title="Admit"),
                "key:N",
            ])
    )


def build_census_chart(
    *,
    alt,
    census_df: pd.DataFrame,
    max_y_axis: Optional[int] = None,
) -> Chart:
    """docstring"""
    y_scale = alt.Scale()

    if max_y_axis:
        y_scale.domain = (0, max_y_axis)

    # TODO fix the fold to allow any number of dispositions
    base = (
        alt.Chart(census_df)
        .transform_fold(fold=["hospitalized", "icu", "ventilated"])
        .mark_line(point=True, interpolate='basis')
        .encode(
            x=alt.X("date:T", title="Date", axis=alt.Axis(format=(DATE_FORMAT))),
            y=alt.Y("value:Q", title="Census", scale=y_scale),
            color="key:N",
            tooltip=[
                "date:T",
                alt.Tooltip("value:Q", format=".0f", title="Census"),
                "key:N",
            ])
    )
    return base
    bar = (
        alt.Chart()
        .mark_rule(
            color="black",
            opacity=0.35,
            size=3)
        .encode(x=alt.X("day:Q", title="Current Date"))
        .transform_filter(alt.datum.day == 0)
    )
    return alt.layer(base, bar, data=census_df)


def build_sim_sir_w_date_chart(
    *,
    alt,
    sim_sir_w_date_df: pd.DataFrame,
    max_y_axis: Optional[int] = None,
) -> Chart:
    y_scale = alt.Scale()

    if max_y_axis is not None:
        y_scale.domain = (0, max_y_axis)

    # TODO fix the fold to allow any number of dispositions
    base = (
        alt.Chart(sim_sir_w_date_df)
        .transform_fold(fold=["susceptible", "infected", "recovered"])
        .mark_line()
        .encode(
            x=alt.X("date:T", title="Date", axis=alt.Axis(format=(DATE_FORMAT))),
            y=alt.Y("value:Q", title="Count", scale=y_scale),
            tooltip=["key:N", "value:Q"],
            color="key:N",
        )
    )
    return base
    bar = (
        alt.Chart()
        .mark_rule(
            color="black",
            opacity=0.35,
            size=3)
        .encode(x=alt.X("day:Q", title="Current Date"))
        .transform_filter(alt.datum.day == 0)
    )
    return alt.layer(base, bar, data=sim_sir_w_date_df)



def build_descriptions(
    *,
    chart: Chart,
    labels: Dict[str, str],
    suffix: str = ""
) -> str:
    """

    :param chart: The alt chart to be used in finding max points
    :param suffix: The assumption is that the charts have similar column names.
                   The census chart adds " Census" to the column names.
                   Make sure to include a space or underscore as appropriate
    :return: Returns a multi-line string description of the results
    """
    messages = []

    cols = ["hospitalized", "icu", "ventilated"]
    asterisk = False
    day = "date" if "date" in chart.data.columns else "day"

    for col in cols:
        if chart.data[col].idxmax() + 1 == len(chart.data):
            asterisk = True

        # todo: bring this to an optional arg / i18n
        on = datetime.strftime(chart.data[day][chart.data[col].idxmax()], "%b %d")

        messages.append(
            "{}{} peaks at {:,} on {}{}".format(
                labels[col],
                suffix,
                ceil(chart.data[col].max()),
                on,
                "*" if asterisk else "",
            )
        )

    if asterisk:
        messages.append("_* The max is at the upper bound of the data, and therefore may not be the actual max_")
    return "\n\n".join(messages)


def build_table(
    *,
    df: pd.DataFrame,
    labels: Dict[str, str],
    modulo: int = 1,
) -> pd.DataFrame:
    table_df = df[np.mod(df.day, modulo) == 0].copy()
    table_df.rename(labels)
    return table_df
