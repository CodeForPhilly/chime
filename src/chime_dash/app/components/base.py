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
    """Base component for rendering dash html objects and callbacks

    Attributes:
        localization_file: File name for rendering localized strings
        callback_outputs: List of callback outputs needed for rendering html.
            Must be used together with `callback()` which provides callback data.
        callback_inputs: Ordered dictionary for element id's and input types.
            Must be used if component contains widgets.
        external_stylesheets: External stylesheets. Just a storage container.
        external_scripts: External scripts. Just a storage container.
    """

    localization_file: str = None

    callback_outputs: List[Output] = []  # must be same length as callback return
    callback_inputs: Dict[str, Input] = {}  # Must be ordered!

    external_stylesheets: List[str] = []
    external_scripts: List[str] = []

    def __init__(self, language: str = "en", defaults: Constants = DEFAULTS):
        """Initializes the component
        """
        self.language = language
        self.defaults = defaults
        self._content = None
        self._html = None

    def callback(  # pylint: disable=W0613, R0201
        self, *args, **kwargs
    ) -> List[Dict[str, Any]]:
        """Function which is called whenever a web-input element is triggered.

        Overwrite this function for custom actions.
        To render arguments, add (or modify)
        ```
        @app.callback(component.callback_outputs, component.callback_inputs.values()):
        def callback_body(*args):
            return component.callback(*args)
        ```
        Args come from the specified forms in order as `callback_outputs`.

        Arguments:
            args: Form parameters specified in `callback_outputs` order
            kwargs: Additional arguments supplied by the user when modifying the
                decorated `callback_body`.

        Result should be the data (usually dictionaries) passed to the Dash element
        of given id. The number of arguments and order must match the elements in
        `callback_outputs`.

        See also https://dash.plotly.com/getting-started-part-2
        """
        return []

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
