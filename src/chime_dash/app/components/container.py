"""Initializes the  dash html
"""
from collections import OrderedDict
from copy import deepcopy

import dash_bootstrap_components as dbc
from chime_dash.app.components.base import Component, HTMLComponentError
from chime_dash.app.components.content import Content
from chime_dash.app.components.sidebar import Sidebar
from chime_dash.app.services.pdf_printer import print_to_pdf
from penn_chime.models import SimSirModel


class Container(Component):
    """
    """

    def __init__(self, language, defaults):
        """
        """
        super().__init__(language, defaults)
        self.components = OrderedDict(
            sidebar=Sidebar(language, defaults),
            content=Content(language, defaults),
        )
        self.callback_outputs = []
        self.callback_inputs = OrderedDict()
        for component in self.components.values():
            self.callback_outputs += component.callback_outputs
            self.callback_inputs.update(component.callback_inputs)

    def get_html(self):
        """Initializes the content container dash html
        """
        container = dbc.Container(
            children=dbc.Row(self.components["sidebar"].html + self.components["content"].html),
            fluid=True,
            className="mt-5",
        )

        return [container]

    def callback(self, *args, **kwargs):
        """
        """
        pars = self.components["sidebar"].parse_form_parameters(**kwargs)
        kwargs["model"] = SimSirModel(pars)
        kwargs["pars"] = pars

        callback_returns = []
        for component in self.components.values():
            try:
                callback_returns += component.callback(**kwargs)
            except Exception as error:
                raise HTMLComponentError(component, error)

        save_to_pdf = self.components["sidebar"].save_to_pdf(kwargs)
        if save_to_pdf:
            print_to_pdf(deepcopy(self.components['content']), kwargs)

        return callback_returns
