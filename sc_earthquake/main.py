#!/usr/bin/env python3
# encoding: utf-8

""" Main app module

This is the module that is launched to run the application.
"""

__author__ = "Michael Biel"
__copyright__ = "Copyright 2024, MAB-Geo Data Science, The Earthquake Data Explorer"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Michael Biel"
__email__ = "mick.the.linux.geek@hotmail.com"
__status__ = "development"

import os
import sys
import logging
import logging.handlers
import getopt
from pathlib import Path
from pandas import set_option

# from dash import Dash
# from dash_bootstrap_components.themes import BOOTSTRAP
import pyogrio.errors

from sc_earthquake import create_app
from sc_earthquake.src.components.layout import create_layout
from sc_earthquake.src.data.loader import load_event_data

# cache is instantiated in the __init__.py of graph_plot_functions and imported here.
from sc_earthquake.src.graph_plot_functions import cache

# dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
# load_dotenv()

# log_path = Path(r"logs")
# data_dir = Path(r"data")
# event_file = data_dir / "SC_Earthquake.geojson"
# log_file = log_path / "app_log.log"

log_path = Path(os.getenv("LOG_PATH"))
data_dir = os.getenv("DATA_DIR")
event_file = Path(data_dir) / Path(os.getenv("EVENT_FILE"))
log_file = Path(log_path) / Path(os.getenv("LOG_FILE"))

set_option("display.max_columns", 32)
set_option("display.width", 132)

# Delete log files each time the app starts
# Already using pathlib; Use pathlib methods instead of importing os module
if log_file.exists():
    for file in list(log_path.glob("*")):
        file.unlink(missing_ok=True)


def main(argv: list) -> None:
    """The main function of the main app module.

    The main function of the main module.  It performs the following tasks:
        * calls load_event_data() function to load the events file
        * set up the Dash app and its cache which is used to cache the graph plot functions
        * creates the app layout
        * runs the app web server
        * clears the cache when the app is closed
    """

    try:
        opts, _ = getopt.getopt(argv, "hl:", ["help", "log="])
    except getopt.GetoptError as err:
        print(f"Invalid command-line argument:  {err}")
        print("Usage:  main.py [-l DEBUG|INFO|WARNING|ERROR|CRITICAL]")
        print("  or:   main.py [--log= DEBUG|INFO|WARNING|ERROR|CRITICAL]")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("Usage:  main.py [-l DEBUG|INFO|WARNING|ERROR|CRITICAL]")
            print("  or:   main.py [--log= DEBUG|INFO|WARNING|ERROR|CRITICAL]")
            sys.exit()
        elif opt in ("-l", "--log"):
            loglevel = arg

            numeric_level = getattr(logging, loglevel.upper(), None)
            if not isinstance(numeric_level, int):
                raise ValueError(f"Invalid log level: {loglevel}")

            rfh = logging.handlers.RotatingFileHandler(
                filename=log_file, mode="a", maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8", delay=True
            )

            logging.basicConfig(
                level=numeric_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", handlers=[rfh]
            )

            logger = logging.getLogger("sc_earthquake_app")

            logger.info("Application Started")

    # try:
    #     data = load_event_data(event_file)
    # except pyogrio.errors.DataSourceError as err:
    #     print(f"Need to run usgs_api.py to create App data files.  {err}")
    #     sys.exit(1)

    # app = Dash(
    #     __name__,
    #     external_stylesheets=[BOOTSTRAP],
    #     meta_tags=[
    #         {
    #             "name": "viewport",
    #             "content": "width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,",
    #         }
    #     ],
    #     suppress_callback_exceptions=True
    #     prevent_initial_callbacks=True
    #

    app = create_app()

    try:
        data = load_event_data(event_file)
    except pyogrio.errors.DataSourceError as err:
        print(f"Need to run usgs_api.py to create App data files.  {err}")
        sys.exit(1)

    # Initialize cache instance
    cache.init_app(app.server)

    # Application html layout structure
    app.layout = create_layout(app, data)

    app.run(debug=True, use_reloader=False, port=8051)

    with app.server.app_context():
        cache.clear()


if __name__ == "__main__":
    main(sys.argv[1:])
    # main()