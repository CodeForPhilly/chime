from typing import List

from dash.development.base_component import ComponentMeta
from dash_core_components import Markdown

from chime_dash.app.utils.templates import read_localization_markdown

LOCALIZATION_FILE_1 = "chime-intro.md"
LOCALIZATION_FILE_2 = "latest-updates.md"


def introducing_chime(language: str) -> List[ComponentMeta]:
    """Initializes the header dash html
    """
    content = read_localization_markdown(LOCALIZATION_FILE_1, language)

    return [Markdown(content)]


def latest_updates(language: str) -> List[ComponentMeta]:
    """Initializes the header dash html
    """
    content = read_localization_markdown(LOCALIZATION_FILE_2, language)

    return [Markdown(content)]
