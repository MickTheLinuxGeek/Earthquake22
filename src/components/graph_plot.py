""" Creates a graph (graph-plot) component in the app layout.

Functions
---------

    render(app: Dash) -> html.Div
"""

import logging
from dash import Dash, html, Input, Output
import dash_bootstrap_components as dbc
from pyogrio.errors import DataSourceError

from ..graph_plot_functions.graph_functions import (
    display_response_time_plot,
    display_intensity_dist_plot,
    display_dyfi_responses_tbl,
    display_zip_plot,
    display_intensity_plot_1km,
    display_intensity_plot_10km,
)

DROPDOWN_DISABLED = True
DROPDOWN_NOT_DISABLED = False
DEFAULT_PLOT_TYPE = "Intensity Plot(10km)"

logger = logging.getLogger(__name__)


def render(app: Dash) -> html.Div:
    """Render the graph-plot component

    Renders the graph-plot component in the app layout by using a Dash callback and callback function.

    Parameters:
    ----------
    app : Dash
        A dash object

    Returns:
    -------
    html.Div : html.Div(id="graph-plot")
        An html.Div that contains the graph-plot from the app callback.
    """

    logger.info(f"Entered graph_plot.render() function.")

    @app.callback(
        Output("graph-plot", "children"),
        Output("plot-type-dropdown", "disabled"),
        Output("plot-type-dropdown", "value"),
        Input("dcc-map-graph", "selectedData"),
        Input("plot-type-dropdown", "value"),
        prevent_initial_call=True,
    )
    def plot_graphs(selected_data: dict, plot_type: str) -> (html.Div, bool):
        """graph-plot callback function

        Callback function that returns and displays the graph plot that is selected.

        Parameters:
        ----------
        selected_data : Python dictionary
            A Python dictionary containing the event data of the selected point on the map.
        plot_type : string
            A string representing the graph plot type selected from the dropdown.

        Returns:
        -------
        html.Div
            Contains a html.P with a text message if the selected_data is None or the felt responses is zero or
            html.Div which was returned from one of the graph-plot functions.
        A boolean
            Indicating whether the plot-type-dropdown is disabled or not.

        Functions:
        ---------
        The following functions are called based on the plot_type from the plot-type-dropdown and the selected_data from
        the dcc-map-graph (events map) component:

            display_intensity_plot_1km(event_id, selected_data)
            display_intensity_plot_10km(event_id, selected_data)
            display_zip_plot(event_id, selected_data)
            display_intensity_dist_plot(event_id)
            display_response_time_plot(event_id)
            display_dyfi_responses_tbl(event_id)
        """

        logger.info(f"Entered plot_graphs() dash callback function.")

        try:
            if selected_data is None:
                return (
                    html.Div(
                        children=[
                            html.P("""Filter events displayed by using the date and magnitude filters."""),
                            html.P(
                                """Select an event marker from the map and a plot type from the
                                                 dropdown for more event information."""
                            ),
                        ],
                        style={
                            "text-align": "center",
                            "margin": "10px 0",
                            "padding": "5px",
                            "border": "1px solid #999",
                            "display": "flex",
                            "flex-direction": "column",
                            "width": "100%",
                        },
                        className="center",
                    ),
                    DROPDOWN_DISABLED,
                    DEFAULT_PLOT_TYPE,
                )
            event_id = selected_data["points"][0]["customdata"][8]

            logger.debug(f"Event id selected:  {event_id}")
            logger.debug(f"Number of DYFI responses:  {selected_data['points'][0]['customdata'][6]}")

            # if DYFI felt is zero
            if selected_data["points"][0]["customdata"][6] == 0:
                return (
                    html.Div(
                        html.P("""Event has no reported DYFI information."""),
                        style={
                            "text-align": "center",
                            "margin": "10px 0",
                            "padding": "5px",
                            "border": "1px solid #999",
                            "display": "flex",
                            "flex-direction": "column",
                        },
                        className="center",
                    ),
                    DROPDOWN_DISABLED,
                    plot_type,
                )
            graph_result = None

            logger.debug(f"Plot type:  {plot_type}")
            logger.debug(f"Event id:  {event_id}")
            logger.debug(f"Selected data:  {selected_data}")

            if plot_type == "Intensity Plot(1km)":
                graph_result = display_intensity_plot_1km(event_id, selected_data)

            if plot_type == "Intensity Plot(10km)":
                graph_result = display_intensity_plot_10km(event_id, selected_data)

            if plot_type == "Zip Map":
                graph_result = display_zip_plot(event_id, selected_data)

            if plot_type == "Intensity Vs. Distance":
                graph_result = display_intensity_dist_plot(event_id)

            if plot_type == "Response Vs. Time":
                graph_result = display_response_time_plot(event_id)

            if plot_type == "DYFI Responses":
                graph_result = display_dyfi_responses_tbl(event_id)

            return graph_result, DROPDOWN_NOT_DISABLED, plot_type
        except (FileNotFoundError, IOError, OSError, PermissionError, DataSourceError) as err:
            print(f"graph_plot.py:  Application data files missing!  Check App error log.  {err}")
            logger.critical(f"Application data missing!  Check App error log.  {err}")
            # plot_graphs() return
            return (
                html.Div(
                    dbc.Alert(
                        children=[
                            html.H4("Application Data Files Not Found!", className="alert-heading mt-0"),
                            html.P(f"{err}"),
                            html.Hr(),
                            html.P("Application data files are missing.  Check App error log."),
                            html.P("May need to run usgs_api.py to download data files.", className="mb-0"),
                        ],
                        color="danger",
                    ),
                    style={"text-align": "center"},
                ),
                DROPDOWN_NOT_DISABLED,
            )

    # render() return
    logger.info(f"Returned from graph_plot.render() function.")
    return html.Div(id="graph-plot")
