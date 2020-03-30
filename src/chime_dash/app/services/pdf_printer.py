"""Utilities for exporting dash app to pdf
"""
import json
import base64

from time import sleep

from io import BytesIO

from dash import Dash
from dash.testing.application_runners import ThreadedRunner
from dash.testing.composite import DashComposite
from dash_bootstrap_components.themes import BOOTSTRAP
import dash_bootstrap_components as dbc

from selenium import webdriver


def send_devtools(driver, cmd, params=None):
    params = params or None
    resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    url = driver.command_executor._url + resource
    body = json.dumps({"cmd": cmd, "params": params})
    response = driver.command_executor._request("POST", url, body)
    if response.get("status", False):
        raise Exception(response.get("value"))
    return response.get("value")


def save_as_pdf(driver, options=None):
    """Saves pdf to buffer object
    """
    options = options or {}
    # https://timvdlippe.github.io/devtools-protocol/tot/Page#method-printToPDF
    result = send_devtools(driver, "Page.printToPDF", options)

    cached_file = BytesIO()
    cached_file.write(base64.b64decode(result["data"]))
    cached_file.seek(0)
    return cached_file


def print_to_pdf(component, kwargs):
    """Extracts content and prints pdf to buffer object.
    """
    app = Dash(
        __name__,
        external_stylesheets=[
            "https://www1.pennmedicine.org/styles/shared/penn-medicine-header.css",
            BOOTSTRAP,
        ],
    )

    component.components['sidebar'].html[0].hidden = True

    app.layout = dbc.Container(children=component.html, fluid=True)
    app.title = "CHIME Printer"

    outputs = component.callback(**kwargs)

    @app.callback(component.callback_outputs, list(component.callback_inputs.values()))
    def callback(*args):  # pylint: disable=W0612, W0613
        return outputs

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")

    with ThreadedRunner() as starter:
        with DashComposite(starter, browser="Chrome", options=[chrome_options]) as dc:
            dc.start_server(app, port=8051)
            while "Loading..." in dc.driver.page_source:
                sleep(1)
            pdf = save_as_pdf(dc.driver, {"landscape": False})
            dc.driver.quit()

    return pdf
