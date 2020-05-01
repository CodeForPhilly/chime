"""Command line interface."""

import os
import sys

from .model.parameters import Parameters
from .model.sir import Sir


def run(argv):
    """Eun cli."""
    p = Parameters.create(os.environ, argv[1:])
    m = Sir(p)

    for df, name in (
        (m.sim_sir_w_date_df, "sim_sir_w_date"),
        (m.admits_df, "projected_admits"),
        (m.census_df, "projected_census"),
        (m.ppe_df, 'ppe_data')
    ):
        df.to_csv(f"{p.current_date}_{name}.csv")


def main():
    """Main."""
    run(sys.argv)
