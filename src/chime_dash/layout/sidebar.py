"""Initializes the  dash html
"""
from typing import List, Dict, Any, Optional

from dash.development.base_component import ComponentMeta
from dash_bootstrap_components import FormGroup, Label, Input, Checklist

from penn_chime.defaults import Constants

from chime_dash.utils import read_localization_yaml

LOCALIZATION_FILE = "sidebar.yml"

INPUTS = {
    "current_hospitalized": {"type": "number", "min": 0, "step": 1},
    "doubling_time": {"type": "number", "min": 0, "step": 1},
    "relative_contact_rate": {
        "type": "number",
        "min": 0,
        "step": 1,
        "max": 100,
        "percent": True,
    },
    "hospitalized_rate": {
        "type": "number",
        "min": 0,
        "step": 1,
        "max": 100,
        "percent": True,
    },
    "icu_rate": {"type": "number", "min": 0, "step": 1, "max": 100, "percent": True},
    "ventilated_rate": {
        "type": "number",
        "min": 0,
        "step": 1,
        "max": 100,
        "percent": True,
    },
    "hospitalized_los": {"type": "number", "min": 0, "step": 1, "max": 100},
    "icu_los": {"type": "number", "min": 0, "step": 1},
    "ventilated_los": {"type": "number", "min": 0, "step": 1},
    "market_share": {
        "type": "number",
        "min": 1,
        "step": 1,
        "max": 100,
        "percent": True,
    },
    "susceptible": {"type": "number", "min": 1, "step": 1},
    "known_infected": {"type": "number", "min": 0, "step": 1},
    "n_days": {"type": "number", "min": 20, "step": 1},
    "as_date": {"type": "switch", "value": False},
    "max_y_axis": {"type": "switch", "value": False},
}


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
        val = getattr(getattr(defaults, split[0], {}), "rate", min_val) * 100
    elif "share" in key:
        val = getattr(defaults, key, min_val) * 100
    elif "susceptible" in key:
        val = defaults.region.susceptible
    else:
        val = getattr(defaults, key, min_val)

    return min(max_val, val) if max_val is not None else val
