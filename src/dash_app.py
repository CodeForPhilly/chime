"""Script which launches dash app
"""
import os

from dash import Dash
from flask import send_from_directory

from chime_dash.app.utils.templates import UPLOAD_DIRECTORY
from chime_dash.app.run import DASH
from penn_chime.settings import DEFAULTS
from chime_dash.app.components import Body

LANGUAGE = "en"


# ef main():
#   """Starts a dash app
#   """
#   body = Body(LANGUAGE, DEFAULTS)
#   app = Dash(
#       __name__,
#       external_stylesheets=body.external_stylesheets,
#       external_scripts=body.external_scripts,
#   )
#   app.layout = body.html
#
#   @app.callback(body.callback_outputs, list(body.callback_inputs.values()))
#   def callback(*args):  # pylint: disable=W0612
#       return body.callback(*args)
#
#   app.run_server(debug=True, host='0.0.0.0')


if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

body = Body(LANGUAGE, DEFAULTS)

DASH.layout = body.html
DASH.title = "Penn Medicine CHIME"  #! Should be moved into config / out of view


@DASH.server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


@DASH.callback(body.callback_outputs, list(body.callback_inputs.values()))
def callback(*args):  # pylint: disable=W0612
    return body.callback(*args)


# app.run_server(debug=True, host='0.0.0.0')


if __name__ == "__main__":
    #    main()
    DASH.run_server(host="0.0.0.0")
