""" Module for loading mapbox API access token.

    Function reads in the mapbox API access token from the hidden file .mapbox_token.

    Functions:
    ----------

        load_mapbox_token() -> str
"""


import logging

logger = logging.getLogger(__name__)


def load_mapbox_token() -> str:
    """Function to read in the mapbox API access token

    Function reads in the mapbox API access token from the hidden file .mapbox_token.

    Returns:
    --------
    mapbox_access_token : str
        A variable containing the mapbox API access token string.
    """

    logger.info("Entered load_mapbox_token() function.")

    try:
        with open(".mapbox_token", "r", encoding="utf-8") as mbxt_in:
            mapbox_access_token = mbxt_in.read()
            logger.debug("Mapbox access token read: %s", mapbox_access_token)
            logger.info("Exited load_mapbox_token() function.")
            return mapbox_access_token
    except (FileNotFoundError, PermissionError, OSError, IOError) as err:
        print(f"Mapbox API access token not found!  {err}")
        logger.critical("Mapbox API access token not found!  Goto mapbox.com to get an access token.  %s", err)
        raise
