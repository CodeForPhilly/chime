"""Functions which set up plotly-dash plots
"""
from typing import Dict, Any

from penn_chime.utils import add_date_column

import pandas as pd


def new_admissions_chart(
    projection_admits: pd.DataFrame,
    plot_projection_days: int,
    as_date: bool = False,
    max_y_axis: int = None,
) -> Dict[str, Any]:
    """
    """
    projection_admits = projection_admits.rename(
        columns={"hosp": "Hospitalized", "icu": "ICU", "vent": "Ventilated"}
    )
    projection_admits = add_date_column(projection_admits).dropna()
    return {
        "data": [
            {
                "x": projection_admits["date"] if as_date else projection_admits["day"],
                "y": projection_admits[col].astype(int),
                "name": col,
                "mode": "lines+markers",
            }
            for col in ["Hospitalized", "ICU", "Ventilated"]
        ]
    }
