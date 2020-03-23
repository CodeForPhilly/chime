"""Initializes the  dash html
"""
from typing import List, Any, Dict

from pandas import DataFrame

from dash.dependencies import Output
from dash.development.base_component import ComponentMeta
from dash_html_components import H4, Div
from dash_core_components import Graph
from dash_bootstrap_components import Table

from penn_chime.utils import add_date_column
from penn_chime.parameters import Parameters

from chime_dash.utils import read_localization_yaml, df_to_html_table
from chime_dash.plotting import plot_dataframe


LOCALIZATION_FILE = "additions.yml"


def setup(language: str) -> List[ComponentMeta]:
    """Initializes the header dash html
    """
    return [Div(id="additions")]


CALLBACK_OUTPUTS = [Output(component_id="additions", component_property="children")]


def render(
    language: str,
    pars: Parameters,
    as_date: bool = False,
    show_tables: bool = False,
    show_additions: bool = False,
) -> List[Any]:
    """Renders the parameter dependent plots and tables
    """
    if show_additions:
        content = read_localization_yaml(LOCALIZATION_FILE, language)
        title = content["infected-v-revovered-title"]

        time_evolution = _build_frame(pars, content, as_date)

        time_evolution_data = plot_dataframe(
            time_evolution.drop(columns=content["susceptible"]),
            max_y_axis=pars.max_y_axis,
        )

        children = [
            H4(title, id="infected-v-revovered-title"),
            Graph(figure=time_evolution_data, id="infected-v-revovered-graph"),
        ]

        if show_tables:
            if as_date:
                time_evolution.index = time_evolution.index.strftime("%b, %d")
            time_evolution_table_data = (
                df_to_html_table(time_evolution, data_only=True, n_mod=7)
                if show_tables
                else {}
            )
            children.append(
                Table(time_evolution_table_data, id="infected-v-revovered-table")
            )

    else:
        children = []

    return (children,)


def _build_frame(pars: Parameters, content: Dict[str, str], as_date: bool = False):

    # Prepare admissions data & census data
    time_evolution = DataFrame(
        {
            "susceptible": pars.susceptible_v,
            "infected": pars.infected_v,
            "recovered": pars.recovered_v,
        }
    )
    time_evolution["day"] = time_evolution.index

    # Convert columns
    if as_date:
        time_evolution = add_date_column(
            time_evolution, drop_day_column=True
        ).set_index("date")
    else:
        time_evolution = time_evolution.set_index("day")

    return time_evolution.rename(
        columns={key: content[key] for key in time_evolution.columns}
    ).astype(int)
