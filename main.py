#!/usr/bin/env python3
# encoding: utf-8

""" Main app module

This is the module that is launched to run the application.
"""

__author__ = "Michael Biel"
__copyright__ = "Copyright 2023, MAB-Geo Data Science, The Earthquake Vis. Project"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Michael Biel"
__email__ = "mick.the.linux.geek@hotmail.com"
__status__ = "development"

import sys
import getopt
import logging
import logging.handlers as handlers
from pathlib import Path

from pandas import set_option
from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP
import pyogrio.errors

from src.components.layout import create_layout
from src.data.loader import load_event_data

# cache is instantiated in the __init__.py of graph_plot_functions and imported here.
from src.graph_plot_functions import cache

LOG_PATH = Path(r"./logs")
DATA_DIR = Path(r"./data")
event_file = DATA_DIR / "SC_Earthquake.geojson"
log_file = LOG_PATH / "app_log.log"

set_option("display.max_columns", 32)
set_option("display.width", 132)

logger = logging.getLogger("sc_earthquake_app")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# log_handler = handlers.RotatingFileHandler(log_file, mode="w", maxBytes=5 * 1024 * 1024, backupCount=3)
log_handler = logging.FileHandler(log_file, mode="w")
log_handler.setLevel(logging.DEBUG)
log_handler.setFormatter(formatter)

logger.addHandler(log_handler)


# def main(argv: list) -> None:
def main() -> None:
    """The main function of the main app module.

    The main function of the main module.  It performs the following tasks:
        * calls load_event_data() function to load the events file
        * set up the Dash app and its cache which is used to cache the graph plot functions
        * creates the app layout
        * runs the app web server
        * clears the cache when the app is closed
    """

    # try:
    #     opts, args = getopt.getopt(argv, "hl:", ["help", "log="])
    # except getopt.GetoptError as err:
    #     print(f"Invalid command-line argument:  {err}")
    #     print(f"Usage:  main.py [-l DEBUG|INFO|WARNING|ERROR|CRITICAL]")
    #     print(f"  or:   main.py [--log= DEBUG|INFO|WARNING|ERROR|CRITICAL]")
    #     sys.exit(2)
    # for opt, arg in opts:
    #     if opt in ("-h", "--help"):
    #         print(f"Usage:  main.py [-l DEBUG|INFO|WARNING|ERROR|CRITICAL]")
    #         print(f"  or:   main.py [--log= DEBUG|INFO|WARNING|ERROR|CRITICAL]")
    #         sys.exit()
    #     elif opt in ("-l", "--log"):
    #         loglevel = arg
    #
    #         numeric_level = getattr(logging, loglevel.upper(), None)
    #         if not isinstance(numeric_level, int):
    #             raise ValueError(f"Invalid log level: {loglevel}")
    #
    #         logging.basicConfig(
    #             level=numeric_level,
    #             filename=log_file,
    #             filemode="w",
    #             format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    #         )

    logger.info(f"Application Started")
    try:
        data = load_event_data(event_file)
    except pyogrio.errors.DataSourceError as err:
        print(f"Need to run usgs_api.py to create App data files.  {err}")
        sys.exit(1)
    # else:
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

    # Initialize cache instance
    cache.init_app(app.server)

    # Application html layout structure
    app.layout = create_layout(app, data)

    app.run(debug=True, use_reloader=False, port=8051)

    with app.server.app_context():
        cache.clear()


if __name__ == "__main__":
    # main(sys.argv[1:])
    main()
