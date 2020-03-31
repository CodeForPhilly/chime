"""components/sidebar
Initializes the side bar containing the various inputs for the model

#! _INPUTS should be considered for moving else where
"""
import dash_html_components as dhc

from typing import List, Dict, Any, Tuple
from collections import OrderedDict

from dash.development.base_component import ComponentMeta

from penn_chime.defaults import RateLos
from penn_chime.parameters import Parameters

from chime_dash.app.components.base import Component
from chime_dash.app.utils import parameters_serializer
from chime_dash.app.utils.templates import create_switch_input, create_number_input, create_header
from chime_dash.app.utils.callbacks import ChimeCallback

FLOAT_INPUT_MIN = 0.001
FLOAT_INPUT_STEP = "any"

_INPUTS = OrderedDict(
    regional_parameters={"type": "header", "size": "h3"},
    market_share={"type": "number", "min": FLOAT_INPUT_MIN, "step": FLOAT_INPUT_STEP, "max": 100.0, "percent": True},
    susceptible={"type": "number", "min": 1, "step": 1},
    known_infected={"type": "number", "min": 0, "step": 1},
    current_hospitalized={"type": "number", "min": 0, "step": 1},
    spread_and_contact={"type": "header", "size": "h3"},
    doubling_time={"type": "number", "min": FLOAT_INPUT_MIN, "step": FLOAT_INPUT_STEP},
    relative_contact_rate={
        "type": "number",
        "min": 0.0,
        "step": FLOAT_INPUT_STEP,
        "max": 100.0,
        "percent": True,
    },
    severity_parameters={"type": "header", "size": "h3"},
    hospitalized_rate={
        "type": "number",
        "min": 0.0,
        "step": FLOAT_INPUT_STEP,
        "max": 100.0,
        "percent": True,
    },
    icu_rate={
        "type": "number",
        "min": 0.0,
        "step": FLOAT_INPUT_STEP,
        "max": 100.0,
        "percent": True
    },
    ventilated_rate={
        "type": "number",
        "min": 0.0,
        "step": FLOAT_INPUT_STEP,
        "max": 100.0,
        "percent": True,
    },
    hospitalized_los={"type": "number", "min": 0, "step": 1},
    icu_los={"type": "number", "min": 0, "step": 1},
    ventilated_los={"type": "number", "min": 0, "step": 1},
    display_parameters={"type": "header", "size": "h3"},
    n_days={"type": "number", "min": 30, "step": 1},
    max_y_axis_value={"type": "number", "min": 10, "step": 10, "value": None},
    as_date={"type": "switch", "value": False},
    show_tables={"type": "switch", "value": False},
    show_tool_details={"type": "switch", "value": False},
    show_additional_projections={"type": "switch", "value": False},
)


class Sidebar(Component):
    """Sidebar to the left of the screen
    contains the various inputs used to interact
    with the model.
    """
    # localization temp. for widget descriptions
    localization_file = "sidebar.yml"

    @staticmethod
    def get_ordered_input_keys():
        return [key for key in _INPUTS if _INPUTS[key]["type"] not in ("header", )]

    @staticmethod
    def update_parameters(*input_values, **kwargs) -> List[str]:
        """
        """
        inputs_dict = dict(zip(Sidebar.get_ordered_input_keys(), input_values))
        # todo remove this hack needed because of how Checklist type used for switch input returns values
        for key in _INPUTS:
            if _INPUTS[key]["type"] == "switch":
                value = False
                if inputs_dict[key] == [True]:
                    value = True
                inputs_dict[key] = value
        pars = Parameters(
            current_hospitalized=inputs_dict["current_hospitalized"],
            doubling_time=inputs_dict["doubling_time"],
            known_infected=inputs_dict["known_infected"],
            relative_contact_rate=inputs_dict["relative_contact_rate"] / 100,
            susceptible=inputs_dict["susceptible"],

            hospitalized=RateLos(
                inputs_dict["hospitalized_rate"] / 100, inputs_dict["hospitalized_los"]
            ),
            icu=RateLos(inputs_dict["icu_rate"] / 100, inputs_dict["icu_los"]),
            ventilated=RateLos(
                inputs_dict["ventilated_rate"] / 100, inputs_dict["ventilated_los"]
            ),
            as_date=inputs_dict["as_date"],
            market_share=inputs_dict["market_share"] / 100,
            max_y_axis=inputs_dict["max_y_axis_value"],
            n_days=inputs_dict["n_days"],
        )
        return [parameters_serializer(pars)]

    def __init__(self, language, defaults):
        input_change_callback = ChimeCallback(
            changed_elements=OrderedDict((key, "value") for key in Sidebar.get_ordered_input_keys()),
            dom_updates=OrderedDict(pars="children"),
            callback_fn=Sidebar.update_parameters,
        )
        super().__init__(language, defaults, [input_change_callback])

    def get_html(self) -> List[ComponentMeta]:
        """Initializes the view
        """
        elements = [
            dhc.Div(id='pars', style={'display': 'none'})
        ]
        for idx, data in _INPUTS.items():
            if data["type"] == "number":
                element = create_number_input(idx, data, self.content, self.defaults)
            elif data["type"] == "switch":
                element = create_switch_input(idx, data, self.content)
            elif data["type"] == "header":
                element = create_header(idx, self.content)
            else:
                raise ValueError(
                    "Failed to parse input '{idx}' with data '{data}'".format(
                        idx=idx, data=data
                    )
                )
            elements.append(element)

        sidebar = dhc.Nav(
            children=dhc.Div(
                children=elements,
                className="p-4",
                style={
                    "height": "calc(100vh - 48px)",
                    "overflowY": "auto",
                },
            ),
            className="col-md-3",
            style={
                "position": "fixed",
                "top": "48px",
                "bottom": 0,
                "left": 0,
                "zIndex": 100,
                "boxShadow": "inset -1px 0 0 rgba(0, 0, 0, .1)"
            }
        )

        return [sidebar]
