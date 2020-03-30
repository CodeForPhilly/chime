"""Initializes the  dash html
"""
from typing import List, Any

from dash.dependencies import Output
from dash.development.base_component import ComponentMeta
from dash_html_components import H2
from dash_core_components import Markdown, Graph
from dash_bootstrap_components import Table

from penn_chime.utils import add_date_column
from penn_chime.parameters import Parameters

from chime_dash.app.utils.templates import df_to_html_table
from chime_dash.app.services.plotting import plot_dataframe
from chime_dash.app.components.base import Component

LOCALIZATION_FILE = "visualizations.yml"


class Visualizations(Component):
    """
    """

    localization_file = "visualizations.yml"
    callback_outputs = [
        Output(component_id="new-admissions-graph", component_property="figure"),
        Output(component_id="new-admissions-table", component_property="children"),
        Output(component_id="admitted-patients-graph", component_property="figure"),
        Output(component_id="admitted-patients-table", component_property="children"),
    ]

    def get_html(self) -> List[ComponentMeta]:
        """Initializes the header dash html
        """
        return [
            H2(self.content["new-admissions-title"]),
            Markdown(self.content["new-admissions-text"]),
            Graph(id="new-admissions-graph"),
            Table(id="new-admissions-table"),
            H2(self.content["admitted-patients-title"]),
            Markdown(self.content["admitted-patients-text"]),
            Graph(id="admitted-patients-graph"),
            Table(id="admitted-patients-table"),
        ]

    def callback(self, *args, **kwargs) -> List[Any]:
        """Renders the parameter dependent plots and tables
        """
        pars = kwargs.get("pars")
        projection_admits, census_df = self._build_frames(**kwargs)

        # Create admissions figure
        admissions_data = plot_dataframe(
            projection_admits.head(pars.n_days - 10), max_y_axis=pars.max_y_axis,
        )
        # Create admissions table data
        if kwargs["as_date"]:
            projection_admits.index = projection_admits.index.strftime("%b, %d")
        admissions_table_data = (
            df_to_html_table(projection_admits, data_only=True, n_mod=7)
            if kwargs["show_tables"]
            else None
        )

        # Create census figure
        census_data = plot_dataframe(
            census_df.head(pars.n_days - 10), max_y_axis=pars.max_y_axis
        )
        # Create admissions table data
        if kwargs["as_date"]:
            census_df.index = census_df.index.strftime("%b, %d")
        census_table_data = (
            df_to_html_table(census_df, data_only=True, n_mod=7)
            if kwargs["show_tables"]
            else None
        )

        return (admissions_data, admissions_table_data, census_data, census_table_data)

    @staticmethod
    def _build_frames(**kwargs):

        # Prepare admissions data & census data
        projection_admits = kwargs["model"].admits_df.copy()
        census_df = kwargs["model"].census_df.copy()

        # Convert columns
        if kwargs["as_date"]:
            projection_admits = add_date_column(
                projection_admits, drop_day_column=True
            ).set_index("date")
            census_df = add_date_column(census_df, drop_day_column=True).set_index(
                "date"
            )
        else:
            projection_admits = projection_admits.set_index("day")
            census_df = census_df.set_index("day")

        projection_admits = projection_admits.fillna(0).astype(int)
        census_df.iloc[0, :] = 0
        census_df = census_df.dropna().astype(int)

        return projection_admits, census_df
