"""PPE.


"""

from __future__ import annotations

from argparse import ArgumentParser
from collections import namedtuple
from datetime import date, datetime
from logging import INFO, basicConfig, getLogger
from sys import stdout
from typing import Dict, List
from ..utils import excel_to_base64


from ..constants import (
    CHANGE_DATE,
    VERSION,
)

basicConfig(
    level=INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=stdout,
)
logger = getLogger(__name__)


class PPE:

    ppe_folder = None

    @classmethod
    def __init__(cls, env: Dict[str, str]):
        cls.ppe_folder = env.get("PPE_FOLDER")
        return

    @classmethod
    def display_ppe_download_link(cls, st):
        excel_filepath = cls.ppe_folder+'PPE_Calculator_for_COVID-19.xlsx'
        filename = excel_filepath[excel_filepath.rfind('/')+1:]
        excel = excel_to_base64(excel_filepath)
        st.markdown("""
                        Download the PPE Calculator here: <a download="{filename}" href="data:file/xlsx;base64,{excel}">{filename}</a>.
                    """.format(excel=excel, filename=filename), unsafe_allow_html=True
                    )