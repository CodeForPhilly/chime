"""Initializes the dash html for content container
"""
from collections import OrderedDict

from dash_html_components import Div
from chime_dash.app.components.base import Component, HTMLComponentError
from chime_dash.app.components.content import Content
from chime_dash.app.components.sidebar import Sidebar
from penn_chime.models import SimSirModel


class Container(Component):
    """Container contains sidebar and content components
    """

    def __init__(self, language, defaults):
        """
        """
        super().__init__(language, defaults)
        self.components = OrderedDict(
            sidebar=Sidebar(language, defaults), content=Content(language, defaults),
        )
        self.callback_outputs = []
        self.callback_inputs = OrderedDict()
        for component in self.components.values():
            self.callback_outputs += component.callback_outputs
            self.callback_inputs.update(component.callback_inputs)

    def get_html(self):
        """Initializes the content container dash html
        """
        container = Div(
            className="app-content",
            children=
                self.components["sidebar"].html
                + self.components["content"].html
        )

        return [container]

    def callback(self, *args, **kwargs):
        """Parse sidebar parameters to model and call sub component callbacks
        """
        pars = self.components["sidebar"].parse_form_parameters(**kwargs)
        kwargs["model"] = SimSirModel(pars)  # note that this call modifies pars!
        kwargs["pars"] = pars

        callback_returns = []
        for component in self.components.values():
            try:
                callback_returns += component.callback(**kwargs)
            except Exception as error:
                raise HTMLComponentError(component, error)

        return callback_returns
