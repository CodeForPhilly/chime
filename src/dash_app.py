"""Script which launches dash app
"""
from chime_dash.app.run import DASH
from penn_chime.settings import DEFAULTS
from chime_dash.app.components import Body
from chime_dash.app.utils.callbacks import wrap_callbacks

LANGUAGE = "en"

body = Body(LANGUAGE, DEFAULTS)

DASH.layout = body.html
DASH.title = "Penn Medicine CHIME"  #! Should be moved into config / out of view
wrap_callbacks(DASH)

if __name__ == "__main__":
    #    main()
    DASH.run_server(host="0.0.0.0")
