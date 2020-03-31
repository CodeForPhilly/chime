"""Command line interface."""

from argparse import (
    Action,
    ArgumentParser,
)
from datetime import datetime

from pandas import DataFrame

from .constants import CHANGE_DATE
from .parameters import Parameters, Disposition
from .models import SimSirModel as Model


class FromFile(Action):
    """From File."""

    def __call__(self, parser, namespace, values, option_string=None):
        with values as f:
            parser.parse_args(f.read().split(), namespace)


def cast_date(string):
    return datetime.strptime(string, '%Y-%m-%d').date()


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

    for arg, cast, min_value, max_value, help, required in (
        (
            "--current-hospitalized",
            int,
            0,
            None,
            "Currently Hospitalized COVID-19 Patients (>= 0)",
            True,
        ),
        (
            "--date-first-hospitalized",
            cast_date,
            None,
            None,
            "Current date",
            False,
        ),
        (
            "--doubling-time",
            float,
            0.0,
            None,
            "Doubling time before social distancing (days)",
            True,
        ),
        ("--hospitalized-days", int, 0, None, "Average Hospital Length of Stay (days)", True),
        (
            "--hospitalized-rate",
            float,
            0.00001,
            1.0,
            "Hospitalized Rate: 0.00001 - 1.0",
            True,
        ),
        ("--icu-days", int, 0, None, "Average Days in ICU", True),
        ("--icu-rate", float, 0.0, 1.0, "ICU Rate: 0.0 - 1.0", True),
        (
            "--market_share",
            float,
            0.00001,
            1.0,
            "Hospital Market Share (0.00001 - 1.0)",
            True,
        ),
        ("--infectious-days", float, 0.0, None, "Infectious days", True),
        ("--n-days", int, 0, None, "Number of days to project >= 0", True),
        (
            "--relative-contact-rate",
            float,
            0.0,
            1.0,
            "Social Distancing Reduction Rate: 0.0 - 1.0",
            True,
        ),
        ("--population", int, 1, None, "Regional Population >= 1", True),
        ("--ventilated-days", int, 0, None, "Average Days on Ventilator", True),
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

    p = Parameters(
        current_hospitalized=a.current_hospitalized,
        date_first_hospitalized=a.date_first_hospitalized,
        doubling_time=a.doubling_time,
        infectious_days=a.infectious_days,
        market_share=a.market_share,
        n_days=a.n_days,
        relative_contact_rate=a.relative_contact_rate,
        population=a.population,

        hospitalized=Disposition(a.hospitalized_rate, a.hospitalized_days),
        icu=Disposition(a.icu_rate, a.icu_days),
        ventilated=Disposition(a.ventilated_rate, a.ventilated_days),
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
