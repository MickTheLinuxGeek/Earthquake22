""" Creates a dcc.DatePickerRange component to provide a start and end date filter for selecting earthquake events.

 Functions:
 ----------

    render() -> html.Div
 """

from datetime import date, datetime as dt
from dash import html, dcc
import dash_bootstrap_components as dbc

import logging

logger = logging.getLogger(__name__)


def render() -> html.Div:
    """Render date range picker component in the app layout.

    Returns:
    --------

        html.Div:  Contains a dbc.Label and a dcc.DatePickerRange component that contains the filter start & end dates.
    """

    logger.info(f"Entered event_date_picker_range.render() function.")

    date_picker_comp = html.Div(
        children=[
            dbc.Label("""Date Range Filter"""),
            html.Div(
                [
                    dcc.DatePickerRange(
                        id="my-date-picker-range",
                        calendar_orientation="horizontal",
                        min_date_allowed=dt(2021, 12, 1),
                        max_date_allowed=date.today(),
                        initial_visible_month=dt(2021, 12, 1),
                        start_date=dt(2021, 12, 1).date(),
                        end_date=date.today(),
                        display_format="MM-DD-Y",
                        updatemode="bothdates",
                    ),
                ],
            ),
        ],
    )
    logger.info(f"Exited event_date_picker_range.render() function.")

    return date_picker_comp
