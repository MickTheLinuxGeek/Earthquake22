""" Creates an header Div at the beginning of the app layout.

 Functions:
 ----------

    render(app: Dash) -> html.Div
 """

import logging
from dash import Dash, html

logger = logging.getLogger(__name__)


def render(app: Dash) -> html.Div:
    """Render a header Div for the app page.

    Parameters:
    -----------
    app : Dash
        A Dash object

    Returns:
    --------
    html.Div:
        A header Div containing the Plotly logo, Plotly url link, and app title.
    """

    logger.info("Entered header.render() function.")

    header_div = html.Div(
        className="div-user-controls",
        children=[
            html.A(
                html.Img(
                    className="logo",
                    src=app.get_asset_url("dash-logo-new.png"),
                ),
                href="https://plotly.com/dash/",
            ),
            html.H3(
                # "DASH - EARTHQUAKE DATA APP",
                "EARTHQUAKE DATA EXPLORER",
                style={"color": "SteelBlue"},
            ),
        ],
    )
    logger.debug("html.Div structure of app page header:\n %s", header_div)
    logger.info("Exited header.render() function.")

    return header_div
