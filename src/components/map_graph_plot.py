""" map_graph_plot Module

This module contains the plot_map_graph function that creates the events scatter mapbox map.

Functions:
----------
    plot_map_graph(geo_dff: GeoDataFrame) -> Figure
"""

import logging
import plotly.express as px
from plotly.graph_objects import Figure
from geopandas import GeoDataFrame

from ..utils.set_zoom_level import determine_zoom_level

logger = logging.getLogger(__name__)


def plot_map_graph(geo_dff: GeoDataFrame) -> Figure:
    """plot_map_graph -- Function that creates a plotly scatter_mapbox map in which the earthquake events are plotted.

    Function returns a plotly.graph_objects.Figure from plotly_express.scatter_mapbox().  First the map's zoom level and
    center are calculated using the latitudes and longitudes of the events.  Secondly, px.scatter_mapbox is called.

    Parameters:
    ----------

    geo_dff : geopandas.GeoDataFrame
        Contains the earthquake events to be plotted on the map

    Returns:
    -------

    Figure : plotly.graph_objects.Figure
        The plotly figure structure that contains the events map (map-graph)

    Functions:
    ----------------

        determine_zoom_level() -- determines the event map's zoom level and center based on the events lat. & lon.,

        px.scatter_mapbox -- plotly function to build map figure
    """

    logger.info(f"Entered plot_map_graph() function.")

    lats = geo_dff.geometry.y
    lons = geo_dff.geometry.x

    logger.debug(f"Latitudes from events GeoDataFrame; Used for determine_zoom_level() function.  \n{lats}")
    logger.debug(f"Longitudes from events GeoDataFrame; Used for determine_zoom_level() function.  \n{lons}")

    zoom_level, map_ctr = determine_zoom_level(lons, lats)

    logger.debug(f"Zoom level returned from determine_zoom_level(). \n{zoom_level}")
    logger.debug(f"Map center latitude and longitude returned from determine_zoom_level(). \n{map_ctr}")

    try:
        with open(".mapbox_token", "r", encoding="utf-8") as file_in:
            mapbox_access_token = file_in.read()
    except (FileNotFoundError, IOError, OSError, PermissionError) as err:
        print(f"map_graph_plot.py:  Mapbox access token not found!  {err}")
        logger.critical(f"Mapbox access token not found!  Goto mapbox.com.  {err}")
        raise
    else:
        fig = px.scatter_mapbox(
            geo_dff,
            lat=geo_dff.geometry.y,
            lon=geo_dff.geometry.x,
            color=geo_dff.Mag,
            custom_data=[
                "Title",
                "Place",
                "Event_Date",
                "Event_Time",
                "Mag",
                "Depth",
                "Felt",
                "CDI",
                "id",
            ],
            color_continuous_scale=px.colors.sequential.Jet,
            zoom=zoom_level,
            center=({"lat": map_ctr[1], "lon": map_ctr[0]}),
            title="South Carolina Earthquake Swarm Dec - 2021 to Present",
            template="ggplot2",
        )

        fig.update_layout(
            mapbox_style="streets",
            mapbox_accesstoken=mapbox_access_token,
            coloraxis_colorbar=(
                {
                    "orientation": "h",
                    "lenmode": "pixels",
                    "len": 350,
                    "thicknessmode": "pixels",
                    "thickness": 4,
                    "xanchor": "left",
                    "x": 0,
                    "xpad": 3,
                    "yanchor": "top",
                }
            ),
            title=({"font": {"color": "#2F4F4F", "size": 14}}),
            autosize=True,
            margin=({"t": 30, "b": 0, "l": 0, "r": 0}),
            clickmode="event+select",
            paper_bgcolor="#FAEBD7",
            uirevision="foo",
            hovermode="closest",
            hoverdistance=2,
        )

        fig.update_traces(
            hovertemplate="<br>".join(
                [
                    "Event Title: %{customdata[0]}",
                    "Event Date: %{customdata[2]}",
                    "Event Time: %{customdata[3]|%I:%M:%S}",
                    "Location: %{customdata[1]}",
                    "Magnitude: %{customdata[4]}",
                    "Lat:  %{lat},  " + "Lon:  %{lon}    " + "Depth(km):  %{customdata[5]}",
                    "DYFI: %{customdata[6]}",
                ]
            ),
            mode="markers",
            marker={"opacity": 0.75, "size": 10},
            unselected={"marker": {"opacity": 0.75, "size": 10}},
            selected={"marker": {"opacity": 1, "size": 25}},
        )

        logger.debug(f"Figure structure returned from px.scatter_mapbox() function.  \n{fig}")
        logger.info(f"Exited plot_map_graph() function")

    return fig
