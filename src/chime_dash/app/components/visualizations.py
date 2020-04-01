"""components/visualizations

Initializes the visual components of the interactive model

localization file can be found in app/templates/en
"""
from typing import Any, List
from datetime import date

from dash.development.base_component import ComponentMeta
from dash_html_components import H2, Div, A
from dash_core_components import Markdown, Graph
from dash_bootstrap_components import Table

from chime_dash.app.components.base import Component


LOCALIZATION_FILE = "visualizations.yml"


class Visualizations(Component):
    """Creates graphs, tables and download links for data

    Categories
    * new addmissions
    * admitted patients
    * Simulated SIR data
    """
    localization_file = "visualizations.yml"

    def get_html(self) -> List[ComponentMeta]:
        """Initializes the header dash html
        """
        today = date.today().strftime(self.content["date-format"])
        return [
            H2(self.content["new-admissions-title"]),
            Markdown(self.content["new-admissions-text"]),
            Graph(id="new_admissions_graph"),
            A(
                self.content["download-text"],
                id="new_admissions_download",
                download="admissions_{}.csv".format(today),
                href="",
                target="_blank",
                className="btn btn-sm btn-info my-2",
            ),
            Div(
                className="row justify-content-center",
                children=Div(
                    id="new_admissions_table_container",
                    className="col-auto",
                    children=[
                        Table(id="new_admissions_table", className="table-responsive"),
                    ],
                ),
            ),
            H2(self.content["admitted-patients-title"]),
            Markdown(self.content["admitted-patients-text"]),
            Graph(id="admitted_patients_graph"),
            A(
                self.content["download-text"],
                id="admitted_patients_download",
                download="census_{}.csv".format(today),
                href="",
                target="_blank",
                className="btn btn-sm btn-info my-4",
            ),
            Div(
                className="row justify-content-center",
                children=Div(
                    id="admitted_patients_table_container",
                    className="col-auto",
                    children=[
                        Table(
                            id="admitted_patients_table", className="table-responsive"
                        ),
                    ],
                ),
            ),
            H2(self.content["SIR-title"]),
            Markdown(self.content["SIR-text"]),
            Graph(id="SIR_graph"),
            A(
                self.content["download-text"],
                id="SIR_download",
                download="SIR_{}.csv".format(today),
                href="",
                target="_blank",
                className="btn btn-sm btn-info my-4",
            ),
            Div(
                className="row justify-content-center",
                children=Div(
                    id="SIR_table_container",
                    className="col-auto",
                    children=[Table(id="SIR_table", className="table-responsive"),],
                ),
            ),
        ]

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
