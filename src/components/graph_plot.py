""" Creates a graph (graph-plot) component in the app layout.

Functions
---------

    render(app: Dash) -> html.Div
"""

from dash import Dash, html, Input, Output

from src.graph_plot_functions.graph_functions import (
    display_response_time_plot,
    display_intensity_dist_plot,
    display_dyfi_responses_tbl,
    display_zip_plot,
    display_intensity_plot_1km,
    display_intensity_plot_10km,
)

dropdown_disabled = True
dropdown_not_disabled = False


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

    @app.callback(
        Output("graph-plot", "children"),
        Output("plot-type-dropdown", "disabled"),
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

        # print(selected_data)
        if selected_data is None:
            return (
                html.Div(
                    children=[
                        html.P(
                            """Filter events displayed by using the date and magnitude filters."""
                        ),
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
                dropdown_not_disabled,
            )
        else:
            event_id = selected_data["points"][0]["customdata"][8]

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
                    dropdown_disabled,
                )
            elif plot_type == "Intensity Plot(1km)":
                return (
                    display_intensity_plot_1km(event_id, selected_data),
                    dropdown_not_disabled,
                )
            elif plot_type == "Intensity Plot(10km)":
                return (
                    display_intensity_plot_10km(event_id, selected_data),
                    dropdown_not_disabled,
                )
            elif plot_type == "Zip Map":
                return (
                    display_zip_plot(event_id, selected_data),
                    dropdown_not_disabled,
                )
            elif plot_type == "Intensity Vs. Distance":
                return display_intensity_dist_plot(event_id), dropdown_not_disabled
            elif plot_type == "Response Vs. Time":
                return display_response_time_plot(event_id), dropdown_not_disabled
            elif plot_type == "DYFI Responses":
                return display_dyfi_responses_tbl(event_id), dropdown_not_disabled

    return html.Div(id="graph-plot")