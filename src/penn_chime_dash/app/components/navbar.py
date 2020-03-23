# components/navbar.py
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from ..config import Config

cfg = Config()

navbar = dbc.NavbarSimple(
    brand='Penn Med CHIME', # Browser window title
    brand_href='/',         # index page
    children=[

        html.Link(
            key='penn-med-header',
            rel="stylesheet",
            href=cfg.PENN_HEADER,
        ),

        dbc.NavItem(
            dcc.Link(
                'Model',
                href='/CHIME',
                className='nav-link'
            )
        ),

        dbc.NavItem(
            dcc.Link(
                'Contribute',
                href='https://codeforphilly.github.io/chime/',
                className='nav-link'
            )
        ),

        dbc.NavItem(
            dcc.Link(
                'Resources',
                href='/resources',
                className='nav-link'
            )
        ),

        dbc.NavItem(
                    dcc.Link(
                        'Contact',
                        href=cfg.PENN_MED_URL,
                        className='nav-link'
                    )
                ),
    ],

    sticky='top',
    color='primary',
    light=True,
    dark=False
)
