""" Creates the Dash app's page layout.

Creates the Dash app's html page layout.  The Layout is a dbc.Container/Row/Col component structure.  All the custom
component render functions are called within the layout.

Functions:
----------

    create_layout(app: Dash, data: GeoDataFrame) -> html.Div
"""

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from geopandas import GeoDataFrame

from . import (
    event_date_picker_range,
    magnitude_range_picker,
    event_map,
    plot_type_dropdown,
    graph_plot_div,
    header,
)


def create_layout(app: Dash, data: GeoDataFrame) -> html.Div:
    """Function to create app html page layout.

    This function creates and returns the app html page.  The page layout is a dbc.Container/Row/Col component structure
    contained inside an html.Div.

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
    The following component render function are called within the layout:

        event_date_picker_range,
        magnitude_range_picker,
        event_map,
        plot_type_dropdown,
        graph_plot_div,
        header
    """

    return html.Div(
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
                            xs=11,
                            sm=8,
                            md=6,
                            lg=2,
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
                            lg=2,
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
                            sm=8,
                            md=12,
                            lg=10,
                            xl={"offset": 4, "size": 8},
                        )
                    ]
                ),
                # This section needs a better looking style
                # Row for Links and Information
                dbc.Row(
                    style={"margin-top": "12px", "margin-bottom": "10px"},
                    children=[
                        dbc.Col(
                            width=12,
                            children=[
                                dbc.Row(
                                    children=[
                                        dbc.Col(
                                            width={"size": 10, "offset": 2},
                                            children=[
                                                html.P("Data Provided By"),
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
                                        ),
                                        dbc.Col(
                                            width={"size": 10, "offset": 2},
                                            children=[
                                                html.P("Contact"),
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
                                        ),
                                    ]
                                )
                            ],
                            xs=12,
                            sm=8,
                            md=12,
                            lg=10,
                            xl=8,
                        )
                    ],
                ),
            ],
            fluid=True,
        )
    )
