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
from dash_bootstrap_components import Table, Container

from penn_chime.charts import build_table
from penn_chime.constants import DATE_FORMAT

from chime_dash.app.utils.templates import df_to_html_table
from chime_dash.app.services.plotting import plot_dataframe
from chime_dash.app.components.base import Component


class Visualizations(Component):
    """Creates graphs, tables and download links for data

    Categories
    * new addmissions
    * admitted patients
    * Simulated SIR data
    """

    localization_file = "visualizations.yml"
    callback_outputs = [
        Output(component_id="new-admissions-graph", component_property="figure"),
        Output(component_id="new-admissions-table", component_property="children"),
        Output(component_id="new-admissions-download", component_property="href"),
        Output(component_id="admitted-patients-graph", component_property="figure"),
        Output(component_id="admitted-patients-table", component_property="children"),
        Output(component_id="admitted-patients-download", component_property="href"),
        Output(component_id="SIR-graph", component_property="figure"),
        Output(component_id="SIR-table", component_property="children"),
        Output(component_id="SIR-download", component_property="href"),
    ]

    def get_html(self) -> List[ComponentMeta]:
        """Initializes the header dash html
        """
        today = date.today().strftime(self.content["date-format"])
        return [
            Container(className="mt-5",
                children=[
                    H2(self.content["new-admissions-title"]),
                    Markdown(self.content["new-admissions-text"]),
                ]
            ),
            Container(fluid=True, children=Graph(id="new-admissions-graph")),
            Container([
                A(
                    self.content["download-text"],
                    id="new-admissions-download",
                    download="admissions_{}.csv".format(today),
                    href="",
                    target="_blank",
                    className="btn btn-sm btn-info",
                ),
                Div(className="row justify-content-center",
                    children=Div(className="col-auto",
                        children=Table(id="new-admissions-table",
                            className="table-responsive mx-auto"
                        ),
                    ),
                ),
            ]),
            Container(className="mt-5",
                children=[
                    H2(self.content["admitted-patients-title"]),
                    Markdown(self.content["admitted-patients-text"]),
                ],
            ),
            Container(fluid=True, children=Graph(id="admitted-patients-graph")),
            Container([
                A(
                    self.content["download-text"],
                    id="admitted-patients-download",
                    download="census_{}.csv".format(today),
                    href="",
                    target="_blank",
                    className="btn btn-sm btn-info",
                ),
                Div(className="row justify-content-center",
                    children=Div(className="col-auto",
                        children=Table(id="admitted-patients-table",
                            className="table-responsive"
                        ),
                    ),
                ),
            ]),
            Container(className="mt-5",
                children=[
                    H2(self.content["SIR-title"]),
                    Markdown(self.content["SIR-text"]),
                ],
            ),
            Container(fluid=True, children=Graph(id="SIR-graph")),
            Container([
                A(
                    self.content["download-text"],
                    id="SIR-download",
                    download="SIR_{}.csv".format(today),
                    href="",
                    target="_blank",
                    className="btn btn-sm btn-info my-4",
                ),
                Div(className="row justify-content-center",
                    children=Div(className="col-auto",
                        children=Table(id="SIR-table",
                            className="table-responsive"
                        ),
                    ),
                ),
            ])
        ]

    @staticmethod
    def _prepare_visualizations(dataframe, **kwargs) -> List[Any]:
        """Creates plot, table and download link for data frame.
        """
        plot_data = plot_dataframe(
            dataframe.dropna().set_index("date").drop(columns=["day"]),
            max_y_axis=kwargs.get("max_y_axis", None),
        )

        table = (
            df_to_html_table(
                build_table(
                    df=dataframe,
                    labels=kwargs.get("labels", dataframe.columns),
                    modulo=kwargs.get("table_mod", 7),
                ),
                data_only=True,
                format={
                    float: int,
                    (date, datetime): lambda d: d.strftime(DATE_FORMAT),
                },
            )
            if kwargs.get("show_tables", None)
            else None
        )

        csv = dataframe.to_csv(index=True, encoding="utf-8")
        csv = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv)

        return [plot_data, table, csv]

    def callback(self, *args, **kwargs) -> List[Any]:
        """Renders the parameter dependent plots and tables
        """
        pars = kwargs.get("pars")
        admits_df = kwargs["model"].admits_df
        census_df = kwargs["model"].census_df
        simsir_df = kwargs["model"].sim_sir_w_date_df

        viz_kwargs = dict(
            labels=pars.labels,
            table_mod=7,
            max_y_axis=pars.max_y_axis,
            show_tables=kwargs["show_tables"],
        )

        return (
            self._prepare_visualizations(admits_df, **viz_kwargs)
            + self._prepare_visualizations(census_df, **viz_kwargs)
            + self._prepare_visualizations(simsir_df, **viz_kwargs)
        )
