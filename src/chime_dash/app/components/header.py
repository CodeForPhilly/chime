"""Initializes the header dash html
"""
from typing import List

from dash.development.base_component import ComponentMeta
from dash_html_components import Div, A

from chime_dash.app.utils import read_localization_yaml

LOCALIZATION_FILE = "header.yml"


def setup(language: str) -> List[ComponentMeta]:
    """Initializes the header dash html
    """
    content = read_localization_yaml(LOCALIZATION_FILE, language)

    return [
        Div(
            className="penn-medicine-header__content",
            children=[
                A(
                    href="https://www.pennmedicine.org",
                    className="penn-medicine-header__logo",
                    title=content["logo-title"],
                    children=content["logo-text"],
                ),
                A(
                    className="penn-medicine-header__title",
                    id="title",
                    children=content["title"],
                ),
            ],
        )
    ]
