import dash_bootstrap_components as dbc
import dash_html_components as html
from ..config import Config

cfg = Config()

footer = dbc.Container(
    dbc.Row(
        dbc.Col(
            html.P(
                [
                    html.Span('', className='mr-2'),
                    # email - used the one from the contact page as a placeholder for now
                    html.A(html.I(className='fas fa-envelope-square mr-1'),
                           href='pennsignals@uphs.upenn.edu'),
                    # github
                    html.A(html.I(className='fab fa-github-square mr-1'),
                           href=cfg.GITHUB_URL),
                    # phone from the contact site as well
                    html.A(html.I(className='nf-fa-phone'),
                           href='tel:267-332-1948'),
                    # template incase you think of anything else or take pity
                    html.A(html.I(className='fab fa-twitter-square mr-1'),
                           href=''),
                ],
                className='lead'
            )
        )
    )
)
