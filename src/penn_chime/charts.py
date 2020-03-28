
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
    idx = "date:T"
    x_kwargs = {"shorthand": "date:T", "title": "Date", "axis": alt.Axis(format=(DATE_FORMAT))}
    y_scale = alt.Scale()

    if max_y_axis is not None:
        y_scale.domain = (0, max_y_axis)

    # TODO fix the fold to allow any number of dispositions

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
            x=alt.X(**x_kwargs),
            y=alt.Y("value:Q", title="Daily admissions", scale=y_scale),
            color="key:N",
            tooltip=[
                idx,
                alt.Tooltip("value:Q", format=".0f", title="Admissions"),
                "key:N",
            ],
        )
        .interactive()
    )


def build_census_chart(
    *,
    alt,
    census_df: pd.DataFrame,
    max_y_axis: Optional[int] = None,
) -> Chart:
    """docstring"""
    idx = "date:T"
    x_kwargs = {"shorthand": "date:T", "title": "Date", "axis": alt.Axis(format=(DATE_FORMAT))}
    y_scale = alt.Scale()

    if max_y_axis:
        y_scale.domain = (0, max_y_axis)

    # TODO fix the fold to allow any number of dispositions
    return (
        #alt.Chart(census_df.head(plot_projection_days))
        alt.Chart(census_df)
        .transform_fold(fold=["hospitalized", "icu", "ventilated"])
        .mark_line(point=True)
        .encode(
            x=alt.X(**x_kwargs),
            y=alt.Y("value:Q", title="Census", scale=y_scale),
            color="key:N",
            tooltip=[
                idx,
                alt.Tooltip("value:Q", format=".0f", title="Census"),
                "key:N",
            ],
        )
        .interactive()
    )



def build_sim_sir_w_date_chart(
    *,
    alt,
    sim_sir_w_date_df: pd.DataFrame,
    max_y_axis: Optional[int] = None,
) -> Chart:
    idx = "date:T"
    x_kwargs = {"shorthand": "date:T", "title": "Date", "axis": alt.Axis(format=(DATE_FORMAT))}
    y_scale = alt.Scale()

    if max_y_axis is not None:
        y_scale.domain = (0, max_y_axis)

    return (
        alt.Chart(sim_sir_w_date_df)
        .transform_fold(fold=["susceptible", "infected", "recovered"])
        .mark_line()
        .encode(
            x=alt.X(**x_kwargs),
            y=alt.Y("value:Q", title="Count", scale=y_scale),
            tooltip=["key:N", "value:Q"],
            color="key:N",
        )
        .interactive()
    )


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
