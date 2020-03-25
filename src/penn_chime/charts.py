
from math import ceil
import datetime

from altair import Chart  # type: ignore
import pandas as pd  # type: ignore

from .parameters import Parameters
from .utils import add_date_column
from .presentation import DATE_FORMAT


def new_admissions_chart(
    alt, projection_admits: pd.DataFrame, parameters: Parameters
) -> Chart:
    """docstring"""
    plot_projection_days = parameters.n_days - 10
    max_y_axis = parameters.max_y_axis
    as_date = parameters.as_date

    y_scale = alt.Scale()

    if max_y_axis is not None:
        y_scale.domain = (0, max_y_axis)

    tooltip_dict = {False: "day", True: "date:T"}
    if as_date:
        projection_admits = add_date_column(projection_admits)
        x_kwargs = {"shorthand": "date:T", "title": "Date", "axis": alt.Axis(format=(DATE_FORMAT))}
    else:
        x_kwargs = {"shorthand": "day", "title": "Days from today"}

    # TODO fix the fold to allow any number of dispositions
    return (
        alt.Chart(projection_admits.head(plot_projection_days))
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


def admitted_patients_chart(
    alt, census: pd.DataFrame, parameters: Parameters
) -> Chart:
    """docstring"""

    plot_projection_days = parameters.n_days - 10
    max_y_axis = parameters.max_y_axis
    as_date = parameters.as_date
    if as_date:
        census = add_date_column(census)
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
        alt.Chart(census.head(plot_projection_days))
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
        "infected": raw_df.infected,
        "recovered": raw_df.recovered
    })
    dat["day"] = dat.index

    as_date = parameters.as_date
    max_y_axis = parameters.max_y_axis

    if as_date:
        dat = add_date_column(dat)
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
