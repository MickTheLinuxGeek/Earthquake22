""" Creates a dcc.Dropdown component used to select the plot type to display.

 Functions:
 ----------

    render() -> html.Div
 """

from dash import html, dcc


def render() -> html.Div:
    """Render a dcc.Dropdown with the plot type options in the app layout.

    Returns:
    --------

        html.Div:  Contains a html.Label and dcc.Dropdown components.
    """

    return html.Div(
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
