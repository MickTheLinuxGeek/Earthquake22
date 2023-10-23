import logging

logger = logging.getLogger(__name__)


def load_mapbox_token() -> str:
    logger.info(f"Entered load_mapbox_token() function.")

    try:
        with open(".mapbox_token", "r", encoding="utf-8") as mbxt_in:
            mapbox_access_token = mbxt_in.read()
            logger.debug(f"Mapbox access token read:  {mapbox_access_token}")
            logger.info(f"Exited load_mapbox_token() function.")
            return mapbox_access_token
    except (FileNotFoundError, PermissionError, OSError, IOError) as err:
        print(f"Mapbox API access token not found!  {err}")
        logger.critical(f"Mapbox API access token not found!  Goto mapbox.com to get an access token.  {err}")
        raise
