"""Utils."""

from collections import namedtuple
from datetime import datetime, timedelta
from typing import Optional

import numpy as np  # type: ignore
import pandas as pd  # type: ignore

# from .parameters import Parameters


# (0.02, 7) is 2%, 7 days
# be sure to multiply by 100 when using as a default to the pct widgets!
RateLos = namedtuple('RateLos', ('rate', 'length_of_stay'))


def build_admissions_df(p) -> pd.DataFrame:
    """Build admissions dataframe from Parameters."""
    days = np.array(range(0, p.n_days + 1))
    data_dict = dict(zip(["day", "Hospitalized", "ICU", "Ventilated"],
                         [days] + [disposition for disposition in p.dispositions]
    ))
    projection = pd.DataFrame.from_dict(data_dict)
    # New cases
    projection_admits = projection.iloc[:-1, :] - projection.shift(1)
    projection_admits[projection_admits < 0] = 0
    projection_admits["day"] = range(projection_admits.shape[0])
    return projection_admits


def build_census_df(
        projection_admits: pd.DataFrame,
        parameters
) -> pd.DataFrame:
    """ALOS for each category of COVID-19 case (total guesses)"""
    n_days = np.shape(projection_admits)[0]
    hosp_los, icu_los, vent_los = parameters.lengths_of_stay
    los_dict = {
        "Hospitalized": hosp_los,
        "ICU": icu_los,
        "Ventilated": vent_los,
    }

    census_dict = dict()
    for k, los in los_dict.items():
        census = (
            projection_admits.cumsum().iloc[:-los, :]
            - projection_admits.cumsum().shift(los).fillna(0)
        ).apply(np.ceil)
        census_dict[k] = census[k]

    census_df = pd.DataFrame(census_dict)
    census_df["day"] = census_df.index
    census_df = census_df[["day", "Hospitalized", "ICU", "Ventilated"]]
    census_df = census_df.head(n_days)
    census_df = census_df.rename(
        columns={disposition: f"{disposition} Census"
                 for disposition
                 in ("Hospitalized", "ICU", "Ventilated")}
    )
    return census_df


def add_date_column(
    df: pd.DataFrame,
    drop_day_column: bool = False,
    date_format: Optional[str] = None,
) -> pd.DataFrame:
    """Copies input data frame and converts "day" column to "date" column

    Assumes that day=0 is today and allocates dates for each integer day.
    Day range can must not be continous.
    Columns will be organized as original frame with difference that date
    columns come first.

    Arguments:
        df: The data frame to convert.
        drop_day_column: If true, the returned data frame will not have a day column.
        date_format: If given, converts date_time objetcts to string format specified.

    Raises:
        KeyError: if "day" column not in df
        ValueError: if "day" column is not of type int
    """
    if not "day" in df:
        raise KeyError("Input data frame for converting dates has no 'day column'.")
    if not pd.api.types.is_integer_dtype(df.day):
        raise KeyError("Column 'day' for dates converting data frame is not integer.")

    df = df.copy()
    # Prepare columns for sorting
    non_date_columns = [col for col in df.columns if not col == "day"]

    # Allocate (day) continous range for dates
    n_days = int(df.day.max())
    start = datetime.now()
    end = start + timedelta(days=n_days + 1)
    # And pick dates present in frame
    dates = pd.date_range(start=start, end=end, freq="D")[df.day.tolist()]

    if date_format is not None:
        dates = dates.strftime(date_format)

    df["date"] = dates

    if drop_day_column:
        df.pop("day")
        date_columns = ["date"]
    else:
        date_columns = ["day", "date"]

    # sort columns
    df = df[date_columns + non_date_columns]

    return df
