from collections import OrderedDict
from typing import Callable, List

from dash.dependencies import Input, Output


class ChimeCallback:
    def __init__(self,
                 changed_elements: OrderedDict,
                 dom_updates: OrderedDict,
                 callback_fn: Callable,
                 memoize: bool = True
                 ):
        pass
        self.inputs = [
            Input(component_id=component_id, component_property=component_property)
            for component_id, component_property in changed_elements.items()
        ]
        self.outputs = [
            Output(component_id=component_id, component_property=component_property)
            for component_id, component_property in dom_updates.items()
        ]
        self.callback_fn = callback_fn
        self.memoize = memoize


registered_callbacks: List[ChimeCallback] = []


def register_callbacks(callbacks: List[ChimeCallback]):
    if callbacks:
        registered_callbacks.extend(callbacks)

