"""Utils."""

from collections import namedtuple
from datetime import datetime, timedelta
from typing import Optional
from base64 import b64encode

import numpy as np  # type: ignore
import pandas as pd  # type: ignore

# from .parameters import Parameters


# (0.02, 7) is 2%, 7 days
# be sure to multiply by 100 when using as a default to the pct widgets!
RateLos = namedtuple("RateLos", ("rate", "length_of_stay"))


def add_date_column(
    df: pd.DataFrame, drop_day_column: bool = False, date_format: Optional[str] = None,
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

def dataframe_to_base64(df: pd.DataFrame) -> str:
    """Converts a dataframe to a base64-encoded CSV representation of that data.

    This is useful for building datauris for use to download the data in the browser.

    Arguments:
        df: The dataframe to convert
    """
    csv = df.to_csv(index=False)
    b64 = b64encode(csv.encode()).decode()
    return b64
