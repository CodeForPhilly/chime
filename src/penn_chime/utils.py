"""Utils."""

from base64 import b64encode

import pandas as pd


def dataframe_to_base64(df: pd.DataFrame) -> str:
    """Converts a dataframe into csv base64-encoded data.

    This is useful for building datauris for use to download the data in the browser.

    Arguments:
        df: The dataframe to convert
    """
    csv = df.to_csv(index=False)
    b64 = b64encode(csv.encode()).decode()
    return b64


def excel_to_base64(filename: str) -> str:
    """Converts an excel document into base64-encoded data."""
    with open(filename, 'rb') as fin:
        return b64encode(fin.read()).decode()
