from unittest.mock import patch, MagicMock

import dash_core_components as dcc
import dash_html_components as html
import pytest
from dash import Dash
from dash.dependencies import Input, Output

from src.chime_dash.app.utils.callbacks import (
    ChimeCallback,
    register_callbacks,
    wrap_callbacks,
)


@pytest.mark.parametrize(
    "callbacks, new_callbacks, registered_callback_length",
    [
        ([], [], 0),
        ([], ["ChimeCallback1", "ChimeCallback2", "ChimeCallback3"], 3),
        (["ChimeCallback1"], ["ChimeCallback2", "ChimeCallback3"], 3),
        (["ChimeCallback1"], [], 1),
    ],
)
def test_register_callbacks(
    callbacks, new_callbacks, registered_callback_length, monkeypatch
):
    registered_callbacks = callbacks
    monkeypatch.setattr(
        "src.chime_dash.app.utils.callbacks.__registered_callbacks",
        registered_callbacks,
    )
    register_callbacks(new_callbacks)
    assert len(registered_callbacks) == registered_callback_length


def test_wrap_callbacks(dash_app, monkeypatch):
    mock_chime_callback = MagicMock()
    monkeypatch.setattr(
        "src.chime_dash.app.utils.callbacks.__registered_callbacks",
        [mock_chime_callback],
    )
    wrap_callbacks(dash_app)
    mock_chime_callback.wrap.assert_called_once_with(dash_app)


def test_ChimeCallback_wrap(dash_app):
    # set up the layout
    dash_app.layout = html.Div(
        id="root",
        children=[
            dcc.Input(id="input-id", value="initial value", type="text"),
            html.Div(id="output-id"),
        ],
    )
    # create a callback for elements in this layout
    chime_callback = ChimeCallback(
        changed_elements={"input-id": "value"},
        callback_fn=lambda *args, **kwargs: ["new value"],
        dom_updates={"output-id": "children"},
    )

    # register the Chime Callback with the layout
    chime_callback.wrap(dash_app)

    assert list(dash_app.callback_map)[0] == "..output-id.children.."
    assert dash_app.callback_map["..output-id.children.."]["inputs"] == [
        {"id": "input-id", "property": "value"}
    ]
    assert dash_app.callback_map["..output-id.children.."]["callback"]
