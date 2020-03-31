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
from json import dumps, loads

from penn_chime.parameters import Parameters
from penn_chime.utils import RateLos


def parameters_serializer(p: Parameters):
    return dumps(p, default=lambda o: o.__dict__, sort_keys=True)


def parameters_deserializer(p_json: str):
    values = loads(p_json)
    result = Parameters(
        current_hospitalized=values["current_hospitalized"],
        doubling_time=values["doubling_time"],
        known_infected=values["known_infected"],
        relative_contact_rate=values["relative_contact_rate"],
        susceptible=values["susceptible"],
        hospitalized=RateLos(*values["hospitalized"]),
        icu=RateLos(*values["icu"]),
        ventilated=RateLos(*values["ventilated"])
    )

    for key, value in values.items():
        if result.__dict__[key] != value and key not in ["hospitalized", "icu", "ventilated", "dispositions"]:
            result.__dict__[key] = value

    return result


def build_csv_download(df):
    return "data:text/csv;charset=utf-8,{csv}".format(csv=quote(df.to_csv(index=True, encoding='utf-8')))


def get_n_switch_values(input_value, elements_to_update):
    result = []
    boolean_input_value = False
    if input_value == [True]:
        boolean_input_value = True
    for _ in repeat(None, elements_to_update):
        # todo Fix once switch values make sense. Currently reported as 'None' for off and '[False]' for on
        result.append(not boolean_input_value)
    return result
