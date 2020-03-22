from flask import Flask
from dash import Dash
from flask_cors import CORS
from .config import config_by_name


def init_app(config_name: str)-> Dash:
    """
    init_app - instantiates the the Dash app and Flask server

    Args:
    ----
    config_name {str} - one of either "dev", "test" or "prod". Environment is
    configured accordingly.
    """
    # assert config_name is type(str)

    cfg = config_by_name[config_name]
    """Plotly Dash uses Flask as it web framework so you can pass your own
    flask app instance into dash at negligible cost and get a lot of added
    extensibility e.g. sending data back to a hub."""
    server = Flask(__name__)
    server.config.from_object(config_by_name[config_name])
    CORS(server)

    app = Dash(
        __name__,
        external_stylesheets=cfg.THEME,
        meta_tags=cfg.META_TAGS,
        server=server,
    )
    app.config.suppress_callback_exceptions = True  # For dynamic pages
    return app
