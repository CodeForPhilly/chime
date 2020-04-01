"""components/sidebar
Initializes the side bar containing the various inputs for the model

#! _INPUTS should be considered for moving else where
"""
from dash_html_components import Nav, Div

from typing import List, Dict, Any, Tuple
from collections import OrderedDict
from datetime import date, datetime

from dash.development.base_component import ComponentMeta
from dash_html_components import Nav, Div, Hr

from penn_chime.parameters import Parameters, Disposition

from chime_dash.app.components.base import Component
from chime_dash.app.utils import parameters_serializer
from chime_dash.app.utils.callbacks import ChimeCallback
from chime_dash.app.utils.templates import (
    create_switch_input,
    create_number_input,
    create_date_input,
    create_header,
)

FLOAT_INPUT_MIN = 0.001
FLOAT_INPUT_STEP = "any"

_INPUTS = OrderedDict(
    ###
    hospital_parameters={"type": "header", "size": "h3"},
    population={"type": "number", "min": 1, "step": 1},
    market_share={
        "type": "number",
        "min": FLOAT_INPUT_MIN,
        "step": FLOAT_INPUT_STEP,
        "max": 100.0,
        "percent": True,
    },
    current_hospitalized={"type": "number", "min": 0, "step": 1},
    ###
    spread_parameters={"type": "header", "size": "h4"},
    date_first_hospitalized={
        "type": "date",
        "min_date_allowed": datetime(2019, 10, 1),
        "max_date_allowed": datetime(2021, 12, 31),
    },
    doubling_time={"type": "number", "min": FLOAT_INPUT_MIN, "step": FLOAT_INPUT_STEP},
    relative_contact_rate={
        "type": "number",
        "min": 0.0,
        "step": FLOAT_INPUT_STEP,
        "max": 100.0,
        "percent": True,
    },
    ###
    severity_parameters={"type": "header", "size": "h4"},
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
        "percent": True,
    },
    ventilated_rate={
        "type": "number",
        "min": 0.0,
        "step": FLOAT_INPUT_STEP,
        "max": 100.0,
        "percent": True,
    },
    infectious_days={"type": "number", "min": 0, "step": 1},
    hospitalized_los={"type": "number", "min": 0, "step": 1},
    icu_los={"type": "number", "min": 0, "step": 1},
    ventilated_los={"type": "number", "min": 0, "step": 1},
    ###
    display_parameters={"type": "header", "size": "h4"},
    n_days={"type": "number", "min": 30, "step": 1},
    current_date={
        "type": "date",
        "min_date_allowed": datetime(2019, 10, 1),
        "max_date_allowed": datetime(2021, 12, 31),
        "initial_visible_month": date.today(),
        "date": date.today(),
    },
    max_y_axis_value={"type": "number", "min": 10, "step": 10, "value": None},
    show_tables={"type": "switch", "value": False},
    show_tool_details={"type": "switch", "value": False},
)

# Different kind of inputs store different kind of "values"
# This tells the callback output for which field to look
_PROPERTY_OUTPUT_MAP = {
    "number": "value",
    "date": "date",
}


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
    def get_formated_values(input_values):
        result = dict(zip(Sidebar.get_ordered_input_keys(), input_values))
        # todo remove this hack needed because of how Checklist type used for switch input returns values
        for key in _INPUTS:
            if _INPUTS[key]["type"] == "switch":
                value = False
                if result[key] == [True]:
                    value = True
                result[key] = value
            elif _INPUTS[key]["type"] == "date":
                value = result[key]
                result[key] = datetime.strptime(value, "%Y-%m-%d").date() if value else value
        return result

    @staticmethod
    def update_parameters(*input_values, **kwargs) -> List[str]:
        """Reads html form outputs and converts them to a parameter instance

        Returns Parameters
        """
        inputs_dict = Sidebar.get_formated_values(input_values)
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

    def __init__(self, language, defaults):
        changed_elements = OrderedDict(
            (key, _PROPERTY_OUTPUT_MAP.get(_INPUTS[key]["type"], "value"))
            for key in _INPUTS
            if _INPUTS[key]["type"] not in ("header",)
        )

        input_change_callback = ChimeCallback(
            changed_elements=changed_elements,
            dom_updates=OrderedDict(pars="children"),
            callback_fn=Sidebar.update_parameters,
        )
        super().__init__(language, defaults, [input_change_callback])

    def get_html(self) -> List[ComponentMeta]:
        """Initializes the view
        """
        elements = [
            Div(id='pars', style={'display': 'none'})
        ]
        for idx, data in _INPUTS.items():
            if data["type"] == "number":
                element = create_number_input(idx, data, self.content, self.defaults)
            elif data["type"] == "switch":
                element = create_switch_input(idx, data, self.content)
            elif data["type"] == "date":
                element = create_date_input(idx, data, self.content, self.defaults)
            elif data["type"] == "header":
                element = create_header(idx, self.content)
            else:
                raise ValueError(
                    "Failed to parse input '{idx}' with data '{data}'".format(
                        idx=idx, data=data
                    )
                )
            elements.append(element)

        sidebar = Nav(
            className="bg-light border-right",
            children=Div(
                children=elements,
                className="px-3 pb-5",
            ),
            style={
                "bottom": 0,
                "left": 0,
                "overflowY": "scroll",
                "position": "fixed",
                "top": "56px",
                "width": "320px",
                "zIndex": 1,
            },
        )

        return [sidebar]

