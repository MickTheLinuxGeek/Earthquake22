""" Creates an event map (map-graph) component in the app layout.

 Functions
 ---------
    render() -> html.Div
 """

import logging
from datetime import date
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from geopandas import GeoDataFrame

from .map_graph_plot import plot_map_graph

logger = logging.getLogger(__name__)


def render(app: Dash, data: GeoDataFrame) -> html.Div:
    """Renders a map with plotted earthquake events.

    Render function for event map (map-graph) component.  It defines a dash callback and callback function
    (update_map_graph) which updates the event map based on the filtered data from the callback.

    Parameters:
    ----------
    app : Dash
        A dash object

    data : geopandas.GeoDataFrame
        A GeoDataFrame containing the earthquake event data

    Returns:
    -------
    html.Div : html.Div(id="map-graph")
        A Div containing the map-graph component
    """

    logger.info(f"Entered event_map.render() function.")

    @app.callback(
        Output("map-graph", "children"),
        Input("my-date-picker-range", "start_date"),
        Input("my-date-picker-range", "end_date"),
        Input("min-mag-input", "value"),
        Input("max-mag-input", "value"),
    )
    def update_map_graph(start_date: str, end_date: str, min_mag: int, max_mag: int) -> html.Div:
        """Map callback function

        Callback function that returns a map figure based on the date range and magnitude range inputs.

        Parameters:
        ----------
        start_date : datetime.datetime.date
            Start date of date range filter
        end_date : datetime.datetime.date
            End date of date range filter
        min_mag : int
            Minimum magnitude value for filter
        max_mag : int
            Maximum magnitude value for filter

        Returns:
        -------
        html.Div
            A Div that contains a dcc.Graph component with the plotly.graph_objects.Figure
            fig -- The Plotly Express scatter mapbox map figure object

        Function Calls:
        --------------
        plot_map_graph(geo_dff)
            This function is called with the geo_dff, which is the filtered data, to create the actual map figure.
        """

        logger.info(f"Entered update_map_graph() dash callback function.")

        try:
            geo_dff = data[
                (data["Event_Date"] >= date.fromisoformat(start_date))
                & (data["Event_Date"] <= date.fromisoformat(end_date))
                & (data["Mag"] >= min_mag)
                & (data["Mag"] <= max_mag)
            ]

            logger.debug(f"Filtered GeoDataFrame, geo_dff based on event date and magnitude.  \n{geo_dff}")

            fig = plot_map_graph(geo_dff)

            event_map_div = html.Div(
                dcc.Graph(
                    id="dcc-map-graph",
                    figure=fig,
                    config={
                        "scrollZoom": True,
                        "responsive": True,
                        "modeBarButtonsToRemove": [
                            "zoom",
                            "pan",
                            "select",
                            "lasso2d",
                            "toImage",
                        ],
                    },
                    style={
                        "padding-bottom": "2px",
                        "padding-top": "4px",
                        "padding-left": "2px",
                        "padding-right": "2px",
                        "height": "45vh",
                        "width": "100%",
                    },
                ),
                id="map-graph",
            )
            logger.debug(f"Event map html.Div with map figure based on filtered GeoDataFrame.  \n{event_map_div}")
            logger.info(f"Returned from update_map_graph() dash callback function.")
            return event_map_div
        except (FileNotFoundError, IOError, OSError, PermissionError) as err:
            print(f"event_map.py:  Event map could not be updated!  {err}")
            logger.critical(f"Event map could not be updated/rendered.  {err}")
            return html.Div(
                dbc.Alert(
                    children=[
                        html.H4("Application Data Files Not Found!", className="alert-heading mt-0"),
                        html.P(f"{err}"),
                        html.Hr(),
                        html.P("Mapbox API access token is missing!"),
                        html.P(
                            "Check App error log and consult installation section of the README.md.", className="mb-0"
                        ),
                    ],
                    color="danger",
                ),
                style={"text-align": "center"},
            )

    logger.info(f"Returned from event_map.render() function.")
    return html.Div(id="map-graph")
