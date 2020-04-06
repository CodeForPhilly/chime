""""""
from penn_chime.parameters import Parameters


def test_cli_defaults():
    """Ensure if the cli defaults have been updated."""
    # TODO how to make this work when the module is installed?
    _ = Parameters.create({'PARAMETERS': './defaults/cli.cfg'}, [])


def test_streamlit_defaults():
    """Ensure the streamlit defaults have beedn updated."""
    # TODO how to make this work when the module is installed?
    _ = Parameters.create({'PARAMETERS': './defaults/streamlit.cfg'}, [])
