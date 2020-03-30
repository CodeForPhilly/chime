"""app/utils
utils
The helper classes and functions here exist to reduce large repetitive code
blocks throughout the project. They may contain functions or classes from
module but do not change the parameters of the class
Modules
-------
templates       utilities for localization templates
"""
from . import callbacks
from . import templates
from itertools import repeat
from urllib.parse import quote


def build_csv_download(df):
    return "data:text/csv;charset=utf-8,{csv}".format(csv=quote(df.to_csv(index=True, encoding='utf-8')))


def toggle_hidden(boolean_input_value, elements_to_update):
    result = []
    for _ in repeat(None, elements_to_update):
        # todo Fix once switch values make sense. Currently reported as 'None' for off and '[False]' for on
        result.append(not boolean_input_value)
    return result
