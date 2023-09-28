""" Creates an event map (map-graph) component in the app layout.

 Functions
 ---------
    render() -> html.Div
 """

from datetime import date
from dash import Dash, html, dcc, Input, Output
from geopandas import GeoDataFrame

from .map_graph_plot import plot_map_graph


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

    @app.callback(
        Output("map-graph", "children"),
        Input("my-date-picker-range", "start_date"),
        Input("my-date-picker-range", "end_date"),
        Input("min-mag-input", "value"),
        Input("max-mag-input", "value"),
    )
    def update_map_graph(
        start_date: str, end_date: str, min_mag: int, max_mag: int
    ) -> html.Div:
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

        geo_dff = data[
            (data["Event_Date"] >= date.fromisoformat(start_date))
            & (data["Event_Date"] <= date.fromisoformat(end_date))
            & (data["Mag"] >= min_mag)
            & (data["Mag"] <= max_mag)
        ]

        fig = plot_map_graph(geo_dff)

        return html.Div(
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

    return html.Div(id="map-graph")
