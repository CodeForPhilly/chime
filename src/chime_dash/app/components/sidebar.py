"""Initializes the  dash html
"""
from typing import List, Dict, Any, Tuple
from collections import OrderedDict

from dash.dependencies import Input as CallbackInput
from dash.development.base_component import ComponentMeta

from penn_chime.defaults import RateLos
from penn_chime.parameters import Parameters

from chime_dash.app.components.base import Component
from chime_dash.app.utils.templates import create_switch_input, create_number_input


_INPUTS = OrderedDict(
    current_hospitalized={"type": "number", "min": 0, "step": 1},
    doubling_time={"type": "number", "min": 0, "step": 1},
    relative_contact_rate={
        "type": "number",
        "min": 0,
        "step": 1,
        "max": 100,
        "percent": True,
    },
    hospitalized_rate={
        "type": "number",
        "min": 0,
        "step": 1,
        "max": 100,
        "percent": True,
    },
    icu_rate={"type": "number", "min": 0, "step": 1, "max": 100, "percent": True},
    ventilated_rate={
        "type": "number",
        "min": 0,
        "step": 1,
        "max": 100,
        "percent": True,
    },
    hospitalized_los={"type": "number", "min": 0, "step": 1, "max": 100},
    icu_los={"type": "number", "min": 0, "step": 1},
    ventilated_los={"type": "number", "min": 0, "step": 1},
    market_share={"type": "number", "min": 1, "step": 1, "max": 100, "percent": True,},
    susceptible={"type": "number", "min": 1, "step": 1},
    known_infected={"type": "number", "min": 0, "step": 1},
    n_days={"type": "number", "min": 20, "step": 1},
    as_date={"type": "switch", "value": False},
    max_y_axis_value={"type": "number", "min": 10, "step": 10, "value": None},
    show_tables={"type": "switch", "value": False},
    show_tool_details={"type": "switch", "value": False},
    show_additional_projections={"type": "switch", "value": False},
)


class Sidebar(Component):
    """
    """

    localization_file = "sidebar.yml"

    callback_inputs = OrderedDict(
        (key, CallbackInput(component_id=key, component_property="value"))
        for key in _INPUTS
    )

    @staticmethod
    def parse_form_parameters(**kwargs) -> Tuple[Parameters, Dict[str, Any]]:
        """Reads html form outputs and converts them to a parameter instance

        Returns Parameters and as_date argument
        """
        pars = Parameters(
            current_hospitalized=kwargs["current_hospitalized"],
            doubling_time=kwargs["doubling_time"],
            known_infected=kwargs["known_infected"],
            market_share=kwargs["market_share"] / 100,
            relative_contact_rate=kwargs["relative_contact_rate"] / 100,
            susceptible=kwargs["susceptible"],
            hospitalized=RateLos(
                kwargs["hospitalized_rate"] / 100, kwargs["hospitalized_los"]
            ),
            icu=RateLos(kwargs["icu_rate"] / 100, kwargs["icu_los"]),
            ventilated=RateLos(
                kwargs["ventilated_rate"] / 100, kwargs["ventilated_los"]
            ),
            max_y_axis=kwargs["max_y_axis_value"],
            n_days=kwargs["n_days"],
        )
        return pars

    def get_html(self) -> List[ComponentMeta]:
        """Initializes the header dash html
        """
        elements = []
        for idx, data in _INPUTS.items():
            if data["type"] == "number":
                element = create_number_input(idx, data, self.content, self.defaults)
            elif data["type"] == "switch":
                element = create_switch_input(idx, data, self.content)
            else:
                raise ValueError(
                    "Failed to parse input '{idx}' with data '{data}'".format(
                        idx=idx, data=data
                    )
                )
            elements.append(element)

        return elements
