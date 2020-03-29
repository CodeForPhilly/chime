"""components/visualizations

Initializes the visual components of the interactive model

localization file can be found in app/templates/en
"""
from typing import List
from collections import OrderedDict

from dash.development.base_component import ComponentMeta
from dash_html_components import H2, Div
from dash_core_components import Markdown, Graph
from dash_bootstrap_components import Table

from penn_chime.utils import add_date_column
from penn_chime.models import SimSirModel

from chime_dash.app.utils.callbacks import ChimeCallback
from chime_dash.app.utils.templates import df_to_html_table
from chime_dash.app.services.plotting import plot_dataframe
from chime_dash.app.components.base import Component

LOCALIZATION_FILE = "visualizations.yml"


class Visualizations(Component):
    """
    """

    localization_file = "visualizations.yml"

    def callback(self, *args, **kwargs):
        """Renders the parameter dependent plots and tables
        """

    @staticmethod
    def show_hide_tables(show_tables):
        return [not show_tables, not show_tables]

    @staticmethod
    def build_graphs_and_tables(model_json, max_y_axis_value, n_days, as_date):
        result = [None, None, None, None]
        if model_json:
            model = SimSirModel.from_json(model_json)
            projection_admits = model.admits_df
            census_df = model.census_df

            if as_date:
                projection_admits = add_date_column(projection_admits, drop_day_column=True).set_index("date")
                census_df = add_date_column(census_df, drop_day_column=True).set_index("date")
            else:
                projection_admits = projection_admits.set_index("day")
                census_df = census_df.set_index("day")

            projection_admits = projection_admits.fillna(0).astype(int)
            census_df.iloc[0, :] = 0
            census_df = census_df.dropna().astype(int)

            # Create admissions figure
            admissions_data = plot_dataframe(projection_admits.head(n_days - 10), max_y_axis=max_y_axis_value)

            # Create admissions table data
            if as_date:
                projection_admits.index = projection_admits.index.strftime("%b, %d")
            admissions_table_data = Table(df_to_html_table(projection_admits, data_only=True, n_mod=7))

            # Create census figure
            census_data = plot_dataframe(census_df.head(n_days - 10), max_y_axis=max_y_axis_value)
            # Create admissions table data
            if as_date:
                census_df.index = census_df.index.strftime("%b, %d")
            census_table_data = Table(df_to_html_table(census_df, data_only=True, n_mod=7))

            result = [admissions_data, admissions_table_data, census_data, census_table_data]
        return result

    def __init__(self, language, defaults):
        super().__init__(language, defaults, [
            ChimeCallback(  # If user toggles tables, show/hide the table
                changed_elements=OrderedDict(show_tables="value"),
                dom_updates=OrderedDict(new_admissions_table="hidden", admitted_patients_table="hidden"),
                callback_fn=Visualizations.show_hide_tables
            ),
            ChimeCallback(  # If the max_y_axis or as_date inputs, parameters, or model changes, update everything
                changed_elements=OrderedDict(
                    model="children",
                    max_y_axis_value="value",
                    n_days="value",
                    as_date="value"
                ),
                dom_updates=OrderedDict(
                    new_admissions_graph="figure",
                    new_admissions_table="children",
                    admitted_patients_graph="figure",
                    admitted_patients_table="children"
                ),
                callback_fn=Visualizations.build_graphs_and_tables
            )
        ])

    def get_html(self) -> List[ComponentMeta]:
        """Initializes the header dash html
        """
        return [
            H2(self.content["new-admissions-title"]),
            Markdown(self.content["new-admissions-text"]),
            Graph(id="new_admissions_graph"),
            Div(id="new_admissions_table"),
            H2(self.content["admitted-patients-title"]),
            Markdown(self.content["admitted-patients-text"]),
            Graph(id="admitted_patients_graph"),
            Div(id="admitted_patients_table"),
        ]
