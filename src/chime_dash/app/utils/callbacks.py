from dash import Dash
from dash.exceptions import DuplicateCallbackOutput
# todo Change to `from collections.abc import Iterable`. Using OrderedDict prevents multiple outputs to same DOM element
# todo e.g., update children and toggle hidden
from collections import OrderedDict
from typing import Callable, List
from functools import lru_cache

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

    def wrap(self, app: Dash):
        if self.memoize:
            @lru_cache(maxsize=32)
            @app.callback(self.outputs, self.inputs)
            def callback_wrapper(*args, **kwargs):
                return self.callback_fn(*args, **kwargs)
        else:
            @app.callback(self.outputs, self.inputs)
            def callback_wrapper(*args, **kwargs):
                return self.callback_fn(*args, **kwargs)


__registered_callbacks: List[ChimeCallback] = []


def register_callbacks(callbacks: List[ChimeCallback]):
    if callbacks:
        __registered_callbacks.extend(callbacks)


def wrap_callbacks(app):
    for callback in __registered_callbacks:
        callback.wrap(app)
