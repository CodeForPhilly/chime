"""Initializes the  dash html
"""
from typing import List

from dash.development.base_component import ComponentMeta

from chime_dash.utils import read_localization_yaml

LOCALIZATION_FILE = ""


def setup(language: str) -> List[ComponentMeta]:
    """Initializes the header dash html
    """
    content = read_localization_yaml(LOCALIZATION_FILE, language)

    return
