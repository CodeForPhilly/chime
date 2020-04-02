from typing import List
from datetime import date, datetime

from chime_dash.app.utils.callbacks import ChimeCallback, register_callbacks
from chime_dash.app.utils import (
    get_n_switch_values,
    parameters_deserializer,
    parameters_serializer,
    prepare_visualization_group
)

from penn_chime.models import SimSirModel
from penn_chime.parameters import Parameters, Disposition


class ComponentCallbacks:
    def __init__(self, callbacks: List[ChimeCallback], component_instance):
        self._callbacks = callbacks
        self._component_instance = component_instance
        register_callbacks(self._callbacks)


class IndexCallbacks(ComponentCallbacks):
    @staticmethod
    def toggle_tool_details(switch_value):
        return get_n_switch_values(switch_value, 1)

    @staticmethod
    def toggle_tables(switch_value):
        return get_n_switch_values(switch_value, 3)

    @staticmethod
    def handle_model_change(i, pars_json):
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
        result.extend(i.components["intro"].build(model, pars))
        result.extend(i.components["tool_details"].build(model, pars))
        for df_key in ["admits_df", "census_df", "sim_sir_w_date_df"]:
            df = None
            if model:
                df = model.__dict__.get(df_key, None)
            result.extend(prepare_visualization_group(df, **viz_kwargs))
        return result

    def __init__(self, component_instance):
        def handle_model_change_helper(pars_json):
            return IndexCallbacks.handle_model_change(component_instance, pars_json)

        super().__init__(
            component_instance=component_instance,
            callbacks=[
                ChimeCallback(  # If user toggles show_additional_projections, show/hide the additional intro content
                    changed_elements={"show_tool_details": "value"},
                    dom_updates={"more_intro_wrapper": "hidden"},
                    callback_fn=IndexCallbacks.toggle_tool_details
                ),
                ChimeCallback(  # If user toggles show_tables, show/hide tables
                    changed_elements={"show_tables": "value"},
                    dom_updates={
                        "SIR_table_container": "hidden",
                        "new_admissions_table_container": "hidden",
                        "admitted_patients_table_container": "hidden",
                    },
                    callback_fn=IndexCallbacks.toggle_tables
                ),
                ChimeCallback(  # If the parameters or model change, update the text
                    changed_elements={"pars": "children"},
                    dom_updates={
                        "intro": "children",
                        "more_intro": "children",
                        "new_admissions_graph": "figure",
                        "new_admissions_table": "children",
                        "new_admissions_download": "href",
                        "admitted_patients_graph": "figure",
                        "admitted_patients_table": "children",
                        "admitted_patients_download": "href",
                        "SIR_graph": "figure",
                        "SIR_table": "children",
                        "SIR_download": "href",
                    },
                    callback_fn=handle_model_change_helper
                )
            ]
        )


class SidebarCallbacks(ComponentCallbacks):

    @staticmethod
    def get_formated_values(i, input_values):
        result = dict(zip(i.input_value_map.keys(), input_values))
        for key, input_type in i.input_type_map.items():
            # todo remove this hack needed because of how Checklist type (used for switch input) returns values
            if input_type == "switch":
                result[key] = False if result[key] == [True] else True
            elif input_type == "date":
                value = result[key]
                result[key] = datetime.strptime(value, "%Y-%m-%d").date() if value else value
        return result

    @staticmethod
    def update_parameters(i, *input_values) -> List[str]:
        """Reads html form outputs and converts them to a parameter instance

        Returns Parameters
        """
        inputs_dict = SidebarCallbacks.get_formated_values(i, input_values)
        dt = inputs_dict["doubling_time"] if inputs_dict["doubling_time"] else None
        dfh = inputs_dict["date_first_hospitalized"] if not dt else None
        pars = Parameters(
            population=inputs_dict["population"],
            current_hospitalized=inputs_dict["current_hospitalized"],
            date_first_hospitalized=dfh,
            doubling_time=dt,
            hospitalized=Disposition(
                inputs_dict["hospitalized_rate"] / 100, inputs_dict["hospitalized_los"]
            ),
            icu=Disposition(inputs_dict["icu_rate"] / 100, inputs_dict["icu_los"]),
            infectious_days=inputs_dict["infectious_days"],
            market_share=inputs_dict["market_share"] / 100,
            n_days=inputs_dict["n_days"],
            relative_contact_rate=inputs_dict["relative_contact_rate"] / 100,
            ventilated=Disposition(
                inputs_dict["ventilated_rate"] / 100, inputs_dict["ventilated_los"]
            ),
            max_y_axis=inputs_dict.get("max_y_axis_value", None),
        )
        return [parameters_serializer(pars)]

    def __init__(self, component_instance):
        def update_parameters_helper(*args, **kwargs):
            return SidebarCallbacks.update_parameters(component_instance, *args)

        super().__init__(
            component_instance=component_instance,
            callbacks=[
                ChimeCallback(
                    changed_elements=component_instance.input_value_map,
                    dom_updates={"pars": "children"},
                    callback_fn=update_parameters_helper
                )
            ]
        )
