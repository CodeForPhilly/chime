"""pages/index
Homepage
"""

from collections import OrderedDict

import dash_bootstrap_components as dbc

from chime_dash.app.components.base import Component
from chime_dash.app.components.footer import Footer
from chime_dash.app.components.header import Header
from chime_dash.app.components.tool_details import ToolDetails
from chime_dash.app.components.additions import Additions
from chime_dash.app.components.intro import Intro
from chime_dash.app.components.visualizations import Visualizations

from chime_dash.app.utils import get_n_switch_values, build_csv_download, parameters_deserializer
from chime_dash.app.utils.callbacks import ChimeCallback
from chime_dash.app.utils.templates import df_to_html_table, read_localization_markdown
from chime_dash.app.services.plotting import plot_dataframe

from penn_chime.models import SimSirModel
from penn_chime.utils import add_date_column


class Index(Component):
    """
    """

    @staticmethod
    def build_graphs_and_tables(model, pars, show_more, content):
        admissions_data = {}
        admissions_table_data = None
        census_data = {}
        census_table_data = None
        evo_figure = {}
        evo_table = None
        admissions_csv = None
        census_csv = None

        if model and pars:
            projection_admits = model.admits_df
            census_df = model.census_df
            time_evolution = model.raw_df
            time_evolution["day"] = time_evolution.index

            if pars.as_date:
                projection_admits = add_date_column(projection_admits, drop_day_column=True).set_index("date")
                census_df = add_date_column(census_df, drop_day_column=True).set_index("date")
                time_evolution = add_date_column(time_evolution, drop_day_column=True).set_index("date")
            else:
                projection_admits = projection_admits.set_index("day")
                census_df = census_df.set_index("day")
                time_evolution = time_evolution.set_index("day")

            projection_admits = projection_admits.fillna(0).astype(int)
            census_df.iloc[0, :] = 0
            census_df = census_df.dropna().astype(int)

            # Create admissions figure
            admissions_data = plot_dataframe(projection_admits.head(pars.n_days - 10), max_y_axis=pars.max_y_axis)

            # Create admissions table data
            if pars.as_date:
                projection_admits.index = projection_admits.index.strftime("%b, %d")
            admissions_table_data = dbc.Table(df_to_html_table(projection_admits, data_only=True, n_mod=7))

            # Create census figure
            census_data = plot_dataframe(census_df.head(pars.n_days - 10), max_y_axis=pars.max_y_axis)
            # Create admissions table data
            if pars.as_date:
                census_df.index = census_df.index.strftime("%b, %d")
            census_table_data = dbc.Table(df_to_html_table(census_df, data_only=True, n_mod=7))

            if show_more:
                time_evolution = time_evolution.rename(
                    columns={key: content[key] for key in time_evolution.columns}
                ).astype(int)

                evo_figure = plot_dataframe(
                    time_evolution.drop(columns=content["susceptible"]).head(pars.n_days - 10),
                    max_y_axis=pars.max_y_axis
                )
                evo_figure["layout"]["height"] = 450
                evo_table = dbc.Table(df_to_html_table(time_evolution, data_only=True, n_mod=7))

            admissions_csv = build_csv_download(projection_admits)
            census_csv = build_csv_download(census_df)

        return [
            admissions_data, admissions_table_data,
            census_data, census_table_data,
            evo_figure, evo_table,
            admissions_csv, census_csv
        ]

    @staticmethod
    def toggle_additions(switch_value):
        return get_n_switch_values(switch_value, 1)

    @staticmethod
    def toggle_tool_details(switch_value):
        return get_n_switch_values(switch_value, 1)

    @staticmethod
    def toggle_tables(switch_value):
        return get_n_switch_values(switch_value, 5)

    def __init__(self, language, defaults):
        """
        """

        def handle_model_change_helper(pars_json, show_additional_projections):
            model = None
            pars = None
            show_more = True if show_additional_projections == [True] else False
            if pars_json:
                pars = parameters_deserializer(pars_json)
                model = SimSirModel(pars)

            intro = self.components["intro"].build(model, pars)
            more_intro = self.components["tool_details"].build(model, pars)
            figures_and_tables = Index.build_graphs_and_tables(
                model,
                pars,
                show_more,
                self.components["additions"].content
            )
            return intro + more_intro + figures_and_tables

        super().__init__(language, defaults, [
            ChimeCallback(  # If user toggles show_additional_projections, show/hide the additions content
                changed_elements=OrderedDict(show_additional_projections="value"),
                dom_updates=OrderedDict(additions="hidden"),
                callback_fn=Index.toggle_additions
            ),
            ChimeCallback(  # If user toggles show_additional_projections, show/hide the additions content
                changed_elements=OrderedDict(show_tool_details="value"),
                dom_updates=OrderedDict(more_intro_wrapper="hidden"),
                callback_fn=Index.toggle_tool_details
            ),
            ChimeCallback(  # If user toggles show_tables, show/hide tables
                changed_elements=OrderedDict(show_tables="value"),
                dom_updates=OrderedDict(
                    infected_v_revovered_table="hidden",
                    new_admissions_table="hidden",
                    admitted_patients_table="hidden",
                    download_admissions="hidden",
                    download_census="hidden"
                ),
                callback_fn=Index.toggle_tables
            ),
            ChimeCallback(  # If the parameters or model change, update the text
                changed_elements=OrderedDict(pars="children", show_additional_projections="value"),
                dom_updates=OrderedDict(
                    intro="children",
                    more_intro="children",
                    new_admissions_graph="figure",
                    new_admissions_table="children",
                    admitted_patients_graph="figure",
                    admitted_patients_table="children",
                    infected_v_revovered_graph="figure",
                    infected_v_revovered_table="children",
                    download_admissions="href",
                    download_census="href"
                ),
                callback_fn=handle_model_change_helper
            )
        ])
        self.components = OrderedDict(
            header=Header(language, defaults),
            intro=Intro(language, defaults),
            tool_details=ToolDetails(language, defaults),
            visualizations=Visualizations(language, defaults),
            additions=Additions(language, defaults),
            footer=Footer(language, defaults),
        )

    def get_html(self):
        """Initializes the content container dash html
        """
        content = dbc.Col(
            children=self.components["header"].html
                     + self.components["intro"].html
                     + self.components["tool_details"].html
                     + self.components["visualizations"].html
                     + self.components["additions"].html
                     + self.components["footer"].html,
            width=9,
            className="ml-sm-auto p-5",
        )

        return [content]
