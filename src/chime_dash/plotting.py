"""Functions which set up plotly-dash plots
"""
from typing import Dict, Any

from penn_chime.utils import add_date_column

import pandas as pd


def plot_dataframe(dataframe: pd.DataFrame, max_y_axis: int = None,) -> Dict[str, Any]:
    """
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
