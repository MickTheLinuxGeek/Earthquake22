""" Utility function to calculate a map's zoom level and center based on longitueds and latitudes passed in. """

import logging
import numpy as np

logger = logging.getLogger(__name__)


def determine_zoom_level(longitudes=None, latitudes=None):
    """Function documentation:\n
    Basic framework adopted from Krichardson under the following thread:
    https://community.plotly.com/t/dynamic-zoom-for-mapbox/32658/7

    # NOTE:
    # THIS IS A TEMPORARY SOLUTION UNTIL THE DASH TEAM IMPLEMENTS DYNAMIC ZOOM
    # in their plotly-functions associated with mapbox, such as go.Densitymapbox() etc.

    Returns the appropriate zoom-level for these plotly-mapbox-graphics along with
    the center coordinate tuple of all provided coordinate tuples.
    """

    logger.info("Entered determine_zoom_level() function.")
    logger.debug("longitudes parameter:\n %s", longitudes)
    logger.debug("latitudes parameter:\n %s", latitudes)

    # Check whether both latitudes and longitudes have been passed,
    # or if the list lengths don't match
    if (latitudes is None or longitudes is None) or (len(latitudes) != len(longitudes)):
        # Otherwise, return the default values of 0 zoom and the coordinate origin as center point
        return 0, (0, 0)

    # Get the boundary-box
    b_box = {
        "height": latitudes.max() - latitudes.min(),
        "width": longitudes.max() - longitudes.min(),
        "center": (np.mean(longitudes), np.mean(latitudes)),
    }

    # get the area of the bounding box in order to calculate a zoom-level
    area = b_box["height"] * b_box["width"]

    # * 1D-linear interpolation with numpy:
    # - Pass the area as the only x-value and not as a list, in order to return a scalar as well
    # - The x-points "xp" should be in parts in comparable order of magnitude of the given area
    # - The zoom-levels are adapted to the areas, i.e. start with the smallest area possible of 0
    # which leads to the highest possible zoom value 20, and so forth decreasing with increasing areas
    # as these variables are anti-proportional
    zoom = np.interp(
        x=area,
        xp=[0, 5**-10, 4**-10, 3**-10, 2**-10, 1**-10, 1**-5],
        fp=[20, 15, 14, 13, 12, 7, 5],
    )

    # Finally, return the zoom level and the associated boundary-box center coordinates

    logger.debug("Calculated zoom level:  %s", zoom)
    logger.debug("Calculated map center coordinates:  %s", b_box["center"])
    logger.info("Exited determine_zoom_level() function.")

    return zoom, b_box["center"]
