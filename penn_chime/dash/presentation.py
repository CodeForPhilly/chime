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
    """Renders `sidebar-bare.yml` and sets default values extracted from the defaults.

    Returns Dash HTML elements and ids for html forms (needed for callbacks)
    """
    yaml = []
    parameter_keys = []

    # Find id's for forms
    for el in YML_TEMPLATES[language]["sidebar-bare.yml"]:
        children = []

        caption = el.pop("caption", None)
        if caption is not None:
            children.append(
                {"element": "label", "html_for": el["id"], "children": caption}
            )

        form = el.copy()
        form["element"] = "input"

        # Get default values
        idx = form["id"]
        if "rate" in idx:
            split = idx.split("_")
            val = getattr(getattr(defaults, split[0], {}), "rate", 0) * 100
        elif "los" in idx:
            split = idx.split("_")
            val = getattr(getattr(defaults, split[0], {}), "rate", 0) * 100
        else:
            val = getattr(defaults, idx, 0)
        form["value"] = val

        children.append(form)
        yaml.append({"element": "formgroup", "children": children})
        parameter_keys.append(idx)

    dash_html = render_yml(yaml)

    return dash_html, parameter_keys
