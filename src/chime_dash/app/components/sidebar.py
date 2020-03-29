"""components/sidebar
Initializes the side bar containing the various inputs for the model

#! _INPUTS should be considered for moving else where
"""
import dash_html_components as dhc

from typing import List, Dict, Any, Tuple
from collections import OrderedDict

from dash.dependencies import Input as CallbackInput, Output
from dash.development.base_component import ComponentMeta
from dash_html_components import Br

from penn_chime.defaults import RateLos
from penn_chime.parameters import Parameters

from chime_dash.app.components.base import Component
from chime_dash.app.utils.templates import create_switch_input, create_number_input, create_header, create_button, \
    create_link

FLOAT_INPUT_MIN = 0.001
FLOAT_INPUT_STEP = "any"

_INPUTS = OrderedDict(
    regional_parameters={"type": "header", "size": "h3"},
    market_share={"type": "number", "min": FLOAT_INPUT_MIN, "step": FLOAT_INPUT_STEP, "max": 100.0, "percent": True},
    susceptible={"type": "number", "min": 1, "step": 1},
    known_infected={"type": "number", "min": 0, "step": 1},
    current_hospitalized={"type": "number", "min": 0, "step": 1},
    spread_and_contact={"type": "header", "size": "h3"},
    doubling_time={"type": "number", "min": FLOAT_INPUT_MIN, "step": FLOAT_INPUT_STEP},
    relative_contact_rate={
        "type": "number",
        "min": 0.0,
        "step": FLOAT_INPUT_STEP,
        "max": 100.0,
        "percent": True,
    },
    severity_parameters={"type": "header", "size": "h3"},
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
        "percent": True
    },
    ventilated_rate={
        "type": "number",
        "min": 0.0,
        "step": FLOAT_INPUT_STEP,
        "max": 100.0,
        "percent": True,
    },
    hospitalized_los={"type": "number", "min": 0, "step": 1},
    icu_los={"type": "number", "min": 0, "step": 1},
    ventilated_los={"type": "number", "min": 0, "step": 1},
    display_parameters={"type": "header", "size": "h3"},
    n_days={"type": "number", "min": 30, "step": 1},
    max_y_axis_value={"type": "number", "min": 10, "step": 10, "value": None},
    as_date={"type": "switch", "value": False},
    show_tables={"type": "switch", "value": False},
    show_tool_details={"type": "switch", "value": False},
    show_additional_projections={"type": "switch", "value": False},
    save_as_pdf={"type": "button", "property": "n_clicks"},
    pdf_file_link={"type": "link", "property": "href"}
)


class Sidebar(Component):
    """Sidebar to the left of the screen
    contains the various inputs used to interact
    with the model.
    """
    # localization temp. for widget descriptions
    localization_file = "sidebar.yml"

    callback_inputs = OrderedDict(
        (key, CallbackInput(component_id=key, component_property=_INPUTS[key].get("property", "value")))
        for key in _INPUTS if _INPUTS[key]["type"] not in ("header", "link")
    )

    callback_outputs = [Output(component_id='pdf_file_link', component_property='href'),
                        Output(component_id='pdf_file_link', component_property='children')]

    def __init__(self, *args, **kwargs):
        self._save_to_pdf = False
        self.pdf_button_clicks = 0
        super().__init__(*args, **kwargs)

    @staticmethod
    def parse_form_parameters(**kwargs) -> Tuple[Parameters, Dict[str, Any]]:
        """Reads html form outputs and converts them to a parameter instance

        Returns Parameters and as_date argument
        """
        pars = Parameters(
            current_hospitalized=kwargs["current_hospitalized"],
            doubling_time=kwargs["doubling_time"],
            known_infected=kwargs["known_infected"],
            market_share=kwargs["market_share"] / 100,
            relative_contact_rate=kwargs["relative_contact_rate"] / 100,
            susceptible=kwargs["susceptible"],
            hospitalized=RateLos(
                kwargs["hospitalized_rate"] / 100, kwargs["hospitalized_los"]
            ),
            icu=RateLos(kwargs["icu_rate"] / 100, kwargs["icu_los"]),
            ventilated=RateLos(
                kwargs["ventilated_rate"] / 100, kwargs["ventilated_los"]
            ),
            max_y_axis=kwargs["max_y_axis_value"],
            n_days=kwargs["n_days"],
        )
        return pars

    def get_html(self) -> List[ComponentMeta]:
        """Initializes the view
        """
        elements = []
        for idx, data in _INPUTS.items():
            if data["type"] == "number":
                element = create_number_input(idx, data, self.content, self.defaults)
            elif data["type"] == "switch":
                element = create_switch_input(idx, data, self.content)
            elif data["type"] == "header":
                element = create_header(idx, self.content)
            elif data["type"] == "button":
                element = create_button(idx, self.content)
            elif data["type"] == "link":
                elements.append(Br())
                element = create_link(idx)
            else:
                raise ValueError(
                    "Failed to parse input '{idx}' with data '{data}'".format(
                        idx=idx, data=data
                    )
                )
            elements.append(element)

        sidebar = dhc.Nav(
            children=dhc.Div(
                children=elements,
                className="p-4",
                style={
                    "height": "calc(100vh - 48px)",
                    "overflowY": "auto",
                },
            ),
            className="col-md-3",
            style={
                "position": "fixed",
                "top": "48px",
                "bottom": 0,
                "left": 0,
                "zIndex": 100,
                "boxShadow": "inset -1px 0 0 rgba(0, 0, 0, .1)"
            }
        )

        return [sidebar]

    def save_to_pdf(self, kwargs):
        """
        Return status of save to pdf flag and set it off.
        """
        if kwargs.get('save_as_pdf', 0) and kwargs.get('save_as_pdf', 0) > self.pdf_button_clicks:
            self.pdf_button_clicks = kwargs.get('save_as_pdf', '0')
            return True
        return False

    def callback(  # pylint: disable=W0613, R0201
        self, *args, **kwargs
    ) -> List[Dict[str, Any]]:
        return [kwargs.get('pdf_url', ''),
                self.content['download_report'] if kwargs.get('pdf_url', None) else None]
