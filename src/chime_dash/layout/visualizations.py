"""Initializes the  dash html
"""
from typing import List, Any

from dash.dependencies import Output
from dash.development.base_component import ComponentMeta
from dash_html_components import H2
from dash_core_components import Markdown, Graph
from dash_bootstrap_components import Table

from penn_chime.utils import build_census_df, build_admissions_df, add_date_column
from penn_chime.models import Parameters


from chime_dash.utils import read_localization_yaml, df_to_html_table
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
        Table(id="new-admissions-table"),
        H2(content["admitted-patients-title"]),
        Markdown(content["admitted-patients-text"]),
        Graph(id="admitted-patients-graph"),
    ]


CALLBACK_OUTPUTS = [
    Output(component_id="new-admissions-graph", component_property="figure"),
    Output(component_id="new-admissions-table", component_property="children"),
    Output(component_id="admitted-patients-graph", component_property="figure"),
]


def render(language: str, pars: Parameters, as_date: bool = False) -> List[Any]:
    """Renders the parameter dependent plots and tables
    """
    content = read_localization_yaml(LOCALIZATION_FILE, language)

    # Prepare admissions data & census data
    projection_admits = build_admissions_df(pars.n_days, *pars.dispositions)
    census_df = build_census_df(projection_admits, *pars.lengths_of_stay)
    if as_date:
        projection_admits = add_date_column(
            projection_admits, drop_day_column=True
        ).set_index("date")
        census_df = add_date_column(census_df, drop_day_column=True).set_index("date")
    else:
        projection_admits = projection_admits.set_index("day")
        census_df = census_df.set_index("day")

    projection_admits = (
        projection_admits.dropna()
        .rename(columns={key: content[key] for key in projection_admits.columns})
        .astype(int)
    )
    census_df = (
        census_df.dropna()
        .rename(columns={key: content[key] for key in census_df.columns})
        .astype(int)
    )

    # Create admissions figure
    admissions_data = plot_dataframe(
        projection_admits.head(pars.n_days - 10), max_y_axis=pars.max_y_axis,
    )
    if as_date:
        projection_admits.index = projection_admits.index.strftime("%b, %d")
    table_data = df_to_html_table(projection_admits, data_only=True, n_mod=7)

    # Create census figure
    census_data = plot_dataframe(
        census_df.head(pars.n_days - 10), max_y_axis=pars.max_y_axis,
    )

    return (admissions_data, table_data, census_data)
