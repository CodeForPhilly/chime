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
                 dom_states: Mapping = None,
                 stores: Iterable = None,
                 states: Mapping = None,
                 memoize: bool = True
                 ):
        self.inputs = [
            Input(component_id=component_id, component_property=component_property)
            for component_id, component_property in changed_elements.items()
        ]
        self.outputs = []
        self.stores = []
        self.states = []
        self.callback_fn = callback_fn
        self.memoize = memoize
        if dom_updates:
            self.outputs.extend(
                Output(component_id=component_id, component_property=component_property)
                for component_id, component_property in dom_updates.items()
            )
        if dom_states:
            self.outputs.extend(
                Output(component_id=component_id, component_property=component_property)
                for component_id, component_property in dom_states.items()
            )

        if stores:
            self.states.extend(
                State(component_id=component_id, component_property="data")
                for component_id in stores
            )
            if states:
                self.states.extend(
                    State(component_id=component_id, component_property=component_property)
                    for component_id, component_property in states.items()
                )

    def wrap(self, app: Dash):
        print(f'Registering callback: \nOutputs: \n{self.outputs}, \nInputs:\n{self.inputs}, \nStore: \n{self.stores} \nUsing: {self.callback_fn}\n\n')
        if self.memoize:
            @lru_cache(maxsize=32)
            @app.callback(self.outputs, self.inputs, self.states)
            def callback_wrapper(*args, **kwargs):
                print(str(self.callback_fn))
                return self.callback_fn(*args, **kwargs)
        else:
            @app.callback(self.outputs, self.inputs, self.states)
            def callback_wrapper(*args, **kwargs):
                return self.callback_fn(*args, **kwargs)


__registered_callbacks: List[ChimeCallback] = []


def register_callbacks(callbacks: List[ChimeCallback]):
    if callbacks:
        __registered_callbacks.extend(callbacks)


def wrap_callbacks(app):
    for callback in __registered_callbacks:
        callback.wrap(app)
