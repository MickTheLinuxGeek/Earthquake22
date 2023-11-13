""" Events data loader module

Loads the earthquake events data from a geoJSON file and then does some data cleaning/wrangling.

Functions:
----------

    load_event_data(file: Path) -> gpd.GeoDataFrame
"""

import logging
from pathlib import Path
import pandas as pd
import geopandas as gpd
import pyogrio.errors


logger = logging.getLogger(__name__)


def load_event_data(file: Path) -> gpd.GeoDataFrame:
    """Load earthquake event data from a file.

    Reads in earthquake events data from file path and stored in a GeoDataFrame.  Afterward, some minor data wrangling
    is done.

    Parameters:
    ----------

    file : Path object
        The file path to the earthquake events file

    Returns:
    -------

    geo_df : geopandas.GeoDataFrame
        A GeoDataFrame containing the events data after some minor wrangling.
    """

    # Read geoJSON file into a geopandas.GeoDataFrame
    # geo_df = gpd.read_file(file, engine="pyogrio")

    logger.info("Entered load_event_data() function.")

    try:
        geo_df = gpd.read_file(file, engine="pyogrio")
    except pyogrio.errors.DataSourceError as err:
        print(f"SC_Earthquake.geojson file missing from data directory.  Run usgs_api to fix.  {err}")
        logger.critical("SC_Earthquake.geojson file is missing.  Run usgs_api.py to download app data files. %s", err)
        raise

    # The time column in the dataframe is a Unix epoch time in ms.  The following two statements convert that epoch
    # time into event date and event time columns that are added to the dataframe.
    geo_df["Event_Date"] = (
        pd.to_datetime(geo_df.time, unit="ms").dt.tz_localize("UTC").dt.tz_convert("America/New_York").dt.date
    )

    geo_df["Event_Time"] = (
        pd.to_datetime(geo_df.time, unit="ms")
        .dt.tz_localize("UTC")
        .dt.tz_convert("America/New_York")
        # .dt.time
    )

    # Filter dataframe
    geo_df = geo_df[
        [
            "id",
            "mag",
            "place",
            "detail",
            "felt",
            "cdi",
            "title",
            "geometry",
            "Event_Date",
            "Event_Time",
        ]
    ]

    # Rename some columns
    geo_df = geo_df.rename(
        columns={
            "mag": "Mag",
            "place": "Place",
            "detail": "Url",
            "felt": "Felt",
            "cdi": "CDI",
            "title": "Title",
        }
    )

    geo_df.Felt = geo_df.Felt.fillna(0).astype("int")
    geo_df.CDI = geo_df.CDI.fillna(0).astype("float")
    geo_df.Place = geo_df.Place.fillna("No Location")

    geo_df["Depth"] = geo_df.geometry.z
    geo_df["Mag"] = geo_df.Mag.round(1)

    logger.debug("Wrangled dataframe, geo_df after SC_Earthquakes.geojson file read.\n %s", geo_df)
    logger.info("Exited load_event_data() function.")

    return geo_df
