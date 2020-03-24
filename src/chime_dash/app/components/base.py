"""Module provides abstract base component needed for rendering
"""
from typing import List, Dict, Any, Union

from abc import ABC

from dash.dependencies import Output, Input
from dash.development.base_component import ComponentMeta
from dash_html_components import Div

from penn_chime.defaults import Constants
from penn_chime.settings import DEFAULTS

from chime_dash.app.utils.templates import read_localization_yml
from chime_dash.app.utils.templates import read_localization_markdown


class Component(ABC):
    """
    """

    callback_outputs: List[Output] = []  # must be same length as callback return
    callback_inputs: Dict[str, Input] = {}
    callback_keys: List[str] = []

    localization_file: str = None

    external_stylesheets: List[str] = []
    external_scripts: List[str] = []

    def __init__(self, language: str = "en", defaults: Constants = DEFAULTS):
        """
        """
        self.language = language
        self.defaults = defaults
        self._content = None

    def callback(self, *args, **kwargs) -> List[Dict[str, Any]]:
        """
        """
        return []

    def get_html(self) -> List[ComponentMeta]:
        """
        """
        return Div("")

    @property
    def html(self) -> List[ComponentMeta]:
        """
        """
        return self.get_html()

    @property
    def content(self) -> Union[str, Dict[str, str]]:
        """
        """
        if not self._content:
            if self.localization_file.endswith(".yml"):
                self._content = read_localization_yml(
                    self.localization_file, self.language
                )
            elif self.localization_file.endswith(".md"):
                self._content = read_localization_markdown(
                    self.localization_file, self.language
                )
            else:
                raise KeyError(
                    "Unknown content file extension 'file'".format(
                        file=self.localization_file
                    )
                )
        return self._content
