
from math import ceil
import datetime

from altair import Chart  # type: ignore
import pandas as pd  # type: ignore
import numpy as np

from .parameters import Parameters
from .presentation import DATE_FORMAT


def build_admits_chart(
    alt, admits_df: pd.DataFrame, parameters: Parameters
) -> Chart:
    """docstring"""
    max_y_axis = parameters.max_y_axis
    as_date = parameters.as_date

    y_scale = alt.Scale()

    if max_y_axis is not None:
        y_scale.domain = (0, max_y_axis)

    tooltip_dict = {False: "day", True: "date:T"}
    if as_date:
        today = np.datetime64(parameters.today)
        admits_df['date'] = admits_df.day.astype('timedelta64[D]') + today
        x_kwargs = {"shorthand": "date:T", "title": "Date", "axis": alt.Axis(format=(DATE_FORMAT))}
    else:
        x_kwargs = {"shorthand": "day", "title": "Days from today"}

    # TODO fix the fold to allow any number of dispositions

    ceil_df = admits_df.copy()

    ceil_df.hospitalized = np.ceil(ceil_df.hospitalized)
    ceil_df.icu = np.ceil(ceil_df.icu)
    ceil_df.ventilated = np.ceil(ceil_df.ventilated)

    return (
        alt.Chart(ceil_df)
        .transform_fold(fold=["hospitalized", "icu", "ventilated"])
        .mark_line(point=True)
        .encode(
            x=alt.X(**x_kwargs),
            y=alt.Y("value:Q", title="Daily admissions", scale=y_scale),
            color="key:N",
            tooltip=[
                tooltip_dict[as_date],
                alt.Tooltip("value:Q", format=".0f", title="Admissions"),
                "key:N",
            ],
        )
        .interactive()
    )


def build_census_chart(
    alt, census_df: pd.DataFrame, parameters: Parameters
) -> Chart:
    """docstring"""

    plot_projection_days = parameters.n_days - 10
    max_y_axis = parameters.max_y_axis
    as_date = parameters.as_date
    if as_date:
        today = np.datetime64(parameters.today)
        census_df['date'] = census_df.day.astype('timedelta64[D]') + today
        x_kwargs = {"shorthand": "date:T", "title": "Date", "axis": alt.Axis(format=(DATE_FORMAT))}
        idx = "date:T"
    else:
        x_kwargs = {"shorthand": "day", "title": "Days from today"}
        idx = "day"

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


def additional_projections_chart(
    alt, model, parameters
) -> Chart:

    # TODO use subselect of df_raw instead of creating a new df
    raw_df = model.raw_df
    dat = pd.DataFrame({
        "day": raw_df.day,
        "infected": raw_df.infected,
        "recovered": raw_df.recovered
    })

    as_date = parameters.as_date
    max_y_axis = parameters.max_y_axis

    if as_date:
        dat = add_date_column(dat, parameters.date_first_hospitalized)
        x_kwargs = {"shorthand": "date:T", "title": "Date", "axis": alt.Axis(format=(DATE_FORMAT))}
    else:
        x_kwargs = {"shorthand": "day", "title": "Days from today"}

    y_scale = alt.Scale()

    if max_y_axis is not None:
        y_scale.domain = (0, max_y_axis)

    return (
        alt.Chart(dat)
        .transform_fold(fold=["infected", "recovered"])
        .mark_line()
        .encode(
            x=alt.X(**x_kwargs),
            y=alt.Y("value:Q", title="Case Volume", scale=y_scale),
            tooltip=["key:N", "value:Q"],
            color="key:N",
        )
        .interactive()
    )


def chart_descriptions(chart: Chart, labels, suffix: str = ""):
    """

    :param chart: Chart: The alt chart to be used in finding max points
    :param suffix: str: The assumption is that the charts have similar column names.
                   The census chart adds " Census" to the column names.
                   Make sure to include a space or underscore as appropriate
    :return: str: Returns a multi-line string description of the results
    """
    messages = []

    cols = ["hospitalized", "icu", "ventilated"]
    asterisk = False
    day = "date" if "date" in chart.data.columns else "day"

    for col in cols:
        if chart.data[col].idxmax() + 1 == len(chart.data):
            asterisk = True

        on = chart.data[day][chart.data[col].idxmax()]
        if day == "date":
            on = datetime.datetime.strftime(on, "%b %d")  # todo: bring this to an optional arg / i18n
        else:
            on += 1  # 0 index issue

        messages.append(
            "{}{} peaks at {:,} on day {}{}".format(
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
