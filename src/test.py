"""Navigation bar view
"""
from typing import List, Any
from chime_dash.app.components import header
from chime_dash.app.controllers import navbar
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.development.base_component import ComponentMeta


def setup(language: str) -> List[ComponentMeta]:
    """Initialize the navigation bar
    """
    nav = dbc.Navbar(
        dbc.Container(
        [
            html.A(
                dbc.Row(
                    children=[
                        dbc.Col(children=header.setup(language)),
                        dbc.Col(
                            dbc.NavbarBrand(
                                children='Penn Medicine CHIME',
                                href='/')
                        )
                    ]
                ),
                href='https://www.pennmedicine.org/'),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem(
                        "Penn Medicine",
                        header=True),
                    dbc.DropdownMenuItem(
                        "Predictive Healthcare",
                        href='http://predictivehealthcare.pennmedicine.org/',
                        external_link=True
                    ),
                    dbc.DropdownMenuItem(
                        "Contact Us",
                        href="http://predictivehealthcare.pennmedicine.org/contact/",
                        external_link=True
                    ),
                    dbc.DropdownMenuItem(
                        divider=True
                    ),
                    dbc.DropdownMenuItem(
                        "User Docs",
                        href="https://code-for-philly.gitbook.io/chime/",
                        external_link=True
                    ),
                    dbc.DropdownMenuItem("Contribute", header=True),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem(
                        "GitHub",
                        href="https://github.com/CodeForPhilly/chime",
                        external_link=True
                    ),
                    dbc.DropdownMenuItem(
                        "Slack",
                        href="https://codeforphilly.org/chat?channel=covid19-chime-penn"
                    )
                ],
                # nav=True,
                # in_navbar=True,
                # label="Learn More"
            )
        ]
    ))
    return nav

app = Dash(
    __name__,
)

app.layout = setup("en")

if __name__ == "__main__":
    app.run_server(debug=True)
