"""Command line interface."""

import os
import sys

from .model.parameters import Parameters
from .model.sir import Sir


def main():
    """Main."""
    p = Parameters.create(os.environ, sys.argv[1:])
    m = Sir(p)

    for df, name in (
        (m.sim_sir_w_date_df, "sim_sir_w_date"),
        (m.admits_df, "projected_admits"),
        (m.census_df, "projected_census"),
    ):
        df.to_csv(f"{p.current_date}_{name}.csv")
