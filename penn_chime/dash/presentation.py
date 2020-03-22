"""Functions which help rendering components of the app
"""
from typing import Tuple, List
from penn_chime.defaults import Constants

from penn_chime.dash.utils import render_yml
from penn_chime.dash.utils import get_yml_templates

YML_TEMPLATES = get_yml_templates()


def display_sidebar(
    language, defaults: Constants
) -> Tuple[List["DashHtml"], List[str]]:
    """Renders `sidebar.yml` and sets default values extracted from the defaults.

    Returns Dash HTML elements and ids for html forms (needed for callbacks)
    """
    yaml = YML_TEMPLATES[language]["sidebar.yml"].copy()

    parameter_keys = []

    # Find id's for forms
    for el in yaml:
        for child in el["children"]:
            if child["element"] == "input":
                # Append id to list of form ids
                idx = child["id"]
                parameter_keys.append(idx)

                # Set default value if possible
                if "rate" in idx:
                    base, _ = idx.split("_")
                    val = getattr(getattr(defaults, base, {}), "rate", 0) * 100
                elif "los" in idx:
                    base, _ = idx.split("_")
                    val = getattr(getattr(defaults, base, {}), "rate", 0) * 100
                else:
                    val = getattr(defaults, idx, 0)

                child["value"] = val

    dash_html = render_yml(yaml)

    return dash_html, parameter_keys
