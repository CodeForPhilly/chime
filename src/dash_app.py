"""Script which launches dash app

Config: Environment specific settings are defined in chime_dash/app/config
change the context argument in create_app to select between 'dev', 'prod',
and testing environments
"""
from chime_dash import create_app

ENV, DASH = create_app(context="prod")
server = DASH.server

if __name__ == "__main__":
    DASH.run_server(host="0.0.0.0", debug=ENV.debug)
