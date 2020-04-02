"""components/visualizations

Initializes the visual components of the interactive model

localization file can be found in app/templates/en
"""
from typing import List
from datetime import date

from dash.development.base_component import ComponentMeta
from dash_html_components import H2, Div, A
from dash_core_components import Markdown, Graph
from dash_bootstrap_components import Table, Container

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
            Container(
                className="mt-5",
                children=[
                    H2(self.content["new-admissions-title"]),
                    Markdown(self.content["new-admissions-text"]),
                ]
            ),
            Container(fluid=True, children=Graph(id="new_admissions_graph")),
            Container([
                A(
                    self.content["download-text"],
                    id="new_admissions_download",
                    download="admissions_{}.csv".format(today),
                    href="",
                    target="_blank",
                    className="btn btn-sm btn-info",
                ),
                Div(
                    className="row justify-content-center",
                    children=Div(
                        id="new_admissions_table_container",
                        className="col-auto",
                        children=Table(
                            id="new_admissions_table",
                            className="table-responsive mx-auto"
                        ),
                    ),
                ),
            ]),
            Container(
                className="mt-5",
                children=[
                    H2(self.content["admitted-patients-title"]),
                    Markdown(self.content["admitted-patients-text"]),
                ],
            ),
            Container(fluid=True, children=Graph(id="admitted_patients_graph")),
            Container([
                A(
                    self.content["download-text"],
                    id="admitted_patients_download",
                    download="census_{}.csv".format(today),
                    href="",
                    target="_blank",
                    className="btn btn-sm btn-info",
                ),
                Div(
                    className="row justify-content-center",
                    children=Div(
                        id="admitted_patients_table_container",
                        className="col-auto",
                        children=Table(
                            id="admitted_patients_table",
                            className="table-responsive"
                        ),
                    ),
                ),
            ]),
            Container(
                className="mt-5",
                children=[
                    H2(self.content["SIR-title"]),
                    Markdown(self.content["SIR-text"]),
                ],
            ),
            Container(fluid=True, children=Graph(id="SIR_graph")),
            Container([
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
                        children=Table(
                            id="SIR_table",
                            className="table-responsive"
                        ),
                    ),
                ),
            ])
        ]
