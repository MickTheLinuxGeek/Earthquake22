#!/usr/bin/env python3
# encoding: utf-8

__author__ = "Michael Biel"
__copyright__ = "Copyright 2023, MAB-Geo Data Science, The Earthquake Vis. Project"
__license__ = ""
__version__ = "1.0.1"
__maintainer__ = "Michael Biel"
__email__ = "mick.the.linux.geek@hotmail.com"
__status__ = "development"


from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP
from pathlib import Path

from src.components.layout import create_layout
from src.data.loader import load_event_data

DATA_DIR = Path(r"./data")
event_file = DATA_DIR / "SC_Earthquake.geojson"


def main() -> None:
    data = load_event_data(event_file)
    app = Dash(
        __name__,
        external_stylesheets=[BOOTSTRAP],
        meta_tags=[
            {
                "name": "viewport",
                "content": "width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,",
            }
        ],
        suppress_callback_exceptions=True
        # prevent_initial_callbacks=True,
    )

    # Application html layout structure
    app.layout = create_layout(app, data)

    app.run(debug=True, use_reloader=False, port=8051)


if __name__ == "__main__":
    main()
