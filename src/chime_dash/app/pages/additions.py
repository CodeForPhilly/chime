"""components/additions
currently handles both view and logic should be separated
graph activated via "Show additional projections"
"""
from typing import List, Any
from collections import OrderedDict

from dash.dependencies import Output
from dash.development.base_component import ComponentMeta
from dash_html_components import H4, Div
from dash_core_components import Graph
from dash_bootstrap_components import Table

from penn_chime.utils import add_date_column
from penn_chime.models import SimSirModel

from chime_dash.app.utils.callbacks import ChimeCallback
from chime_dash.app.utils.templates import df_to_html_table
from chime_dash.app.services.plotting import plot_dataframe
from chime_dash.app.components.base import Component


class Additions(Component):
    """
    """
    @staticmethod
    def show_hide_additions(show_additional_projections):
        return [not show_additional_projections]

    @staticmethod
    def show_hide_additions_table(show_tables):
        return [not show_tables]

    @staticmethod
    def build_graph_and_table(model_json, max_y_axis_value, as_date, content):
        figure = None
        table = None

        if model_json:
            model = SimSirModel.from_json(model_json)
            time_evolution = model.raw_df
            time_evolution["day"] = time_evolution.index

            # Convert columns
            if as_date:
                time_evolution = add_date_column(time_evolution, drop_day_column=True).set_index("date")
            else:
                time_evolution = time_evolution.set_index("day")

            time_evolution = time_evolution.rename(
                columns={key: content[key] for key in time_evolution.columns}
            ).astype(int)

            figure = plot_dataframe(time_evolution.drop(columns=content["susceptible"]), max_y_axis=max_y_axis_value)
            table = Table(df_to_html_table(time_evolution, data_only=True, n_mod=7))

        return [figure, table]

    localization_file = "additions.yml"

    def __init__(self, language, defaults):
        def build_graph_and_table_helper(model, max_y_axis_value, as_date):
            return Additions.build_graph_and_table(model, max_y_axis_value, as_date, self.content)
        super().__init__(language, defaults, [
            ChimeCallback(  # If user toggles show_additional_projections, show/hide the additions content
                changed_elements=OrderedDict(show_additional_projections="value"),
                dom_updates=OrderedDict(additions="hidden"),
                callback_fn=Additions.show_hide_additions
            ),
            ChimeCallback(  # If user toggles show_additional_projections, show/hide the table
                changed_elements=OrderedDict(show_tables="value"),
                dom_updates=OrderedDict(infected_v_revovered_table="hidden"),
                callback_fn=Additions.show_hide_additions_table
            ),
            ChimeCallback(  # If the max_y_axis or as_date inputs or model change, update the graph and table
                changed_elements=OrderedDict(model="children", max_y_axis_value="value", as_date="value"),
                dom_updates=OrderedDict(infected_v_revovered_graph="figure", infected_v_revovered_table="children"),
                callback_fn=build_graph_and_table_helper
            )
        ])

    def get_html(self) -> List[ComponentMeta]:
        """Initializes the header dash html
        """
        return [Div(
            id="additions",
            hidden=True,
            children=[
                H4(self.content["infected-v-revovered-title"]),
                Graph(id="infected_v_revovered_graph"),
                Div(id="infected_v_revovered_table", hidden=True)
            ]
        )]
