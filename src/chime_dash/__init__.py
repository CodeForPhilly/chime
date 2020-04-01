"""
chime_dash/app

dash instance defined here
"""

from dash import Dash
from typing import TypeVar
from chime_dash.app.config import from_object
from penn_chime.settings import DEFAULTS
from chime_dash.app.components import Body
from chime_dash.app.utils.callbacks import wrap_callbacks

DashAppInstance = TypeVar('dash.Dash')

def create_app(context:str='prod')-> DashAppInstance:
    """
    create_app initializes the app instance
    
    Args:
        context (str, optional): One of either 'prod', 'dev', 'testing.
        Defaults to 'prod'. Change to 'dev' to set debug to true.
    
    Returns:
        DashAppInstance: Dash instance with appropriate configuration settings
    """

    Env = from_object(context)
    
    LANGUAGE = Env.LANG
    body = Body(LANGUAGE, DEFAULTS)
    
    
    App = Dash(
        __name__,
        external_stylesheets=body.external_stylesheets,
        external_scripts=body.external_scripts,
    )

    App.title = Env.CHIME_TITLE
    App.layout = body.html
    wrap_callbacks(App)

    

    return Env, App

