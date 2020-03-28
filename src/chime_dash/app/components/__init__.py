"""Combines all components

The `sidebar` component combines all the inputs while other components potentially
have callbacks.

To add or remove components, adjust the `setup`.
If callbacks are present, also adjust `CALLBACK_INPUTS`, `CALLBACK_OUTPUTS` and
`callback_body`.
"""
from collections import OrderedDict

import dash_html_components as dhc
from chime_dash.app.components.base import Component, HTMLComponentError
from dash_bootstrap_components.themes import BOOTSTRAP
from chime_dash.app.components.navbar import Navbar
from chime_dash.app.components.container import Container


class Body(Component):
    """
    """

    external_stylesheets = [
        "https://www1.pennmedicine.org/styles/shared/penn-medicine-header.css",
        BOOTSTRAP,
    ]

    def __init__(self, language, defaults):
        """
        """
        super().__init__(language, defaults)
        self.components = OrderedDict(
            navbar=Navbar(language, defaults),
            container=Container(language, defaults),
        )
        self.callback_outputs = []
        self.callback_inputs = OrderedDict()
        for component in self.components.values():
            self.callback_outputs += component.callback_outputs
            self.callback_inputs.update(component.callback_inputs)

    def get_html(self):
        """Glues individual setup components together
        """
        return dhc.Div(self.components["navbar"].html + self.components["container"].html)

    def callback(self, *args, **kwargs):
        """
        """
        kwargs = dict(zip(self.callback_inputs, args))

        callback_returns = []
        for component in self.components.values():
            try:
                callback_returns += component.callback(**kwargs)
            except Exception as error:
                raise HTMLComponentError(component, error)

        return callback_returns
