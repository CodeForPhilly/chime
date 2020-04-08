"""app/components/base

Abstract base class for components

#! candidate for moving into utils/components
"""
from typing import List, Dict, Union

from abc import ABC

from dash.development.base_component import ComponentMeta
from dash_html_components import Div

from penn_chime.parameters import Parameters

from chime_dash.app.utils.templates import read_localization_yml, read_localization_markdown


class Component(ABC):
    """Base component for rendering dash html objects and registering callbacks

    Attributes:
        localization_file: File name for rendering localized strings
        external_stylesheets: External stylesheets. Just a storage container.
        external_scripts: External scripts. Just a storage container.
    """

    localization_file: str = None
    external_stylesheets: List[str] = []
    external_scripts: List[str] = []

    def __init__(self, language: str = "en", defaults: Parameters = None):
        """Initializes the component
        """
        self.language = language
        self.defaults = defaults
        self._content = None
        self._html = None

    def get_html(self) -> List[ComponentMeta]:  # pylint: disable=R0201
        """Function which is called to render html elements.

        Should return a list of Dash components. Must be overwritten.
        """
        return Div("")

    @property
    def html(self) -> List[ComponentMeta]:
        """Accessor for `get_html` wrapped with Exception handling:

        Raises:
            HTMLComponentError: if any error occurs.
        """
        if self._html is None:
            try:
                self._html = self.get_html()
            except Exception as error:
                raise HTMLComponentError(self, error)
        return self._html

    @property
    def content(self) -> Union[str, Dict[str, str], None]:
        """Reads localization files and returns text (for md) or dict (for yml) files.

        Infers template location from `localization_file` and `language` attributes.

        Raises:
            Key error if unknown
        """
        if self._content is None:
            if self.localization_file is None:
                self._content = {}
            else:
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


class Page(Component):
    callbacks_cls = None

    def __init__(self, language: str = "en", defaults: Parameters = None):
        super().__init__(language, defaults)
        self.callbacks_cls(self)


class HTMLComponentError(Exception):
    """Custom exception for errors when rendering component html.

    Original error is stored in `error` attribute.
    """

    def __init__(self, component: Component, error: Exception):
        """Initializes the error message
        """
        message = "{etype}->{error} while rendering HTML component {component}".format(
            etype=error.__class__.__name__, error=error, component=component
        )
        message += (
            "\n\nData:\n"
            + "\n -".join(
                [
                    "{key}: {value}".format(key=key, value=value)
                    for key, value in {
                        "language": component.language,
                        "localization_file": component.localization_file,
                        "content": component.content,
                        "defaults": component.defaults,
                    }.items()
                ]
            )
            + "\n"
        )
        super().__init__(message)
        self.component = component
        self.error = error
