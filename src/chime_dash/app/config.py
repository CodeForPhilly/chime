"""
 app/config
"""

import __main__
from pathlib import Path


_entrypoint = Path(__main__.__file__)


class Base:

    root = str(_entrypoint.parent)
    debug = False
    LANG = "en"
    CHIME_TITLE = "Penn Medicine CHIME"


class Development(Base):
    """Development environment config"""

    debug = True


class Testing(Base):
    """Testing environment config"""

    debug = True


class Production(Base):
    """Production environment config"""

    debug = False


def from_object(context: str):

    envs = {"dev": Development(), "test": Testing(), "prod": Production()}

    if context in envs.keys():
        return envs[context]
    else:
        raise ValueError('Please select a valid environment')
        


