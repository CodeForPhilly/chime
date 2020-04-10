"""services/plotting

Logic for data manipulation needed when new call backs are executed
"""
from typing import Dict, Any

from pandas import DataFrame


def plot_dataframe(
    dataframe: DataFrame,
    max_y_axis: int = None,
) -> Dict[str, Any]:
    """Returns dictionary used for plotly graphs

    Arguments:
        dataframe: The dataframe to plot. Plots all columns as y, index is x.
        max_y_axis: Maximal value on y-axis.
    """

    if max_y_axis is None:
        yaxis = {}
    else:
        yaxis = {"range": (0, max_y_axis), "autorange": False}

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
        "layout": {"yaxis": yaxis},
    }
