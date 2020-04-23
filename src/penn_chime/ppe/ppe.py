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

    excel_file = None

    @classmethod
    def __init__(cls, env: Dict[str, str]):
        cls.excel_file = env.get("PPE_EXCEL")
        return

    @classmethod
    def display_ppe_download_link(cls, st):
        excel = excel_to_base64(cls.excel_file)
        filename = cls.excel_file[cls.excel_file.rfind('/')+1:]
        st.markdown("""
                        Download the PPE forecasting tool here: <a download="{filename}" href="data:file/xlsx;base64,{excel}">{filename}</a>.
                    """.format(excel=excel, filename=filename), unsafe_allow_html=True
                    )