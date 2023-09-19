""" Creates an header Div at the beginning of the app layout.

 Functions:
 ----------

    render(app: Dash) -> html.Div
 """

from dash import Dash, html


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

    return html.Div(
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
                "DASH - EARTHQUAKE DATA APP",
                style={"color": "SteelBlue"},
            ),
        ],
    )
