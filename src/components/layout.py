""" Creates the Dash app's page layout.

Creates the Dash app's html page layout.  The Layout is a dbc.Container/Row/Col component structure.  All the custom
component render functions are called within the layout.

Functions:
----------

    create_layout(app: Dash, data: GeoDataFrame) -> html.Div
"""

import logging
from dash import Dash, html
import dash_bootstrap_components as dbc
from geopandas import GeoDataFrame

from . import (
    event_date_picker_range,
    magnitude_range_picker,
    event_map,
    plot_type_dropdown,
    graph_plot_div,
    header,
    footer,
)

logger = logging.getLogger(__name__)


def create_layout(app: Dash, data: GeoDataFrame) -> html.Div:
    """Function to create app html page layout.

    This function creates and returns the app html page.  The page layout is a dbc.Container/Row/Col component structure
    contained inside a html.Div.

    Parameters:
    ----------
    app : Dash
        A dash object
    data : geopandas.GeoDataFrame
        A geopandas GeoDataFrame which contains the earthquake event data.

    Returns:
    -------
    html.Div : html.Div
        An html.Div that contains the entire app page layout structure.

    Functions:
    --------------
    The following component render functions are called within the layout:

        event_date_picker_range,
        magnitude_range_picker,
        event_map,
        plot_type_dropdown,
        graph_plot_div,
        header
    """

    logger.info("Entered create_layout() function; Created application html layout.")

    eq_layout = html.Div(
        dbc.Container(
            [
                dbc.Row(
                    children=[
                        # Column for user controls
                        dbc.Col(
                            children=[
                                html.Div(
                                    children=[
                                        header.render(app),
                                    ],
                                ),
                                html.Div(
                                    children=[
                                        event_date_picker_range.render(),
                                    ],
                                ),
                                html.Div(
                                    children=[
                                        magnitude_range_picker.render(),
                                    ],
                                ),
                                html.Div(children=[plot_type_dropdown.render()]),
                            ],
                            xs=12,
                            sm=8,
                            md=6,
                            lg=4,
                            xl=4,
                        ),
                        # Column for map-graph
                        dbc.Col(
                            html.Div(
                                children=[event_map.render(app, data)],
                            ),
                            xs=12,
                            sm=8,
                            md=6,
                            lg=8,
                            xl=8,
                        ),
                    ],
                ),
                # Row & Column for the graph-plot
                dbc.Row(
                    children=[
                        dbc.Col(
                            children=[
                                graph_plot_div.render(app),
                            ],
                            xs=12,
                            sm=12,
                            md=12,
                            lg=12,
                            xl={"offset": 4, "size": 8},
                        )
                    ]
                ),
                html.Div(
                    children=[footer.render()],
                ),
            ],
            fluid=True,
        )
    )

    logger.info("Exited create_layout() function; Created application html layout.")

    return eq_layout
