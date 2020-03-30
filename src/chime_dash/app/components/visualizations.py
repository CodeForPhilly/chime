"""components/visualizations

Initializes the visual components of the interactive model

localization file can be found in app/templates/en
"""
from typing import List
from datetime import date
import urllib.parse

from dash.development.base_component import ComponentMeta
from dash_html_components import H2, Div, A
from dash_core_components import Markdown, Graph
from chime_dash.app.components.base import Component

LOCALIZATION_FILE = "visualizations.yml"


class Visualizations(Component):
    """
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
                id='download_admissions',
                download="admissions_{}.csv".format(today),
                href="",
                target="_blank",
                className="btn btn-sm btn-info"
            ),
            Div(id="new_admissions_table"),
            H2(self.content["admitted-patients-title"]),
            Markdown(self.content["admitted-patients-text"]),
            Graph(id="admitted_patients_graph"),
            A(
                self.content["download-text"],
                id='download_census',
                download="census_{}.csv".format(today),
                href="",
                target="_blank",
                className="btn btn-sm btn-info"
            ),
            Div(id="admitted_patients_table"),
        ]
