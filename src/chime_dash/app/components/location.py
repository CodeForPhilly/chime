from collections import OrderedDict
from typing import List

from dash.dependencies import Input as CallbackInput
from dash_core_components import Location

from chime_dash.app.components import Component
from dash.development.base_component import ComponentMeta


class LocationComponent(Component):
    callback_inputs = OrderedDict([('location',
                                    CallbackInput(
                                        component_id='location',
                                        component_property='pathname'))])

    def get_html(self) -> List[ComponentMeta]:
        return [Location(id='location')]
