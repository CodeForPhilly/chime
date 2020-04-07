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
from typing import Any, List
from datetime import date, datetime
from dateutil.parser import parse as parse_date
from collections import Mapping
from pandas import DataFrame

from chime_dash.app.services.plotting import plot_dataframe
from chime_dash.app.utils.templates import df_to_html_table

from penn_chime.parameters import Parameters, Disposition
from penn_chime.constants import DATE_FORMAT
from penn_chime.charts import build_table


class ReadOnlyDict(Mapping):
    def __init__(self, data):
        self._data = data

    def __getitem__(self, key):
        return self._data[key]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def keys(self):
        return self._data.keys()


def _parameters_serializer_helper(obj):
    if isinstance(obj, (datetime, date)):
        result = obj.isoformat()
    else:
        result = obj.__dict__
    return result


# todo handle versioning? we don"t currently persist Dash state, but we may. ¯\_(ツ)_/¯
def parameters_serializer(p: Parameters):
    return dumps(p, default=_parameters_serializer_helper, sort_keys=True)


def parameters_deserializer(p_json: str):
    values = loads(p_json)
    dfh = (
        parse_date(values["date_first_hospitalized"])
        if values["date_first_hospitalized"]
        else None
    )
    result = Parameters(
        current_hospitalized=values["current_hospitalized"],
        hospitalized=Disposition(*values["hospitalized"]),
        icu=Disposition(*values["icu"]),
        relative_contact_rate=values["relative_contact_rate"],
        ventilated=Disposition(*values["ventilated"]),
        current_date=parse_date(values["current_date"]),
        date_first_hospitalized=dfh,
        doubling_time=values["doubling_time"],
        infectious_days=values["infectious_days"],
        market_share=values["market_share"],
        max_y_axis=values["max_y_axis"],
        n_days=values["n_days"],
        population=values["population"],
        recovered=values["recovered"],
        region=values["region"],
    )

    for key, value in values.items():

        if result.__dict__[key] != value and key not in (
            "dispositions",
            "hospitalized",
            "icu",
            "ventilated",
            "current_date",
            "date_first_hospitalized",
        ):
            result.__dict__[key] = value

    return result


def build_csv_download(df):
    return "data:text/csv;charset=utf-8,{csv}".format(
        csv=quote(df.to_csv(index=True, encoding="utf-8"))
    )


def get_n_switch_values(input_value, elements_to_update) -> List[bool]:
    result = []
    boolean_input_value = False
    if input_value == [True]:
        boolean_input_value = True
    for _ in repeat(None, elements_to_update):
        # todo Fix once switch values make sense. Currently reported as "None" for off and "[False]" for on
        result.append(not boolean_input_value)
    return result


def prepare_visualization_group(df: DataFrame = None, **kwargs) -> List[Any]:
    """Creates plot, table and download link for data frame.

    Arguments:
        df: The Dataframe to plot
        content: Dict[str, str]
            Mapping for translating columns and index.
        max_y_axis:  int
            Maximal value on y-axis
        labels: List[str]
            Columns to display
        table_mod: int
            Displays only each `table_mod` row in table

    """
    result = [{}, None, None]
    if df is not None and isinstance(df, DataFrame):

        date_column = "date"
        day_column = "day"

        # Translate column and index if specified
        content = kwargs.get("content", None)
        if content:
            columns = {col: content[col] for col in df.columns if col in content}
            index = (
                {df.index.name: content[df.index.name]}
                if df.index.name and df.index.name in content
                else None
            )
            df = df.rename(columns=columns, index=index)
            date_column = content.get(date_column, date_column)
            day_column = content.get(day_column, day_column)

        plot_data = plot_dataframe(
            df.dropna().set_index(date_column).drop(columns=[day_column]),
            max_y_axis=kwargs.get("max_y_axis", None),
        )


        # translate back for backwards compability of build_table
        column_map = {day_column: "day", date_column: "date"}
        table = (
            df_to_html_table(
                build_table(
                    df=df.rename(columns=column_map),
                    labels=kwargs.get("labels", df.columns),
                    modulo=kwargs.get("table_mod", 7),
                ),
                formats={
                    float: int,
                    (date, datetime): lambda d: d.strftime(DATE_FORMAT),
                },
            )
            # if kwargs.get("show_tables", None)
            # else None
        )

        # Convert columnnames to lowercase
        column_map = {col: col.lower() for col in df.columns}
        csv = build_csv_download(df.rename(columns=column_map))
        result = [plot_data, table, csv]

    return result


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance
