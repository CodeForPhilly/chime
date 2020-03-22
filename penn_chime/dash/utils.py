"""Utility functions for dash frontend
"""
from typing import Dict, List, Any

from os import path, listdir, walk, sep

from yaml import safe_load

from pandas import DataFrame

from dash_html_components import Table, Thead, Tbody, Tr, Td, Th
from dash_html_components import H1, Div, A

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


def get_md_templates() -> Dict[str, Dict[str, str]]:
    """Reads all the templates located in the template dir (markdown)

    File names are keys, values are the file content.
    """
    templates = dict()
    for root, dirs, files in walk(TEMPLATE_DIR):
        for f in files:
            if f.endswith("md"):
                with open(path.join(root, f), "r") as inp:
                    templates.setdefault(root.split(sep)[-1], dict())[f] = inp.read()

    return templates


def get_yml_templates() -> Dict[str, Dict[str, str]]:
    """Finds all the templates located in the template dir (yaml)

    File names are keys, values are the file address.
    """
    templates = dict()
    for root, dirs, files in walk(TEMPLATE_DIR):
        for f in files:
            if f.endswith("yml"):
                templates.setdefault(root.split(sep)[-1], dict())[f] = path.join(
                    root, f
                )

    return templates


DASH_HTML_ELEMENTS = {"div": Div, "h1": H1, "a": A}


def render_yml(file: str) -> List["HtmlObjtects"]:
    """Reads yaml file and converts to dash html objects
    """
    with open(file, "r") as stream:
        yaml_list = safe_load(stream)

    return [_render_yml(yaml) for yaml in yaml_list]


def _render_yml(yaml: Dict[str, str]) -> "HtmlObjtects":
    """Reads recursively reads dictionary and renders Dash HTML compenents
    """
    tmp = dict(**yaml)
    el = DASH_HTML_ELEMENTS[tmp.pop("element")]

    kwargs = dict()
    for key, val in tmp.items():
        # Recursively cast children if possible
        if key == "children" and isinstance(val, List):
            children = []
            for child in val:
                children.append(_render_yml(child))
            val = children
        elif key == "class":
            key = "className"
        # Store element creation args
        kwargs[key] = val

    return el(**kwargs)
