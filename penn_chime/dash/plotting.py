"""Functions which set up plotly-dash plots
"""


def get_figure_data(y_max):
    """
    """
    return {
        "data": [
            {"x": [1, 2, 3, 4], "y": [4, 1, 2, y_max], "type": "bar", "name": "SF"},
            {
                "x": [1, 2, 3, 4],
                "y": [2, 4, 5, y_max],
                "type": "bar",
                "name": u"Montréal",
            },
        ],
        "layout": {"title": "Dash Data Visualization"},
    }
