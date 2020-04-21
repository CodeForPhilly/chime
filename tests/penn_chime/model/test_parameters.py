"""Test Parameters."""

from penn_chime.model.parameters import Parameters


def test_cypress_defaults():
    """Ensure the cypress defaults have been updated."""
    # TODO how to make this work when the module is installed?
    _ = Parameters.create({"PARAMETERS": "./defaults/cypress.cfg"}, [])


def test_cli_defaults():
    """Ensure the cli defaults have been updated."""
    # TODO how to make this work when the module is installed?
    _ = Parameters.create({"PARAMETERS": "./defaults/cli.cfg"}, [])


def test_webapp_defaults():
    """Ensure the webapp defaults have been updated."""
    # TODO how to make this work when the module is installed?
    _ = Parameters.create({"PARAMETERS": "./defaults/webapp.cfg"}, [])
