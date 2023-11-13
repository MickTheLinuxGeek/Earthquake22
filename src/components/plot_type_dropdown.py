""" Creates a dcc.Dropdown component used to select the plot type to display.

 Functions:
 ----------

    render() -> html.Div
 """

import logging
from dash import html, dcc

logger = logging.getLogger(__name__)


def render() -> html.Div:
    """Render a dcc.Dropdown with the plot type options in the app layout.

    Returns:
    --------

        html.Div:  Contains a html.Label and dcc.Dropdown components.
    """

    logger.info("Entered plot_type_dropdown.render() function.")

    plot_type_drop = html.Div(
        children=[
            html.Label("Plot Type"),
            dcc.Dropdown(
                id="plot-type-dropdown",
                options=[
                    "Intensity Plot(1km)",
                    "Intensity Plot(10km)",
                    "Zip Map",
                    "Intensity Vs. Distance",
                    "Response Vs. Time",
                    "DYFI Responses",
                ],
                value="Intensity Plot(10km)",
                clearable=False,
                searchable=False,
                multi=False,
                disabled=False,
                style={"width": "77%"},
            ),
        ],
    )

    logger.info("Exited plot_type_dropdown.render() function.")

    return plot_type_drop
