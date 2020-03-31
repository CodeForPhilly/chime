"""components/visualizations

Initializes the visual components of the interactive model

localization file can be found in app/templates/en
"""
from typing import List, Any

import urllib.parse
from datetime import date, datetime

from dash.dependencies import Output
from dash.development.base_component import ComponentMeta
from dash_html_components import H2, A, Div
from dash_core_components import Markdown, Graph
from dash_bootstrap_components import Table

from penn_chime.charts import build_table
from penn_chime.constants import DATE_FORMAT

from chime_dash.app.utils.templates import df_to_html_table
from chime_dash.app.services.plotting import plot_dataframe
from chime_dash.app.components.base import Component


class Visualizations(Component):
    """
    """

    localization_file = "visualizations.yml"
    callback_outputs = [
        Output(component_id="new-admissions-graph", component_property="figure"),
        Output(component_id="new-admissions-table", component_property="children"),
        Output(component_id="admitted-patients-graph", component_property="figure"),
        Output(component_id="admitted-patients-table", component_property="children"),
        Output(component_id="download-admissions", component_property="href"),
        Output(component_id="download-census", component_property="href"),
    ]

    def get_html(self) -> List[ComponentMeta]:
        """Initializes the header dash html
        """
        today = date.today().strftime(self.content["date-format"])
        return [
            H2(self.content["new-admissions-title"]),
            Markdown(self.content["new-admissions-text"]),
            Graph(id="new-admissions-graph"),
            A(
                self.content["download-text"],
                id="download-admissions",
                download="admissions_{}.csv".format(today),
                href="",
                target="_blank",
                className="btn btn-sm btn-info my-2",
            ),
            Div(
                className="row justify-content-center",
                children=Div(
                    className="col-auto",
                    children=[
                        Table(id="new-admissions-table", className="table-responsive"),
                    ],
                ),
            ),
            H2(self.content["admitted-patients-title"]),
            Markdown(self.content["admitted-patients-text"]),
            Graph(id="admitted-patients-graph"),
            A(
                self.content["download-text"],
                id="download-census",
                download="census_{}.csv".format(today),
                href="",
                target="_blank",
                className="btn btn-sm btn-info my-4",
            ),
            Div(
                className="row justify-content-center",
                children=Div(
                    className="col-auto",
                    children=[
                        Table(
                            id="admitted-patients-table", className="table-responsive"
                        ),
                    ],
                ),
            ),
        ]

    def callback(self, *args, **kwargs) -> List[Any]:
        """Renders the parameter dependent plots and tables
        """
        pars = kwargs.get("pars")
        admits_df = kwargs["model"].admits_df
        census_df = kwargs["model"].census_df

        census_modulo = 7
        admits_modulo = 7

        # Create admissions figure
        admits_plot_data = plot_dataframe(
            admits_df.dropna().set_index("date").drop(columns=["day"]),
            max_y_axis=pars.max_y_axis,
        )

        # Create admissions table data
        admits_table = (
            df_to_html_table(
                build_table(df=admits_df, labels=pars.labels, modulo=admits_modulo),
                format={
                    float: int,
                    (date, datetime): lambda d: d.strftime(DATE_FORMAT),
                },
            )
            if kwargs["show_tables"]
            else None
        )

        # Create census figure
        census_plot_data = plot_dataframe(
            census_df.dropna().set_index("date").drop(columns=["day"]),
            max_y_axis=pars.max_y_axis,
        )
        # Create admissions table data
        census_table = (
            df_to_html_table(
                build_table(df=census_df, labels=pars.labels, modulo=census_modulo),
                format={
                    float: int,
                    (date, datetime): lambda d: d.strftime(DATE_FORMAT),
                },
            )
            if kwargs["show_tables"]
            else None
        )

        # Create admissions CSV
        admissions_csv = admits_df.to_csv(index=True, encoding="utf-8")
        admissions_csv = "data:text/csv;charset=utf-8," + urllib.parse.quote(
            admissions_csv
        )

        # Create census CSV
        census_csv = census_df.to_csv(index=True, encoding="utf-8")
        census_csv = "data:text/csv;charset=utf-8," + urllib.parse.quote(census_csv)

        return [
            admits_plot_data,
            admits_table,
            census_plot_data,
            census_table,
            admissions_csv,
            census_csv,
        ]

    @staticmethod
    def _build_frames(**kwargs):

        # Prepare admissions data & census data
        projection_admits = kwargs["model"].admits_df.copy()
        census_df = kwargs["model"].census_df.copy()

        projection_admits = projection_admits.fillna(0).astype(int)
        census_df.iloc[0, :] = 0
        census_df = census_df.dropna().astype(int)

        return projection_admits, census_df
