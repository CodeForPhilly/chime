"""Script which launches dash app
"""
from chime_dash.app.run import DASH


if __name__ == "__main__":
    #    main()
    DASH.run_server(host="0.0.0.0")
