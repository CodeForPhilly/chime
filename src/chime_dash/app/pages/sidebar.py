"""components/sidebar
Initializes the side bar containing the various inputs for the model

#! _SIDEBAR_ELEMENTS should be considered for moving else where
"""
from typing import List
from collections import OrderedDict
from datetime import date, datetime

from dash.development.base_component import ComponentMeta
from dash_html_components import Nav, Div
from dash_core_components import Store

from chime_dash.app.components.base import Page
from chime_dash.app.utils import ReadOnlyDict
from chime_dash.app.utils.templates import (
    create_switch_input,
    create_number_input,
    create_date_input,
    create_header,
)
from chime_dash.app.services.callbacks import SidebarCallbacks

FLOAT_INPUT_MIN = 0.001
FLOAT_INPUT_STEP = "any"

_SIDEBAR_ELEMENTS = ReadOnlyDict(OrderedDict(
    ###
    hospital_parameters={"type": "header", "size": "h3"},
    population={"type": "number", "min": 1, "step": 1},
    market_share={
        "type": "number",
        "min": FLOAT_INPUT_MIN,
        "step": FLOAT_INPUT_STEP,
        "max": 100.0,
        "percent": True,
    },
    current_hospitalized={"type": "number", "min": 0, "step": 1},
    ###
    spread_parameters={"type": "header", "size": "h4"},
    date_first_hospitalized={
        "type": "date",
        "min_date_allowed": datetime(2019, 10, 1),
        "max_date_allowed": datetime(2021, 12, 31),
    },
    doubling_time={"type": "number", "min": FLOAT_INPUT_MIN, "step": FLOAT_INPUT_STEP},
    relative_contact_rate={
        "type": "number",
        "min": 0.0,
        "step": FLOAT_INPUT_STEP,
        "max": 100.0,
        "percent": True,
    },
    ###
    severity_parameters={"type": "header", "size": "h4"},
    hospitalized_rate={
        "type": "number",
        "min": 0.0,
        "step": FLOAT_INPUT_STEP,
        "max": 100.0,
        "percent": True,
    },
    icu_rate={
        "type": "number",
        "min": 0.0,
        "step": FLOAT_INPUT_STEP,
        "max": 100.0,
        "percent": True,
    },
    ventilated_rate={
        "type": "number",
        "min": 0.0,
        "step": FLOAT_INPUT_STEP,
        "max": 100.0,
        "percent": True,
    },
    infectious_days={"type": "number", "min": 0, "step": 1},
    hospitalized_los={"type": "number", "min": 0, "step": 1},
    icu_los={"type": "number", "min": 0, "step": 1},
    ventilated_los={"type": "number", "min": 0, "step": 1},
    ###
    display_parameters={"type": "header", "size": "h4"},
    n_days={"type": "number", "min": 30, "step": 1},
    current_date={
        "type": "date",
        "min_date_allowed": datetime(2019, 10, 1),
        "max_date_allowed": datetime(2021, 12, 31),
        "initial_visible_month": date.today(),
        "date": date.today(),
    },
    max_y_axis_value={"type": "number", "min": 10, "step": 10, "value": None},
    show_tables={"type": "switch", "value": False},
))


class Sidebar(Page):
    """Sidebar to the left of the screen
    contains the various inputs used to interact
    with the model.
    """
    callbacks_cls = SidebarCallbacks

    # localization temp. for widget descriptions
    localization_file = "sidebar.yml"
    # Different kind of inputs store different kind of "values"
    # This tells the callback output for which field to look
    input_type_map = ReadOnlyDict(OrderedDict(
        (key, value["type"])
        for key, value in _SIDEBAR_ELEMENTS.items()
        if value["type"] not in ("header",)
    ))
    input_value_map = ReadOnlyDict(OrderedDict(
        (key, {"number": "value", "date": "date"}.get(value, "value"))
        for key, value in input_type_map.items()
    ))

    def get_html(self) -> List[ComponentMeta]:
        """Initializes the view
        """
        elements = [
            Store(id="sidebar-store")
        ]
        for idx, data in _SIDEBAR_ELEMENTS.items():
            if data["type"] == "number":
                element = create_number_input(idx, data, self.content, self.defaults)
            elif data["type"] == "switch":
                element = create_switch_input(idx, data, self.content)
            elif data["type"] == "date":
                element = create_date_input(idx, data, self.content, self.defaults)
            elif data["type"] == "header":
                element = create_header(idx, self.content)
            else:
                raise ValueError(
                    "Failed to parse input '{idx}' with data '{data}'".format(
                        idx=idx, data=data
                    )
                )
            elements.append(element)

        sidebar = Nav(
            className="bg-light border-right",
            children=Div(
                children=elements,
                className="px-3 pb-5",
            ),
            style={
                "bottom": 0,
                "left": 0,
                "overflowY": "scroll",
                "position": "fixed",
                "top": "56px",
                "width": "320px",
                "zIndex": 1,
            },
        )

        return [sidebar]
