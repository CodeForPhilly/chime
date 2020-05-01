"""Parameters.

Changes affecting results or their presentation should also update
constants.py `change_date``.
"""

from __future__ import annotations
import i18n

from argparse import ArgumentParser
from collections import namedtuple
from datetime import date, datetime
from logging import INFO, basicConfig, getLogger
from sys import stdout
from typing import Dict, List

from ..constants import (
    CHANGE_DATE,
    VERSION,
)
from .validators import (
    Date,
    GteOne,
    OptionalDate,
    OptionalValue,
    OptionalStrictlyPositive,
    Positive,
    Rate,
    StrictlyPositive,
    ValDisposition,
)


basicConfig(
    level=INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=stdout,
)
logger = getLogger(__name__)


# Parameters for each disposition (hospitalized, icu, ventilated)
#   The rate of disposition within the population of infected
#   The average number days a patient has such disposition

# Hospitalized:
#   2.5 percent of the infected population are hospitalized: hospitalized.rate is 0.025
#   Average hospital length of stay is 7 days: hospitalized.days = 7

# ICU:
#   0.75 percent of the infected population are in the ICU: icu.rate is 0.0075
#   Average number of days in an ICU is 9 days: icu.days = 9

# Ventilated:
#   0.5 percent of the infected population are on a ventilator: ventilated.rate is 0.005
#   Average number of days on a ventilator: ventilated.days = 10

# Be sure to multiply by 100 when using the parameter as a default to a percent widget!


_Disposition = namedtuple("_Disposition", ("days", "rate"))


class Disposition(_Disposition):

    @classmethod
    def create(cls, *, days: int, rate: float):
        """Mandate key word arguments."""
        GteOne(key="days", value=days)
        Rate(key="rate", value=rate)
        return cls(days, rate)


class Regions:
    """Arbitrary regions to sum population."""

    def __init__(self, **kwargs):
        population = 0
        for key, value in kwargs.items():
            setattr(self, key, value)
            population += value
        self.population = population


def cast_date(string):
    return datetime.strptime(string, '%Y-%m-%d').date()


def declarative_validator(cast):
    """Validator."""

    def validate(string):
        """Validate."""
        if string == '' and cast != str:
            return None
        return cast(string)

    return validate


def validator(arg, cast, min_value, max_value, required=True):
    """Validator."""

    def validate(string):
        """Validate."""
        if string == '' and cast != str:
            if required:
                raise ValueError(f'{arg} is required.')
            return None
        value = cast(string)
        if min_value is not None and value < min_value:
            raise ValueError(f'{arg} must be greater than {min_value}.')
        if max_value is not None and value > max_value:
            raise ValueError(f'{arg} must be less than {max_value}.')
        return value

    return validate


# TODO make validators cast and report properties for args


VALIDATORS = {
    "current_hospitalized": Positive,
    "current_date": OptionalDate,
    "date_first_hospitalized": OptionalDate,
    "doubling_time": OptionalStrictlyPositive,
    "infectious_days": StrictlyPositive,
    "mitigation_date": OptionalDate,
    "market_share": Rate,
    "max_y_axis": OptionalStrictlyPositive,
    "n_days": StrictlyPositive,
    "population": OptionalStrictlyPositive,
    "recovered": Positive,
    "region": OptionalValue,
    "relative_contact_rate": Rate,
    "ventilated": ValDisposition,
    "hospitalized": ValDisposition,
    "icu": ValDisposition,
    "use_log_scale": OptionalValue
}


HELP = {
    "current_hospitalized": "Currently hospitalized COVID-19 patients (>= 0)",
    "current_date": "Date on which the projection should be based (default is today)",
    "date_first_hospitalized": "Date the first patient was hospitalized",
    "doubling_time": "Doubling time before social distancing (days)",
    "hospitalized_days": "Average hospital length of stay (in days)",
    "hospitalized_rate": "Hospitalized Rate: 0.00001 - 1.0",
    "icu_days": "Average days in ICU",
    "icu_rate": "ICU rate: 0.0 - 1.0",
    "infectious_days": "Infectious days",
    "mitigation_date": "Date on which social distancing measures too effect",
    "market_share": "Hospital market share (0.00001 - 1.0)",
    "max_y_axis": "Max y-axis",
    "n_days": "Number of days to project >= 1 and less than 30",
    "parameters": "Parameters file",
    "population": "Regional population >= 1",
    "recovered": "Number of patients already recovered (not yet implemented)",
    "region": "No help available",
    "relative_contact_rate": "Social distancing reduction rate: 0.0 - 1.0",
    "ventilated_days": "Average days on ventilator",
    "ventilated_rate": "Ventilated Rate: 0.0 - 1.0",
    "use_log_scale": "Flag to use logarithmic scale on charts instead of linear scale."
}


ARGS = (
    (
        "parameters",
        str,
        None, # Min value
        None, # Max value
        False, # Whether it is required or optional.
    ),
    (
        "current_hospitalized",
        int,
        0,
        None,
        True,
    ),
    (
        "current_date",
        cast_date,
        None,
        None,
        False,
    ),
    (
        "date_first_hospitalized",
        cast_date,
        None,
        None,
        False,
    ),
    (
        "doubling_time",
        float,
        0.0,
        None,
        True,
    ),
    (
        "hospitalized_days",
        int,
        1,
        None,
        True,
    ),
    (
        "hospitalized_rate",
        float,
        0.00001,
        1.0,
        True,
    ),
    (
        "icu_days",
        int,
        1,
        None,
        True,
    ),
    (
        "icu_rate",
        float,
        0.0,
        1.0,
        True,
    ),
    (
        "market_share",
        float,
        0.00001,
        1.0,
        True,
    ),
    (
        "infectious_days",
        int,
        0.0,
        None,
        True,
    ),
    (
        "mitigation_date",
        cast_date,
        None,
        None,
        False,
    ),
    (
        "max_y_axis",
        int,
        0,
        None,
        True,
    ),
    (
        "n-days",
        int,
        1,
        30,
        True,
    ),
    (
        "recovered",
        int,
        0,
        None,
        True,
    ),
    (
        "relative-contact-rate",
        float,
        0.0,
        1.0,
        True,
    ),
    (
        "population",
        int,
        1,
        None,
        True,
    ),
    (
        "ventilated_days",
        int,
        1,
        None,
        True,
    ),
    (
        "ventilated_rate",
        float,
        0.0,
        1.0,
        True,
    ),
    (
        "use_log_scale",
        bool,
        None,
        None,
        False
    )
)


def to_cli(name):
    return "--" + name.replace('_', '-')

class Parameters:
    """
    Object containing all of the parameters that can be adjusted by the user, either from the command line or using
    the side bar of the web app.
    """

    @classmethod
    def parser(cls):
        parser = ArgumentParser(
            description=f"penn_chime: {VERSION} {CHANGE_DATE}")

        for name, cast, min_value, max_value, required in ARGS:
            arg = to_cli(name)
            if cast == bool:
                # This argument is a command-line flag and does not need validation.
                parser.add_argument(
                    arg,
                    action='store_true',
                    help=HELP.get(name),
                )
            else:
                # Use a custom validator for any arguments that take in values.
                parser.add_argument(
                    arg,
                    type=validator(arg, cast, min_value, max_value, required),
                    help=HELP.get(name),
                )
        return parser

    @classmethod
    def create(
        cls,
        env: Dict[str, str],
        argv: List[str],
    ) -> Parameters:
        parser = cls.parser()
        a = parser.parse_args(argv)

        if a.parameters is None:
            a.parameters = env.get("PARAMETERS")

        if a.parameters is not None:
            logger.info('Using file: %s', a.parameters)
            with open(a.parameters, 'r') as fin:
                parser.parse_args(fin.read().split(), a)

        del a.parameters

        Positive(key='hospitalized_days', value=a.hospitalized_days)
        Positive(key='icu_days', value=a.icu_days)
        Positive(key='ventilated_days', value=a.ventilated_days)

        Rate(key='hospitalized_rate', value=a.hospitalized_rate)
        Rate(key='icu_rate', value=a.icu_rate)
        Rate(key='ventilated_rate', value=a.ventilated_rate)

        hospitalized = Disposition.create(
            days=a.hospitalized_days,
            rate=a.hospitalized_rate,
        )
        icu = Disposition.create(
            days=a.icu_days,
            rate=a.icu_rate,
        )
        ventilated = Disposition.create(
            days=a.ventilated_days,
            rate=a.ventilated_rate,
        )

        del a.hospitalized_days
        del a.hospitalized_rate
        del a.icu_days
        del a.icu_rate
        del a.ventilated_days
        del a.ventilated_rate

        return cls(
            hospitalized=hospitalized,
            icu=icu,
            ventilated=ventilated,
            **vars(a),
        )

    def __init__(self, **kwargs):
        today = date.today()

        # mypy needs properties
        self.current_date = None
        self.current_hospitalized = None
        self.date_first_hospitalized = None
        self.doubling_time = None
        self.hospitalized = None
        self.icu = None
        self.infectious_days = None
        self.market_share = None
        self.max_y_axis = None
        self.mitigation_date = None
        self.n_days = None
        self.population = None
        self.region = None
        self.relative_contact_rate = None
        self.recovered = None
        self.ventilated = None
        self.use_log_scale = False

        passed_and_default_parameters = {}
        for key, value in kwargs.items():
            if key not in VALIDATORS:
                raise ValueError(f"Unexpected parameter {key}")
            passed_and_default_parameters[key] = value

        for key, value in passed_and_default_parameters.items():
            validator = VALIDATORS[key]
            try:
                validator(key=key, value=value)
            except TypeError as ve:
                raise ValueError(
                    f"For parameter '{key}', with value '{value}', validation returned error \"{ve}\"")
            setattr(self, key, value)

        if self.region is None and self.population is None:
            raise AssertionError('population or regions must be provided.')

        if self.current_date is None:
            self.current_date = today

        if self.mitigation_date is None:
            self.mitigation_date = today

        Date(key='current_date', value=self.current_date)
        Date(key='mitigation_date', value=self.mitigation_date)

        self.labels = {
            "admits_hospitalized": i18n.t("admits_hospitalized"),
            "admits_icu": i18n.t("admits_icu"),
            "admits_ventilated": i18n.t("admits_ventilated"),
            "census_hospitalized": i18n.t("census_hospitalized"),
            "census_icu": i18n.t("census_icu"),
            "census_ventilated": i18n.t("census_ventilated"),
            "day": i18n.t("day"),
            "date": i18n.t("date"),
            "susceptible" :i18n.t("susceptible"),
            "infected": i18n.t("infected"),
            "recovered": i18n.t("recovered")
        }

        self.dispositions = {
            "hospitalized": self.hospitalized,
            "icu": self.icu,
            "ventilated": self.ventilated,
        }
