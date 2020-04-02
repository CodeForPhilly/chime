"""pages/index
Homepage
"""

from collections import OrderedDict

from dash_html_components import Main
from dash_bootstrap_components import Container

from chime_dash.app.components.base import Component
from chime_dash.app.components.footer import Footer
from chime_dash.app.components.header import Header
from chime_dash.app.components.tool_details import ToolDetails
from chime_dash.app.components.intro import Intro
from chime_dash.app.components.visualizations import Visualizations

from chime_dash.app.utils import get_n_switch_values, parameters_deserializer, prepare_visualization_group
from chime_dash.app.utils.callbacks import ChimeCallback

from penn_chime.models import SimSirModel


class Index(Component):
    """
    """

    @staticmethod
    def toggle_tool_details(switch_value):
        return get_n_switch_values(switch_value, 1)

    @staticmethod
    def toggle_tables(switch_value):
        return get_n_switch_values(switch_value, 3)

    def __init__(self, language, defaults):
        """
        """

        def handle_model_change_helper(pars_json):
            model = {}
            pars = None
            result = []
            viz_kwargs = {}
            if pars_json:
                pars = parameters_deserializer(pars_json)
                model = SimSirModel(pars)
                viz_kwargs = dict(
                    labels=pars.labels,
                    table_mod=7,
                    max_y_axis=pars.max_y_axis,
                )
            result.extend(self.components["intro"].build(model, pars))
            result.extend(self.components["tool_details"].build(model, pars))
            for df_key in ["admits_df", "census_df", "sim_sir_w_date_df"]:
                df = None
                if model:
                    df = model.__dict__.get(df_key, None)
                result.extend(prepare_visualization_group(df, **viz_kwargs))
            return result

        super().__init__(language, defaults, [
            ChimeCallback(  # If user toggles show_additional_projections, show/hide the additional intro content
                changed_elements=OrderedDict(show_tool_details="value"),
                dom_updates=OrderedDict(more_intro_wrapper="hidden"),
                callback_fn=Index.toggle_tool_details
            ),
            ChimeCallback(  # If user toggles show_tables, show/hide tables
                changed_elements=OrderedDict(show_tables="value"),
                dom_updates=OrderedDict(
                    SIR_table_container="hidden",
                    new_admissions_table_container="hidden",
                    admitted_patients_table_container="hidden",
                ),
                callback_fn=Index.toggle_tables
            ),
            ChimeCallback(  # If the parameters or model change, update the text
                changed_elements=OrderedDict(pars="children"),
                dom_updates=OrderedDict(
                    intro="children",
                    more_intro="children",
                    new_admissions_graph="figure",
                    new_admissions_table="children",
                    new_admissions_download="href",
                    admitted_patients_graph="figure",
                    admitted_patients_table="children",
                    admitted_patients_download="href",
                    SIR_graph="figure",
                    SIR_table="children",
                    SIR_download="href",
                ),
                callback_fn=handle_model_change_helper
            )
        ])
        self.components = OrderedDict(
            header=Header(language, defaults),
            intro=Intro(language, defaults),
            tool_details=ToolDetails(language, defaults),
            visualizations=Visualizations(language, defaults),
            footer=Footer(language, defaults),
        )

    def get_html(self):
        """Initializes the content container dash html
        """
        content = Main(
            className="py-5",
            style={
                "marginLeft": "320px",
                "marginTop": "56px"
            },
            children=
            [Container(
                children=
                self.components["header"].html
                + self.components["intro"].html
                + self.components["tool_details"].html
            )]
            + self.components["visualizations"].html
            + [Container(
                children=
                self.components["footer"].html
            )],
        )

        return [content]
