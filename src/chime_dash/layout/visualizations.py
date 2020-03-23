"""Initializes the  dash html
"""
from typing import List, Any

from dash.dependencies import Output
from dash.development.base_component import ComponentMeta
from dash_html_components import H2, Div
from dash_core_components import Markdown, Graph

from penn_chime.utils import build_census_df, build_admissions_df, add_date_column
from penn_chime.models import Parameters


from chime_dash.utils import read_localization_yaml
from chime_dash.plotting import plot_dataframe

LOCALIZATION_FILE = "visualizations.yml"


def setup(language: str) -> List[ComponentMeta]:
    """Initializes the header dash html
    """
    content = read_localization_yaml(LOCALIZATION_FILE, language)

    return [
        H2(content["new-admissions-title"]),
        Markdown(content["new-admissions-text"]),
        Graph(id="new-admissions-graph"),
        H2(content["admitted-patients-title"]),
        Markdown(content["admitted-patients-text"]),
        Graph(id="admitted-patients-graph"),
    ]


CALLBACK_OUTPUTS = [
    Output(component_id="new-admissions-graph", component_property="figure"),
    Output(component_id="admitted-patients-graph", component_property="figure"),
]


def render(language: str, pars: Parameters, as_date: bool = False) -> List[Any]:
    """Renders the parameter dependent plots and tables
    """
    content = read_localization_yaml(LOCALIZATION_FILE, language)

    # Prepare admissions data
    projection_admits = build_admissions_df(pars.n_days, *pars.dispositions)
    if as_date:
        projection_admits = add_date_column(
            projection_admits, drop_day_column=True
        ).set_index("date")
    else:
        projection_admits = projection_admits.set_index("day")

    localized_columns = {key: content[key] for key in projection_admits.columns}
    projection_admits = projection_admits.dropna().rename(columns=localized_columns)

    # Plot admissions figure
    admissions_data = plot_dataframe(
        projection_admits.head(pars.n_days - 10), max_y_axis=pars.max_y_axis,
    )

    return (admissions_data, admissions_data)
