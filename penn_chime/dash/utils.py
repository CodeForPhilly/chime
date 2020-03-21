"""Utility functions for dash frontend
"""
from typing import Dict

from os import path, listdir

from pandas import DataFrame
from dash_html_components import Table, Thead, Tbody, Tr, Td, Th

TEMPLATE_DIR = path.join(path.abspath(path.dirname(__file__)), "templates")


def df_to_html_table(df: DataFrame) -> Table:
    """Converts pandas data frame to html table
    """
    return Table(
        [
            Thead([Tr([Th("id")] + [Th(col) for col in df.columns])]),
            Tbody(
                [Tr([Th(idx)] + [Td(col) for col in row]) for idx, row in df.iterrows()]
            ),
        ],
    )


def get_md_templates() -> Dict[str, str]:
    """Reads all the templates located in the template dir

    File names are keys, values are the file content.
    """
    files = [f for f in listdir(TEMPLATE_DIR) if f.endswith("md")]
    templates = dict()
    for ff in files:
        with open(path.join(TEMPLATE_DIR, ff), "r") as inp:
            templates[ff] = inp.read()

    return templates
