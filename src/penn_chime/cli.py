"""Command line interface."""

from argparse import (
    Action,
    ArgumentParser,
)
from datetime import datetime

from pandas import DataFrame

from penn_chime.parameters import Parameters
from penn_chime.models import SimSirModel
from penn_chime.utils import RateLos

class FromFile(Action):
    """From File."""

    def __call__(self, parser, namespace, values, option_string=None):
        with values as f:
            parser.parse_args(f.read().split(), namespace)


def validator(cast, min_value, max_value):
    """Validator."""

    def validate(string):
        """Validate."""
        value = cast(string)
        if min_value is not None:
            assert value >= min_value
        if max_value is not None:
            assert value <= max_value
        return value

    return validate


def parse_args():
    """Parse args."""
    parser = ArgumentParser(description="CHIME")

    parser.add_argument("--file", type=open, action=FromFile)
    parser.add_argument(
        "--prefix", type=str, default=datetime.now().strftime("%Y.%m.%d.%H.%M."),
    )

    for arg, cast, min_value, max_value, help in (
        (
            "--current-hospitalized",
            int,
            0,
            None,
            "Currently Hospitalized COVID-19 Patients (>= 0)",
        ),
        (
            "--doubling-time",
            float,
            0.0,
            None,
            "Doubling time before social distancing (days)",
        ),
        ("--hospitalized-los", int, 0, None, "Hospitalized Length of Stay (days)"),
        (
            "--hospitalized-rate",
            float,
            0.00001,
            1.0,
            "Hospitalized Rate: 0.00001 - 1.0",
        ),
        ("--icu-los", int, 0, None, "ICU Length of Stay (days)"),
        ("--icu-rate", float, 0.0, 1.0, "ICU Rate: 0.0 - 1.0"),
        (
            "--known-infected",
            int,
            0,
            None,
            "Currently Known Regional Infections (>=0) (only used to compute detection rate - does not change projections)",
        ),
        (
            "--market_share",
            float,
            0.00001,
            1.0,
            "Hospital Market Share (0.00001 - 1.0)",
        ),
        ("--n-days", int, 0, None, "Nuber of days to project >= 0"),
        (
            "--relative-contact-rate",
            float,
            0.0,
            1.0,
            "Social Distancing Reduction Rate: 0.0 - 1.0",
        ),
        ("--susceptible", int, 1, None, "Regional Population >= 1"),
        ("--ventilated-los", int, 0, None, "Ventilated Length of Stay (days)"),
        ("--ventilated-rate", float, 0.0, 1.0, "Ventilated Rate: 0.0 - 1.0"),
    ):
        parser.add_argument(arg, type=validator(cast, min_value, max_value))
    return parser.parse_args()


def main():
    """Main."""
    a = parse_args()

    p = Parameters(
        current_hospitalized=a.current_hospitalized,
        doubling_time=a.doubling_time,
        known_infected=a.known_infected,
        market_share=a.market_share,
        n_days=a.n_days,
        relative_contact_rate=a.relative_contact_rate,
        susceptible=a.susceptible,

        hospitalized=RateLos(a.hospitalized_rate, a.hospitalized_los),
        icu=RateLos(a.icu_rate, a.icu_los),
        ventilated=RateLos(a.ventilated_rate, a.ventilated_los),
    )

    m = SimSirModel(p)

    prefix = a.prefix
    for df, name in (
        (m.raw_df, "raw"),
        (m.admits_df, "admits"),
        (m.census_df, "census"),
    ):
        df.to_csv(prefix + name + ".csv")


if __name__ == "__main__":
    main()
