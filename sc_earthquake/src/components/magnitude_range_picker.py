""" Creates input fields for the min. and max magnitude events filter.

 Functions:
 ----------

    render() -> html.Div
 """


import logging
from dash import html
import dash_bootstrap_components as dbc

logger = logging.getLogger(__name__)


def render() -> html.Div:
    """Render min and max magnitude input fields in the app layout.

    Returns:
    --------

        html.Div:  Contains min-mag-input and max-mag-input fields for the magnitude_range_picker (this) component.
    """

    logger.info("Entered magnitude_range_picker.render() function.")

    mag_range_picker = html.Div(
        children=[
            dbc.Label("Min./Max. Magnitude Filter"),
            html.Div(
                children=[
                    dbc.Input(
                        id="min-mag-input",
                        type="number",
                        min=1,
                        max=10,
                        step=0.5,
                        size="md",
                        placeholder="Min.",
                        debounce=True,
                        value=1,
                        autofocus=True,
                        n_submit=0,
                        n_blur=0,
                        style={"width": "21.5%"},
                    ),
                    dbc.Input(
                        id="max-mag-input",
                        type="number",
                        min=1,
                        max=10,
                        step=0.5,
                        size="md",
                        placeholder="Max.",
                        debounce=True,
                        value=10,
                        n_submit=0,
                        n_blur=0,
                        style={"width": "21.5%"},
                    ),
                ],
                style={"display": "flex"},
            ),
        ],
    )

    logger.info("Exited magnitude_range_picker.render() function.")

    return mag_range_picker
