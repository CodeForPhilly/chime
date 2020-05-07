"""Constants."""

from datetime import date

"""
This reflects a date from which previously-run reports will no
longer match current results, indicating when users should
re-run their reports
"""
CHANGE_DATE = date(year=2020, month=4, day=8)
VERSION = 'v1.1.5'

DATE_FORMAT = "%b, %d"  # see https://strftime.org
DOCS_URL = "https://code-for-philly.gitbook.io/chime"

EPSILON = 1.0e-7

FLOAT_INPUT_MIN = 0.0001
FLOAT_INPUT_STEP = 0.1

PREFIT_ADDITIONAL_DAYS = 300
