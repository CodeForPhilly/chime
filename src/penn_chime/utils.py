"""Utils."""

from base64 import b64encode

import pandas as pd


def dataframe_to_base64(df: pd.DataFrame) -> str:
    """Converts a dataframe to a base64-encoded CSV representation of that data.

    This is useful for building datauris for use to download the data in the browser.

    Arguments:
        df: The dataframe to convert
    """
    csv = df.to_csv(index=False)
    b64 = b64encode(csv.encode()).decode()
    return b64
