"""Script which launches dash app
"""
from chime_dash.app import DASH_APP
from chime_dash.app.components import root
from chime_dash.app.utils.callbacks import registered_callbacks, ChimeCallback
from functools import lru_cache

DASH_APP.config["external_stylesheets"] = root.external_stylesheets
DASH_APP.config["external_scripts"] = root.external_scripts
DASH_APP.layout = root.html

for callback in registered_callbacks[ChimeCallback]:
    if callback.memoize:
        @lru_cache(maxsize=32)
        @DASH_APP.callback(callback.outputs, callback.inputs)
        def callback_wrapper(*args, **kwargs):
            callback.callback_fn(args, kwargs)
    else:
        @DASH_APP.callback(callback.outputs, callback.inputs)
        def callback_wrapper(*args, **kwargs):
            callback.callback_fn(args, kwargs)

if __name__ == "__main__":
    DASH_APP.server.run_server(host='0.0.0.0')
