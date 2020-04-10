"""
chime_dash/app

dash instance defined here
"""

import os
from typing import TypeVar

from dash import Dash
from penn_chime.parameters import Parameters

from chime_dash.app.config import from_object
from chime_dash.app.pages.root import Root
from chime_dash.app.utils.callbacks import wrap_callbacks

DashAppInstance = TypeVar('DashAppInstance')


def create_app(context: str = 'prod') -> DashAppInstance:
    """
    create_app initializes the app instance

    Args:
        context (str, optional): One of either 'prod', 'dev', 'testing.
        Defaults to 'prod' where dash.Dash.run_server(debug=False).
        Change to 'dev' or 'test' to set debug to true.

    Returns:
        Env: Config variables based on context argument received
        DashAppInstance: Dash instance with appropriate configuration settings
    """

    Env = from_object(context)

    LANGUAGE = Env.LANG
    body = Root(
        LANGUAGE,
        Parameters.create(os.environ, []),
    )

    App = Dash(
        __name__,
        external_stylesheets=body.external_stylesheets,
        external_scripts=body.external_scripts,
    )

    App.title = Env.CHIME_TITLE
    App.layout = body.html
    wrap_callbacks(App)

    return Env, App
