""" Creates a html.Div in the app layout for the graph plot.

Creates and renders a html.Div in the app layout that will contain the graph plot selected.

Functions:
----------

    render(app: Dash) -> html.Div
"""

from dash import Dash, html, dcc
from . import graph_plot


def render(app: Dash) -> html.Div:
    """Renders graph-plot component.

    Renders the graph-plot component in a dcc.Loading (spinner) component which is returned inside a html.Div.

    Parameters:
    ----------
    app : Dash
        A dash object

    Returns:
    -------
    html.Div : html.Div
        An html.Div component containing a dcc.Loading and the graph-plot components.

    Functions:
    ---------
    Calls graph_plot.render(app) function to render the actual graph-plot.

    """
    return html.Div(
        children=[
            dcc.Loading(
                id="loading",
                children=[
                    html.Div(
                        graph_plot.render(app),
                    )
                ],
                type="default",
            )
        ],
        style={"align-self": "center"},
    )
