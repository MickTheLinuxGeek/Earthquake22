""" Creates a footer Div at the end of the app layout.

 Functions:
 ----------

    render() -> dbc.Row
 """

import logging
from dash import html, dcc
import dash_bootstrap_components as dbc

logger = logging.getLogger(__name__)


def render() -> dbc.Row:
    """Render a footer for the app page.

    Returns:
    --------
    dbc.Row :
        A footer dbc.Row component containing links and contact information.
    """

    logger.info("Entered footer.render() function.")

    app_footer = dbc.Row(
        style={"margin-top": "12px", "margin-bottom": "10px"},
        children=[
            dbc.Col(
                children=[
                    dbc.Row(
                        children=[
                            dbc.Col(
                                children=[
                                    html.Label("Data Provided By"),
                                    html.Div(
                                        children=[
                                            dcc.Link(
                                                "U.S. Geological Survey - USAGov",
                                                href="https://www.usgs.gov/earthquake",
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        children=[
                                            dcc.Link(
                                                "U.S. Census Bureau",
                                                href="https://www.census.gov/",
                                            )
                                        ]
                                    ),
                                ],
                                xs=12,
                                sm=4,
                                md=4,
                                lg=4,
                                xl=4,
                            ),
                            dbc.Col(
                                children=[
                                    html.Label("Contact"),
                                    html.Div(
                                        children=[
                                            dcc.Link(
                                                "mick.the.linux.geek@hotmail.com",
                                                href="mailto:mick.the.linuk.geek@hotmail.com",
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        children=[
                                            dcc.Link(
                                                "Mastodon",
                                                href="https://mastodon.online/@mickthelinuxgeek",
                                            )
                                        ]
                                    ),
                                ],
                                xs=12,
                                sm=4,
                                md=4,
                                lg=4,
                                xl=4,
                            ),
                        ]
                    )
                ],
            ),
        ],
    )

    logger.debug("Page footer structure.\n %s", app_footer)
    logger.info("Exited footer.render() function.")

    return app_footer
