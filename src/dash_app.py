"""Script which launches dash app
"""
from flask import send_file, request

from penn_chime.settings import DEFAULTS

from chime_dash.app.run import DASH
from chime_dash.app.components import Body
from chime_dash.app.services.pdf_printer import print_to_pdf

LANGUAGE = "en"

BODY = Body(LANGUAGE, DEFAULTS)

DASH.layout = BODY.html
DASH.title = "Penn Medicine CHIME"  #! Should be moved into config / out of view


@DASH.server.route("/download-as-pdf")
def download_as_pdf():
    """Serve a file from the upload directory."""
    kwargs = dict()
    for key in BODY.callback_inputs:
        val = request.args.get(key, None)
        if val is not None:
            try:
                val = int(val) if val.isdigit() else float(val)
            except ValueError:
                pass
        kwargs[key] = val

    pdf = print_to_pdf(BODY.components["container"], kwargs)
    return send_file(
        pdf, as_attachment=True, mimetype="pdf", attachment_filename="CHIME-report.pdf",
    )


@DASH.callback(BODY.callback_outputs, list(BODY.callback_inputs.values()))
def callback(*args):  # pylint: disable=W0612
    return BODY.callback(*args)


if __name__ == "__main__":
    DASH.run_server(host="0.0.0.0")
