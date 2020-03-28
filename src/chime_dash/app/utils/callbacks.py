from collections import OrderedDict
from typing import Callable, List

from dash.dependencies import Input, Output, DashDependency


class ChimeCallback:
    @staticmethod
    def _convert_to_dash_dependency(dep: OrderedDict[str, str], dep_type: type[DashDependency]):
        result = []
        for component_id, component_property in dep.values():
            result.append(dep_type(component_id=component_id, component_property=component_property))
        return result

    def __init__(self,
                 changed_elements: OrderedDict[str, str],
                 dom_updates: OrderedDict[str, str],
                 callback_fn: Callable,
                 memoize: bool = True
                 ):

        self.inputs = ChimeCallback._convert_to_dash_dependency(changed_elements, Input)
        self.outputs = ChimeCallback._convert_to_dash_dependency(dom_updates, Output)
        self.callback_fn = callback_fn
        self.memoize = memoize


registered_callbacks: List[ChimeCallback] = []


def register_callbacks(callbacks: List[ChimeCallback]):
    registered_callbacks.extend(callbacks)

