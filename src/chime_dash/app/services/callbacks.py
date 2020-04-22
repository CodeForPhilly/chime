from collections import OrderedDict, defaultdict
from datetime import datetime, date
from typing import List
from urllib.parse import parse_qsl, urlencode

from dash.exceptions import PreventUpdate

from chime_dash.app.utils import (
    get_n_switch_values,
    parameters_deserializer,
    parameters_serializer,
    prepare_visualization_group
)
from chime_dash.app.utils.callbacks import ChimeCallback, register_callbacks
from penn_chime.model.sir import Sir
from penn_chime.model.parameters import Parameters, Disposition


class ComponentCallbacks:
    def __init__(self, callbacks: List[ChimeCallback], component_instance):
        self._callbacks = callbacks
        self._component_instance = component_instance
        register_callbacks(self._callbacks)


class IndexCallbacks(ComponentCallbacks):

    @staticmethod
    def toggle_tables(switch_value):
        return get_n_switch_values(not switch_value, 3)

    @staticmethod
    def change_btn_color(n_clicks):
        try:
            return [False] if n_clicks % 2 == 0 else [True]
        except:
            return [False]

    @staticmethod
    def handle_model_change(i, sidebar_data, lock_zoom_clicks, graphs_relayout_data):
        model = {}
        pars = None
        result = []
        viz_kwargs = {}
        if sidebar_data:
            pars = parameters_deserializer(sidebar_data["parameters"])
            model = Sir(pars)
            vis = i.components.get("visualizations", None) if i else None
            vis_content = vis.content if vis else None

            viz_kwargs = dict(
                labels=pars.labels,
                table_mod=7,
                content=vis_content
            )
        result.extend(i.components["intro"].build(model, pars))
        for df_key in ["admits_df", "census_df", "sim_sir_w_date_df"]:
            df = None
            if model:
                df = model.__dict__.get(df_key, None)
            result.extend(prepare_visualization_group(df, **viz_kwargs))

        figures = [result[1], result[4], result[7]]

        for n_clicks, relayout_data, figure in zip(lock_zoom_clicks, graphs_relayout_data, figures):
            if relayout_data:
                if n_clicks == None or n_clicks % 2 == 0:
                    # Set plot_data figure coordinates 
                    if "xaxis.range[0]" in relayout_data:
                        figure["layout"]["xaxis"]["range"] = [
                            relayout_data["xaxis.range[0]"],
                            relayout_data["xaxis.range[1]"]
                        ]
                    if "yaxis.range[0]" in relayout_data:
                        figure["layout"]["yaxis"]["range"] = [
                            relayout_data["yaxis.range[0]"],
                            relayout_data["yaxis.range[1]"]
                        ]
                            
        return result

    def __init__(self, component_instance):
        def handle_model_change_helper(
            sidebar_mod, 
            new_admissions_lock_zoom, 
            admitted_patients_lock_zoom,
            SIR_lock_zoom,
            sidebar_data, 
            new_admissions_relayout_data, 
            admitted_patients_relayout_data,
            SIR_relayout_data
            ):
            # parameter order: Inputs (sidebar_mod and all lock_zooms) followed by States (sidebar_data and all relayout_datas)
            # Order matters; callback_wrapper passes in Inputs before States
            lock_zoom_clicks = [new_admissions_lock_zoom, admitted_patients_lock_zoom, SIR_lock_zoom]
            graphs_relayout_data = [new_admissions_relayout_data, admitted_patients_relayout_data, SIR_relayout_data]
            return IndexCallbacks.handle_model_change(component_instance, sidebar_data, lock_zoom_clicks, graphs_relayout_data)

        super().__init__(
            component_instance=component_instance,
            callbacks=[
                ChimeCallback(  # If user toggles show_tables, show/hide tables
                    changed_elements={"show_tables": "on"},
                    dom_updates={
                        "SIR_table_container": "hidden",
                        "new_admissions_table_container": "hidden",
                        "admitted_patients_table_container": "hidden",
                    },
                    callback_fn=IndexCallbacks.toggle_tables
                ),
                ChimeCallback(  # If the parameters or model change, update the text
                    changed_elements={
                        "sidebar-store": "modified_timestamp",
                        "new_admissions_lock_zoom": "n_clicks",
                        "admitted_patients_lock_zoom": "n_clicks",
                        "SIR_lock_zoom": "n_clicks"
                        },
                    dom_updates={
                        "intro": "children",
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
                    states={
                        "new_admissions_graph": "relayoutData",
                        "admitted_patients_graph": "relayoutData",
                        "SIR_graph": "relayoutData"
                        },
                    stores=["sidebar-store"],
                    callback_fn=handle_model_change_helper
                ),
                ChimeCallback( # If user presses the Lock Zoom Button, update outline / solid color
                    changed_elements={"new_admissions_lock_zoom": "n_clicks"},
                    dom_updates={"new_admissions_lock_zoom": "outline"},
                    callback_fn=IndexCallbacks.change_btn_color
                ),
                ChimeCallback(
                    changed_elements={"admitted_patients_lock_zoom": "n_clicks"},
                    dom_updates={"admitted_patients_lock_zoom": "outline"},
                    callback_fn=IndexCallbacks.change_btn_color
                ),
                ChimeCallback(
                    changed_elements={"SIR_lock_zoom": "n_clicks"},
                    dom_updates={"SIR_lock_zoom": "outline"},
                    callback_fn=IndexCallbacks.change_btn_color
                )
            ]
        )


class SidebarCallbacks(ComponentCallbacks):

    @staticmethod
    def get_formated_values(i, input_values):
        result = dict(zip(i.input_value_map.keys(), input_values))
        for key, input_type in i.input_type_map.items():
            if input_type == "date":
                value = result[key]
                try:
                    result[key] = datetime.strptime(value, "%Y-%m-%d").date() if value else value
                except ValueError:
                    pass
        return result

    @staticmethod
    def update_parameters(i, *input_values) -> List[dict]:
        """Reads html form outputs and converts them to a parameter instance

        Returns Parameters
        """
        inputs_dict = SidebarCallbacks.get_formated_values(i, input_values)
        dt = inputs_dict["doubling_time"] if inputs_dict["doubling_time"] else None
        dfh = inputs_dict["date_first_hospitalized"] if not dt else None
        pars = Parameters(
            current_hospitalized=inputs_dict["current_hospitalized"],
            date_first_hospitalized=dfh,
            doubling_time=dt,
            hospitalized=Disposition.create(
                days=inputs_dict["hospitalized_los"],
                rate=inputs_dict["hospitalized_rate"] / 100,
            ),
            icu=Disposition(
                days=inputs_dict["icu_los"],
                rate=inputs_dict["icu_rate"] / 100,
            ),
            infectious_days=inputs_dict["infectious_days"],
            market_share=inputs_dict["market_share"] / 100,
            n_days=inputs_dict["n_days"],
            population=inputs_dict["population"],
            recovered=0,  #FIXME input or pass through from defaults is required!
            relative_contact_rate=inputs_dict["relative_contact_rate"] / 100,
            ventilated=Disposition.create(
                days=inputs_dict["ventilated_los"],
                rate=inputs_dict["ventilated_rate"] / 100,
            )
        )
        return [{"inputs_dict": inputs_dict, "parameters": parameters_serializer(pars)}]

    def __init__(self, component_instance):
        def update_parameters_helper(*args, **kwargs):
            input_values = list(args)
            input_dict = dict(zip(component_instance.input_value_map.keys(), input_values))
            sidebar_data = input_values.pop(-1)
            if sidebar_data and input_dict and input_dict == sidebar_data["inputs_dict"]:
                raise PreventUpdate
            return SidebarCallbacks.update_parameters(component_instance, *args)

        super().__init__(
            component_instance=component_instance,
            callbacks=[
                ChimeCallback(
                    changed_elements=component_instance.input_value_map,
                    dom_updates={"sidebar-store": "data"},
                    callback_fn=update_parameters_helper,
                    stores=["sidebar-store"],
                )
            ]
        )


# todo Add tons of tests and validation because there be dragons
class RootCallbacks(ComponentCallbacks):
    @staticmethod
    def try_parsing_number(v):
        if v == 'None':
            result = None
        else:
            try:
                result = int(v)
            except ValueError:
                try:
                    result = float(v)
                except ValueError:
                    result = v
        return result

    @staticmethod
    def get_inputs(val_dict, inputs_keys):
        # todo handle versioning of inputs
        return OrderedDict((key, value) for key, value in val_dict.items() if key in inputs_keys)

    @staticmethod
    def parse_hash(hash_str, sidebar_input_types):
        hash_dict = dict(parse_qsl(hash_str[1:]))
        for key, value in hash_dict.items():
            value_type = sidebar_input_types[key]
            if value_type == "number":
                parsed_value = RootCallbacks.try_parsing_number(value)
            elif value == 'None':
                parsed_value = None
            elif value == 'True':
                parsed_value = True
            elif value == 'False':
                parsed_value = False
            else:
                parsed_value = value
            hash_dict[key] = parsed_value
        return hash_dict

    @staticmethod
    def hash_changed(sidebar_input_types, hash_str=None, root_data=None):
        if hash_str:
            hash_dict = RootCallbacks.parse_hash(hash_str, sidebar_input_types)
            # Fix that empty values encodes to 'None' string in url
            result = RootCallbacks.get_inputs(hash_dict, sidebar_input_types.keys())
            # Don't update the data store if it already contains the same data
            if result == root_data:
                raise PreventUpdate
        else:
            raise PreventUpdate
        return [result]

    @staticmethod
    def stores_changed(inputs_keys, root_mod, sidebar_mod, root_data, sidebar_data):
        root_modified = root_mod or 0
        sidebar_modified = sidebar_mod or 0
        if root_data and sidebar_data and root_data == sidebar_data.get("inputs_dict", None):
            raise PreventUpdate
        if (root_modified + 100) < sidebar_modified:
            inputs_dict = sidebar_data["inputs_dict"]
            new_val = RootCallbacks.get_inputs(inputs_dict, inputs_keys)
        elif root_modified > (sidebar_modified + 100):
            new_val = RootCallbacks.get_inputs(root_data, inputs_keys)
        else:
            raise PreventUpdate

        # Spread parameters toggle handling
        if sidebar_data.get('inputs_dict', {}).get('spread_parameters_checkbox'):
            styles = {
                'date_first_hospitalized': None,
                'doubling_time': {'display': 'none'}
            }
            new_val['doubling_time'] = None
            new_val['date_first_hospitalized'] = date(year=2020, month=4, day=1)
        else:
            styles = {
                'date_first_hospitalized': {'display': 'none'},
                'doubling_time': None
            }
            new_val['date_first_hospitalized'] = None
            if new_val['doubling_time'] is None:
                new_val['doubling_time'] = 1

        # Social distancing handler
        if sidebar_data.get('inputs_dict', {}).get('social_distancing_checkbox'):
            styles.update({
                'social_distancing_start_date': None,
                'relative_contact_rate': None
            })
            if not new_val['social_distancing_start_date']:
                new_val['social_distancing_start_date'] = new_val['current_date']
        else:
            styles.update({
                'social_distancing_start_date': {'display': 'none'},
                'relative_contact_rate': {'display': 'none'}
            })
            new_val['relative_contact_rate'] = 0

        if not styles['date_first_hospitalized']:
            print(sidebar_data.get('inputs_dict', {}).get('spread_parameters_checkbox'))
        return ["#{}".format(urlencode(new_val))] + list(new_val.values()) + list(styles.values())

    def __init__(self, component_instance):
        sidebar = component_instance.components["sidebar"]
        sidebar_inputs = sidebar.input_value_map
        sidebar_input_types = sidebar.input_type_map

        def hash_changed_helper(hash_str=None, root_data=None):
            return RootCallbacks.hash_changed(sidebar_input_types, hash_str, root_data)

        def stores_changed_helper(root_mod, sidebar_mod, root_data, sidebar_data):
            return RootCallbacks.stores_changed(sidebar_inputs.keys(),
                                                root_mod,
                                                sidebar_mod,
                                                root_data,
                                                sidebar_data)

        super().__init__(
            component_instance=component_instance,
            callbacks=[
                ChimeCallback(
                    changed_elements={"location": "hash"},
                    dom_updates={"root-store": "data"},
                    callback_fn=hash_changed_helper,
                    stores=["root-store"],
                ),
                ChimeCallback(
                    changed_elements={"root-store": "modified_timestamp", "sidebar-store": "modified_timestamp"},
                    dom_updates={"location": "hash", **sidebar_inputs},
                    dom_states=sidebar.input_state_map,
                    callback_fn=stores_changed_helper,
                    stores=["root-store", "sidebar-store"],
                ),
            ]
        )
