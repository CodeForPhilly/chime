from typing import Dict, Optional

from altair import Chart, Scale
import pandas as pd
import numpy as np

from ..constants import DATE_FORMAT


def build_admits_chart(
    *, alt, admits_floor_df: pd.DataFrame, max_y_axis: Optional[int] = None, use_log_scale: bool = False
) -> Chart:
    """
    This builds the "New Admissions" chart, projecting daily admissions over time.

    Args:
        alt: Reference to Altair package.
        admits_floor_df: Pandas data frame containing three columns: "admits_hospitalized", "admits_icu", and
        "admits_ventilated".
        max_y_axis: Optional maximum value for the Y axis of the chart.
        use_log_scale: Set to true to use a logarithmic scale on the Y axis. Default is linear scale.

    Returns: The newly created chart.

    """

    adjusted_admits_floor_df = __adjust_data_for_log_scale(admits_floor_df) if use_log_scale else admits_floor_df
    y_scale = __build_y_scale(alt, max_y_axis, use_log_scale)

    x = dict(shorthand="date:T", title="Date", axis=alt.Axis(format=DATE_FORMAT))
    y = dict(shorthand="value:Q", title="Daily admissions", scale=y_scale)
    color = "key:N"
    tooltip = ["date:T", alt.Tooltip("value:Q", format=".0f", title="Admit"), "key:N"]

    # TODO fix the fold to allow any number of dispositions
    points = (
        alt.Chart()
        .transform_fold(fold=["admits_hospitalized", "admits_icu", "admits_ventilated"])
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
    return (
        alt.layer(points, bar, data=adjusted_admits_floor_df)
        .configure_legend(orient="bottom")
        .interactive()
    )


def build_census_chart(
    *, alt, census_floor_df: pd.DataFrame, max_y_axis: Optional[int] = None, use_log_scale: bool = False
) -> Chart:
    """
    This builds the "Admitted Patients" census chart, projecting total number of patients in the hospital over time.

    Args:
        alt: Reference to Altair package.
        census_floor_df: Pandas data frame containing three columns: "census_hospitalized", "census_icu", and
        "census_ventilated".
        max_y_axis: Optional maximum value for the Y axis of the chart.
        use_log_scale: Set to true to use a logarithmic scale on the Y axis. Default is linear scale.

    Returns: The newly created chart.

    """

    adjusted_census_floor_df = __adjust_data_for_log_scale(census_floor_df) if use_log_scale else census_floor_df
    y_scale = __build_y_scale(alt, max_y_axis, use_log_scale)

    x = dict(shorthand="date:T", title="Date", axis=alt.Axis(format=(DATE_FORMAT)))
    y = dict(shorthand="value:Q", title="Census", scale=y_scale)
    color = "key:N"
    tooltip = ["date:T", alt.Tooltip("value:Q", format=".0f", title="Census"), "key:N"]

    # TODO fix the fold to allow any number of dispositions
    points = (
        alt.Chart()
        .transform_fold(fold=["census_hospitalized", "census_icu", "census_ventilated"])
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
    return (
        alt.layer(points, bar, data=adjusted_census_floor_df)
        .configure_legend(orient="bottom")
        .interactive()
    )


def build_sim_sir_w_date_chart(
    *, alt, sim_sir_w_date_floor_df: pd.DataFrame, max_y_axis: Optional[int] = None, use_log_scale: bool = False
) -> Chart:
    """
    This builds the "Susceptible, Infected, and Recovered" chart, projecting the number of those individuals in the
    hospital's region over time.

    Args:
        alt: Reference to the Altair package.
        sim_sir_w_date_floor_df: A Pandas data frame with columns named "susceptible", "infected", and "recovered".
        max_y_axis: Optional maximum value for the Y axis of the chart.
        use_log_scale: Set to true to use a logarithmic scale on the Y axis. Default is linear scale.

    Returns: The newly created chart.

    """

    adjusted_sim_sir_w_date_floor_df = __adjust_data_for_log_scale(sim_sir_w_date_floor_df) if use_log_scale else sim_sir_w_date_floor_df
    y_scale = __build_y_scale(alt, max_y_axis, use_log_scale)

    x = dict(shorthand="date:T", title="Date", axis=alt.Axis(format=(DATE_FORMAT)))
    y = dict(shorthand="value:Q", title="Count", scale=y_scale)
    color = "key:N"
    tooltip = ["key:N", "value:Q"]

    # TODO fix the fold to allow any number of dispositions
    points = (
        alt.Chart()
        .transform_fold(fold=["susceptible", "infected", "recovered"])
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
    return (
        alt.layer(points, bar, data=adjusted_sim_sir_w_date_floor_df)
        .configure_legend(orient="bottom")
        .interactive()
    )


def build_table(
    *, df: pd.DataFrame, labels: Dict[str, str], modulo: int = 1
) -> pd.DataFrame:
    table_df = df[np.mod(df.day, modulo) == 0].copy()
    table_df.date = table_df.date.dt.strftime(DATE_FORMAT)
    table_df.rename(labels)
    return table_df


def __adjust_data_for_log_scale(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    This will clean and adjust some of the data so that Altair can plot it using a logarithmic scale. Altair does not
    allow zero values on the Y axis when plotting with a logarithmic scale, as log(0) is undefined.

    Args:
        dataframe: The data to plot on the chart.

    Returns: A new data frame with the appropriate adjustments for plotting on a log scale.

    """
    return dataframe.replace(0, float('nan'))  # We use NaN so that the values will not appear at all on the chart.


def __build_y_scale(alt, max_y_axis: Optional[int] = None, use_log_scale: bool = False) -> Scale:
    """
    Creates the Y axis of the chart, taking into account some of the configuration parameters set by the user.

    Args:
        alt: Reference to Altair package.
        max_y_axis: The maximum value of the Y axis. This is optional.
        use_log_scale: Whether to use a logarithmic scale instead of a linear scale.

    Returns: A newly created Scale instance.

    """
    scale_type = 'log' if use_log_scale else 'linear'
    y_scale = alt.Scale(type=scale_type)
    if max_y_axis is not None:
        y_scale.domain = (0, max_y_axis)

    return y_scale
