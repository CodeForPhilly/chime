"""components/sidebar
Initializes the side bar containing the various inputs for the model

#! _INPUTS should be considered for moving else where
"""
from typing import List

from collections import OrderedDict
from datetime import date, datetime

from dash.dependencies import Input as CallbackInput
from dash.development.base_component import ComponentMeta
from dash_html_components import Nav, Div

from penn_chime.parameters import Parameters, Disposition

from chime_dash.app.components.base import Component
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
    show_additional_projections={"type": "switch", "value": False},
)

# Different kind of inputs store different kind of "values"
## This tells the callback output for which field to look
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

    callback_inputs = OrderedDict(
        (
            key,
            CallbackInput(
                component_id=key,
                component_property=_PROPERTY_OUTPUT_MAP.get(
                    _INPUTS[key]["type"], "value"
                ),
            ),
        )
        for key in _INPUTS
        if _INPUTS[key]["type"] not in ("header",)
    )

    @staticmethod
    def parse_form_parameters(**kwargs) -> Parameters:
        """Reads html form outputs and converts them to a parameter instance

        Returns Parameters
        """
        for key in ["date_first_hospitalized", "current_date"]:
            val = kwargs.get(key, None)
            kwargs[key] = datetime.strptime(val, "%Y-%m-%d").date() if val else val

        dt = kwargs["doubling_time"] if kwargs["doubling_time"] else None
        dfh = kwargs["date_first_hospitalized"] if not dt else None

        pars = Parameters(
            population=kwargs["population"],
            current_hospitalized=kwargs["current_hospitalized"],
            date_first_hospitalized=dfh,
            doubling_time=dt,
            hospitalized=Disposition(
                kwargs["hospitalized_rate"] / 100, kwargs["hospitalized_los"]
            ),
            icu=Disposition(kwargs["icu_rate"] / 100, kwargs["icu_los"]),
            infectious_days=kwargs["infectious_days"],
            market_share=kwargs["market_share"] / 100,
            n_days=kwargs["n_days"],
            relative_contact_rate=kwargs["relative_contact_rate"] / 100,
            ventilated=Disposition(
                kwargs["ventilated_rate"] / 100, kwargs["ventilated_los"]
            ),
        )
        return pars

    def get_html(self) -> List[ComponentMeta]:
        """Initializes the view
        """
        elements = []
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
            children=Div(
                children=elements,
                className="p-4",
                style={"height": "calc(100vh - 48px)", "overflowY": "auto",},
            ),
            className="col-md-3",
            style={
                "position": "fixed",
                "top": "48px",
                "bottom": 0,
                "left": 0,
                "zIndex": 100,
                "boxShadow": "inset -1px 0 0 rgba(0, 0, 0, .1)",
            },
        )

        return [sidebar]
