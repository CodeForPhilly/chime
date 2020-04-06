"""Parameters.

Changes affecting results or their presentation should also update
constants.py `change_date``.
"""

from __future__ import annotations

from argparse import (
    Action,
    ArgumentParser,
)
from collections import namedtuple
from datetime import date, datetime
from typing import Dict, List

from .constants import (
    CHANGE_DATE,
    VERSION,
)
from .validators import (
    Date,
    OptionalDate,
    OptionalValue,
    OptionalStrictlyPositive,
    Positive,
    Rate,
    StrictlyPositive,
    ValDisposition,
)

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
        Positive(key='days', value=days)
        Rate(key='rate', value=rate)
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


# Dictionary from parameter names to Tuples containing (validator, cast function, help text)
ACCEPTED_PARAMETERS = {
    "current_hospitalized": (Positive, int, "Currently hospitalized COVID-19 patients (>= 0)"),
    "current_date": (OptionalDate, cast_date, "Date on which the forecast should be based"),
    "date_first_hospitalized": (OptionalDate, cast_date, "Date the first patient was hospitalized"),
    "doubling_time": (OptionalStrictlyPositive, float, "Doubling time before social distancing (days)"),
    "hospitalized": (ValDisposition, None, None),
    "icu": (ValDisposition, None, None),
    "infectious_days": (StrictlyPositive, int, "Infectious days"),
    "mitigation_date": (OptionalDate, cast_date, "Date on which social distancing measures too effect"),
    "market_share": (Rate, float, "Hospital market share (0.00001 - 1.0)"),
    "max_y_axis": (OptionalStrictlyPositive, int, None),
    "n_days": (StrictlyPositive, int, "Number of days to project >= 0"),
    "population": (OptionalStrictlyPositive, int, "Regional population >= 1"),
    "recovered": (Positive, int, "Number of patients already recovered (not yet implemented)"),
    "region": (OptionalValue, None, "No help available"),
    "relative_contact_rate": (Rate, float, "Social distancing reduction rate: 0.0 - 1.0"),
    "ventilated": (ValDisposition, None, None),
}


class FromFile(Action):
    """From File."""

    def __call__(self, parser, namespace, values, option_string=None):
        with values as f:
            parser.parse_args(f.read().split(), namespace)


def to_cli(name):
    return "--" + name.replace('_', '-')


class Parameters:
    """Parameters."""

    @classmethod
    def parser(cls, environ: Dict[str, str]):
        parser = ArgumentParser(
            description=f"penn_chime: {VERSION} {CHANGE_DATE}")
        parser.add_argument(
            "--parameters",
            type=open,
            action=FromFile,
            default=environ.get("PARAMETERS"),
            help='Parameters file.'
        )

        for name, (params_validator, cast, help) in ACCEPTED_PARAMETERS.items():
            if cast is None:
                continue

            parser.add_argument(
                to_cli(name),
                type=declarative_validator(cast),
                help=help
            )

        for name, cast, min_value, max_value, help, required in (
            ("hospitalized_days", int, 0, None, "Average hospital length of stay (in days)", True),
            (
                "hospitalized_rate",
                float,
                0.00001,
                1.0,
                "Hospitalized Rate: 0.00001 - 1.0",
                True,
            ),
            ("icu_days", int, 0, None, "Average days in ICU", True),
            ("icu_rate", float, 0.0, 1.0, "ICU rate: 0.0 - 1.0", True),

            ("ventilated_days", int, 0, None, "Average days on ventilator", True),
            ("ventilated_rate", float, 0.0, 1.0, "Ventilated Rate: 0.0 - 1.0", True),
        ):
            arg = to_cli(name)
            parser.add_argument(
                arg,
                type=validator(arg, cast, min_value, max_value, required),
                help=help,
            )
        return parser

    @classmethod
    def create(
        cls,
        environ: Dict[str, str],
        argv: List[str],
    ) -> Parameters:
        parser = cls.parser(environ)
        a = parser.parse_args(argv)

        del a.parameters

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

        passed_and_default_parameters = {}
        for key, value in kwargs.items():
            if key not in ACCEPTED_PARAMETERS:
                raise ValueError(f"Unexpected parameter {key}")
            passed_and_default_parameters[key] = value

        for key, value in passed_and_default_parameters.items():
            validator = ACCEPTED_PARAMETERS[key][0]
            try:
                validator(key=key, value=value)
            except TypeError as ve:
                raise ValueError(f"For parameter '{key}', with value '{value}', validation returned error \"{ve}\"")
            setattr(self, key, value)

        if self.region is None and self.population is None:
            raise AssertionError('population or regions must be provided.')

        if self.current_date is None:
            self.current_date = today

        if self.mitigation_date is None:
            self.mitigation_Date = today

        Date(key='current_date', value=self.current_date)
        Date(key='mitigation_date', value=self.mitigation_date)

        self.labels = {
            "hospitalized": "Hospitalized",
            "icu": "ICU",
            "ventilated": "Ventilated",
            "day": "Day",
            "date": "Date",
            "susceptible": "Susceptible",
            "infected": "Infected",
            "recovered": "Recovered",
        }

        self.dispositions = {
            "hospitalized": self.hospitalized,
            "icu": self.icu,
            "ventilated": self.ventilated,
        }
