"""Script which launches dash app
"""
from chime_dash import DASH

server = DASH.server

if __name__ == "__main__":
    DASH.run_server(host="0.0.0.0")  #, debug=True)
