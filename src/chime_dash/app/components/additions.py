"""Initializes the  dash html
"""
from typing import List, Any

from pandas import DataFrame

from dash.dependencies import Output
from dash.development.base_component import ComponentMeta
from dash_html_components import H4, Div
from dash_core_components import Graph
from dash_bootstrap_components import Table

from penn_chime.utils import add_date_column
from penn_chime.parameters import Parameters

from chime_dash.app.utils.templates import df_to_html_table
from chime_dash.app.services.plotting import plot_dataframe

from chime_dash.app.components.base import Component


class Additions(Component):
    """
    """

    localization_file = "additions.yml"
    callback_outputs = [Output(component_id="additions", component_property="children")]

    def get_html(self) -> List[ComponentMeta]:
        """Initializes the header dash html
        """
        return [Div(id="additions")]

    def callback(self, *args, **kwargs) -> List[Any]:
        """Renders the parameter dependent plots and tables
        """
        pars = kwargs["pars"]

        if kwargs["show_additional_projections"]:
            title = self.content["infected-v-revovered-title"]

            time_evolution = self._build_frame(**kwargs)

            time_evolution_data = plot_dataframe(
                time_evolution.drop(columns=self.content["susceptible"]),
                max_y_axis=pars.max_y_axis,
            )

            children = [
                H4(title, id="infected-v-revovered-title"),
                Graph(figure=time_evolution_data, id="infected-v-revovered-graph"),
            ]

            if kwargs["show_tables"]:
                if kwargs["as_date"]:
                    time_evolution.index = time_evolution.index.strftime("%b, %d")
                time_evolution_table_data = (
                    df_to_html_table(time_evolution, data_only=True, n_mod=7)
                    if kwargs["show_tables"]
                    else {}
                )
                children.append(
                    Table(time_evolution_table_data, id="infected-v-revovered-table")
                )

        else:
            children = []

        return [children]

    def _build_frame(self, **kwargs):

        # Prepare admissions data & census data
        time_evolution = kwargs["model"].raw_df
        time_evolution["day"] = time_evolution.index

        # Convert columns
        if kwargs["as_date"]:
            time_evolution = add_date_column(
                time_evolution, drop_day_column=True
            ).set_index("date")
        else:
            time_evolution = time_evolution.set_index("day")

        return time_evolution.rename(
            columns={key: self.content[key] for key in time_evolution.columns}
        ).astype(int)
