"""Utility functions for dash frontend
"""
from typing import Dict, Any, Optional

from os import path

from yaml import safe_load

from numpy import mod
from pandas import DataFrame

from dash_html_components import Table, Thead, Tbody, Tr, Td, Th

TEMPLATE_DIR = path.join(
    path.abspath(path.dirname(path.dirname(__file__))), "templates"
)


def read_localization_yaml(file: str, language: str) -> Dict[str, Any]:
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
