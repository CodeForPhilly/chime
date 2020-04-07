"""utils/templates
Utility functions for localization templates
templates themselves can be found in app/templates/en
"""
from typing import Dict, Any, Optional

from os import path

from yaml import safe_load

from numpy import mod
from pandas import DataFrame

from dash_html_components import Table, Thead, Tbody, Tr, Td, Th, H4
from dash_core_components import DatePickerSingle
from dash_bootstrap_components import FormGroup, Label, Input, Checklist

from penn_chime.parameters import Parameters

# Consider moving this to a config file eventually
TEMPLATE_DIR = path.join(
    path.abspath(path.dirname(path.dirname(__file__))), "templates"
)

LABEL_STYLE = {"fontSize": "0.875rem", "marginBottom": "0.3333em"}

HEADER_STYLE = {
    "fontSize": "1rem",
    "fontWeight": "bold",
    "margin": "2rem 0 1rem",
}


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
    dataframe: DataFrame,
    data_only: bool = False,
    n_mod: Optional[int] = None,
    formats: Optional[Dict[Any, str]] = None,
) -> Table:
    """Converts pandas data frame to html table
    """
    formats = formats or {}

    def cast_type(val):
        for dtype, cast in formats.items():
            if isinstance(val, dtype):
                try:
                    val = cast(val)
                    break
                except ValueError:
                    break
        return val

    index_name = dataframe.index.name
    index_name = index_name or "#"

    tmp = dataframe.copy()
    if n_mod is not None:
        tmp = tmp[mod(tmp.index, n_mod) == 0].copy()

    data = [
        Thead([Tr([Th(index_name)] + [Th(col) for col in tmp.columns])]),
        Tbody(
            [
                Tr([Th(cast_type(idx))] + [Td(cast_type(col)) for col in row])
                for idx, row in tmp.iterrows()
            ]
        ),
    ]
    return data if data_only else Table(data)


def create_number_input(
    idx: str,
    data: Dict[str, Any],
    content: Dict[str, str],
    defaults: Parameters,
    debounce: bool = True,
):
    """Returns number formgroup for given form data.

    Arguments:
        idx: The name of the varibale (html id)
        data: Input form kwargs.
        content: Localization text
        defaults: Parameters to infer defaults
        debounce: Trigger callback on enter or unfocus
    """
    input_kwargs = data.copy()
    input_kwargs.pop("percent", None)

    if not "value" in input_kwargs:
        input_kwargs["value"] = _get_default_values(
            idx, defaults, min_val=data.get("min", None), max_val=data.get("max", None)
        )
    return FormGroup(
        children=[
            Label(html_for=idx, children=content[idx], style=LABEL_STYLE),
            Input(id=idx, debounce=debounce, **input_kwargs),
        ]
    )


def create_header(idx: str, content: Dict[str, str]):
    """
    Create heading element using localization map
    """

    return H4(id=idx, children=content[idx], style=HEADER_STYLE)


def create_date_input(
    idx: str, data: Dict[str, Any], content: Dict[str, str], defaults: Parameters
):
    """Returns number formgroup for given form data.

    Arguments:
        idx: The name of the varibale (html id)
        data: Input form kwargs.
        content: Localization text
        defaults: Parameters to infer defaults
    """
    input_kwargs = data.copy()
    input_kwargs.pop("type")

    if not "date" in input_kwargs:
        input_kwargs["date"] = input_kwargs[
            "initial_visible_month"
        ] = _get_default_values(idx, defaults)

    return FormGroup(
        children=[
            Label(html_for=idx, children=content[idx], style=LABEL_STYLE),
            DatePickerSingle(
                className="form-control",
                day_size=32,
                display_format='YYYY-MM-DD',
                id=idx,
                **input_kwargs
            ),
        ]
    )


def create_switch_input(idx: str, data: Dict[str, Any], content: Dict[str, str]):
    """Returns switch for given form data.

    Arguments:
        idx: The name of the varibale (html id)
        data: Input form kwargs.
        content: Localization text
        defaults: Parameters to infer defaults
    """
    return Checklist(
        id=idx, switch=True, options=[{"label": content[idx], "value": True}],
    )


def _get_default_values(
    key: str,
    defaults: Parameters,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None,
) -> float:
    """Tries to infer default values given parameters.

    Ensures that value is between min and max.
    Min defaults to zero if not given. Max will be ignored if not given.

    Arguments:
        key: The name of the varibale (html id)
        defaults: Parameters to infer defaults
        min_val: Min boundary of form
        max_val: Max boundary of form
    """
    min_val = 0 if min_val is None else min_val

    if "rate" in key:
        val = (
            defaults.dispositions[key.split("_")[0]].rate
            if key.split("_")[0] in defaults.dispositions
            else getattr(defaults, key, min_val)
        ) * 100
    elif "los" in key:
        val = (
            defaults.dispositions[key.split("_")[0]].days
            if key.split("_")[0] in defaults.dispositions
            else getattr(defaults, key, min_val)
        )
    elif "share" in key:
        val = getattr(defaults, key, min_val) * 100
    elif "susceptible" in key:
        val = defaults.region.susceptible
    else:
        val = getattr(defaults, key, min_val)

    return min(max_val, val) if max_val is not None else val
