"""Command line interface."""

from argparse import (
    Action,
    ArgumentParser,
)

from pandas import DataFrame

from .constants import CHANGE_DATE
from .parameters import Parameters, Disposition, ACCEPTED_PARAMETERS
from .models import SimSirModel as Model


class FromFile(Action):
    """From File."""

    def __call__(self, parser, namespace, values, option_string=None):
        with values as f:
            parser.parse_args(f.read().split(), namespace)


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
                raise AssertionError('%s is required.')
            return None
        value = cast(string)
        if min_value is not None:
            assert value >= min_value
        if max_value is not None:
            assert value <= max_value
        return value

    return validate


def parse_args():
    """Parse args."""
    parser = ArgumentParser(description=f"penn_chime: {CHANGE_DATE}")
    parser.add_argument("--file", type=open, action=FromFile)

    for name, (params_validator, default, cast, help) in ACCEPTED_PARAMETERS.items():
        if cast is None:
            continue

        parser.add_argument(
            "--" + name.replace('_', '-'),
            type=declarative_validator(cast),
            default=default,
            help=help
        )

    for arg, cast, min_value, max_value, help, required in (
        ("--hospitalized-days", int, 0, None, "Average hospital length of stay (in days)", True),
        (
            "--hospitalized-rate",
            float,
            0.00001,
            1.0,
            "Hospitalized Rate: 0.00001 - 1.0",
            True,
        ),
        ("--icu-days", int, 0, None, "Average days in ICU", True),
        ("--icu-rate", float, 0.0, 1.0, "ICU rate: 0.0 - 1.0", True),

        ("--ventilated-days", int, 0, None, "Average days on ventilator", True),
        ("--ventilated-rate", float, 0.0, 1.0, "Ventilated Rate: 0.0 - 1.0", True),
    ):
        parser.add_argument(
            arg,
            type=validator(arg, cast, min_value, max_value, required),
            help=help,
        )
    return parser.parse_args()


def main():
    """Main."""
    a = parse_args()

    del a.file

    hospitalized = Disposition(a.hospitalized_rate, a.hospitalized_days)
    icu = Disposition(a.icu_rate, a.icu_days)
    ventilated = Disposition(a.ventilated_rate, a.ventilated_days)

    del a.hospitalized_days
    del a.hospitalized_rate
    del a.icu_days
    del a.icu_rate
    del a.ventilated_days
    del a.ventilated_rate

    p = Parameters(
        hospitalized=hospitalized,
        icu=icu,
        ventilated=ventilated,
        **vars(a)
    )

    m = Model(p)

    for df, name in (
        (m.sim_sir_w_date_df, "sim_sir_w_date"),
        (m.admits_df, "projected_admits"),
        (m.census_df, "projected_census"),
    ):
        df.to_csv(f"{p.current_date}_{name}.csv")


if __name__ == "__main__":
    main()
