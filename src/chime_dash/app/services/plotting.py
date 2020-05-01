"""services/plotting

Logic for data manipulation needed when new call backs are executed
"""
from typing import Dict, Any

from pandas import DataFrame


def plot_dataframe(dataframe: DataFrame) -> Dict[str, Any]:
    """Returns dictionary used for plotly graphs

    Arguments:
        dataframe: The dataframe to plot. Plots all columns as y, index is x.
    """

    return {
        "data": [
            {
                "x": dataframe.index,
                "y": dataframe[col].astype(int),
                "name": col,
                "mode": "lines+markers",
            }
            for col in dataframe.columns
        ],
        "layout": {
            "xaxis": {},
            "yaxis": {},
            "legend": {"orientation": "h"},
        },
    }
