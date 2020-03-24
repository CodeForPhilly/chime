"""Initializes the  dash html
"""
from typing import List, Dict, Any, Optional, Tuple
from collections import OrderedDict

from dash.dependencies import Input as CallbackInput
from dash.development.base_component import ComponentMeta
from dash_bootstrap_components import FormGroup, Label, Input, Checklist

from penn_chime.defaults import RateLos, Constants
from penn_chime.parameters import Parameters

from chime_dash.utils import read_localization_yaml

LOCALIZATION_FILE = "sidebar.yml"

INPUTS = OrderedDict(
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

CALLBACK_INPUTS = [
    CallbackInput(component_id=key, component_property="value") for key in INPUTS
]


def parse_form_parameters(*args) -> Tuple[Parameters, Dict[str, Any]]:
    """Reads html form outputs and converts them to a parameter instance

    Returns Parameters and as_date argument
    """
    kwargs = {
        key: val / 100 if ("rate" in key or "share" in key) else val
        for key, val in zip(INPUTS.keys(), args)
    }
    max_y_axis_value = kwargs["max_y_axis_value"]
    pars = Parameters(
        current_hospitalized=kwargs["current_hospitalized"],
        doubling_time=kwargs["doubling_time"],
        known_infected=kwargs["known_infected"],
        market_share=kwargs["market_share"],
        relative_contact_rate=kwargs["relative_contact_rate"],
        susceptible=kwargs["susceptible"],
        hospitalized=RateLos(kwargs["hospitalized_rate"], kwargs["hospitalized_los"]),
        icu=RateLos(kwargs["icu_rate"], kwargs["icu_los"]),
        ventilated=RateLos(kwargs["ventilated_rate"], kwargs["ventilated_los"]),
        max_y_axis=max_y_axis_value,
        n_days=kwargs["n_days"],
    )
    return pars, kwargs


def setup(language: str, defaults: Constants) -> List[ComponentMeta]:
    """Initializes the header dash html
    """
    content = read_localization_yaml(LOCALIZATION_FILE, language)

    elements = []

    for idx, data in INPUTS.items():
        if data["type"] == "number":
            element = _create_number_input(idx, data, content, defaults)
        elif data["type"] == "switch":
            element = _create_switch_input(idx, data, content)
        else:
            raise ValueError(
                "Failed to parse input '{idx}' with data '{data}'".format(
                    idx=idx, data=data
                )
            )

        elements.append(element)

    return elements


def _create_number_input(
    idx: str, data: Dict[str, Any], content: Dict[str, str], defaults: Constants
):
    """Returns number formgroup for given form data.

    Arguments:
        idx: The name of the varibale (html id)
        data: Input form kwargs.
        content: Localization text
        defaults: Constants to infer defaults
    """
    input_kwargs = data.copy()
    input_kwargs.pop("percent", None)
    if not "value" in input_kwargs:
        input_kwargs["value"] = _get_default(
            idx, defaults, min_val=data.get("min", None), max_val=data.get("max", None)
        )
    return FormGroup(
        children=[
            Label(html_for=idx, children=content[idx]),
            Input(id=idx, **input_kwargs),
        ]
    )


def _create_switch_input(idx: str, data: Dict[str, Any], content: Dict[str, str]):
    """Returns switch for given form data.

    Arguments:
        idx: The name of the varibale (html id)
        data: Input form kwargs.
        content: Localization text
        defaults: Constants to infer defaults
    """
    return Checklist(
        id=idx,
        switch=True,
        options=[{"label": content[idx], "value": data.get("value", False)}],
    )


def _get_default(
    key: str,
    defaults: Constants,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None,
) -> float:
    """Tries to infer default values given parameters.

    Ensures that value is between min and max.
    Min defaults to zero if not given. Max will be ignored if not given.

    Arguments:
        key: The name of the varibale (html id)
        defaults: Constants to infer defaults
        min_val: Min boundary of form
        max_val: Max boundary of form
    """
    min_val = 0 if min_val is None else min_val

    if "rate" in key:
        split = key.split("_")
        val = getattr(getattr(defaults, split[0], {}), "rate", min_val) * 100
    elif "los" in key:
        split = key.split("_")
        val = getattr(getattr(defaults, split[0], {}), "length_of_stay", min_val)
    elif "share" in key:
        val = getattr(defaults, key, min_val) * 100
    elif "susceptible" in key:
        val = defaults.region.susceptible
    else:
        val = getattr(defaults, key, min_val)

    return min(max_val, val) if max_val is not None else val
