from pytest import fixture
from selenium.webdriver.chrome.options import Options

from dash_app import DASH


def pytest_setup_options():
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")

    return options


@fixture
def test_app(dash_duo):

    dash_duo.start_server(DASH)

    yield dash_duo
