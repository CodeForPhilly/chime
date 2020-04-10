from dash import Dash
from dash.dependencies import Input, Output, State
from collections.abc import Iterable, Mapping
from typing import Callable, List
from functools import lru_cache


class ChimeCallback:
    def __init__(self,
                 changed_elements: Mapping,
                 callback_fn: Callable,
                 dom_updates: Mapping = None,
                 stores: Iterable = None,
                 memoize: bool = True
                 ):
        self.inputs = [
            Input(component_id=component_id, component_property=component_property)
            for component_id, component_property in changed_elements.items()
        ]
        self.outputs = []
        self.stores = []
        self.callback_fn = callback_fn
        self.memoize = memoize
        if dom_updates:
            self.outputs.extend(
                Output(component_id=component_id, component_property=component_property)
                for component_id, component_property in dom_updates.items()
            )
        if stores:
            self.stores.extend(
                State(component_id=component_id, component_property="data")
                for component_id in stores
            )

    def wrap(self, app: Dash):
        if self.memoize:
            @lru_cache(maxsize=32)
            @app.callback(self.outputs, self.inputs, self.stores)
            def callback_wrapper(*args, **kwargs):
                print(str(self.callback_fn))
                return self.callback_fn(*args, **kwargs)
        else:
            @app.callback(self.outputs, self.inputs, self.stores)
            def callback_wrapper(*args, **kwargs):
                return self.callback_fn(*args, **kwargs)


__registered_callbacks: List[ChimeCallback] = []


def register_callbacks(callbacks: List[ChimeCallback]):
    if callbacks:
        __registered_callbacks.extend(callbacks)


def wrap_callbacks(app):
    for callback in __registered_callbacks:
        callback.wrap(app)
