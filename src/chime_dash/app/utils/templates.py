"""Utility functions for dash frontend
"""
from typing import Dict, Any, Optional

from os import path

from yaml import safe_load

from numpy import mod
from pandas import DataFrame

from dash_html_components import Table, Thead, Tbody, Tr, Td, Th
from dash_bootstrap_components import FormGroup, Label, Input, Checklist

from penn_chime.defaults import Constants


TEMPLATE_DIR = path.join(
    path.abspath(path.dirname(path.dirname(__file__))), "templates"
)


def read_localization_yml(file: str, language: str) -> Dict[str, Any]:
    """Reads localization template.

    Arguments:
        file: Name of the section plus `.yml`
        language: Localization info

    Raises:
        KeyError: If no template for file/language exists.
    """
    file_address = path.join(TEMPLATE_DIR, language, file)
    if not path.exists(file_address):
        raise KeyError(
            "No template found for language '{language}' and section '{file}'".format(
                file=file, language=language
            )
        )
    with open(file_address, "r") as stream:
        yaml = safe_load(stream)

    return yaml


def read_localization_markdown(file: str, language: str) -> str:
    """Reads localization template.

    Arguments:
        file: Name of the section plus `.md`
        language: Localization info

    Raises:
        KeyError: If no template for file/language exists.
    """
    file_address = path.join(TEMPLATE_DIR, language, file)
    if not path.exists(file_address):
        raise KeyError(
            "No template found for langage '{language}' and section '{file}'".format(
                file=file, language=language
            )
        )
    with open(file_address, "r") as stream:
        md = stream.read()

    return md


def df_to_html_table(
    dataframe: DataFrame, data_only: bool = False, n_mod: Optional[int] = None,
) -> Table:
    """Converts pandas data frame to html table
    """
    index_name = dataframe.index.name
    tmp = dataframe.reset_index()
    tmp = tmp[mod(tmp.index, n_mod) == 0].copy()
    tmp = tmp.set_index(index_name)
    data = [
        Thead([Tr([Th(tmp.index.name)] + [Th(col) for col in tmp.columns])]),
        Tbody(
            [Tr([Th(idx)] + [Td(col) for col in row]) for idx, row in tmp.iterrows()]
        ),
    ]
    return data if data_only else Table(data)


def create_number_input(
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
        input_kwargs["value"] = _get_default_values(
            idx, defaults, min_val=data.get("min", None), max_val=data.get("max", None)
        )
    return FormGroup(
        children=[
            Label(html_for=idx, children=content[idx]),
            Input(id=idx, **input_kwargs),
        ]
    )


def create_switch_input(idx: str, data: Dict[str, Any], content: Dict[str, str]):
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


def _get_default_values(
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
