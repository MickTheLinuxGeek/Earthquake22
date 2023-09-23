#!/usr/bin/env python3
# encoding: utf-8

__author__ = "Michael Biel"
__copyright__ = "Copyright 2023, MAB-Geo Data Science, The Earthquake Vis. Project"
__license__ = ""
__version__ = "1.0.1"
__maintainer__ = "Michael Biel"
__email__ = "mick.the.linux.geek@hotmail.com"
__status__ = "development"

# This is a git branch test

# ----------------------------------------------------------------------------------------------------------
#
# TODO:  Use USGS api to retrieve data instead of reading downloaded data files
#
# TODO:  Add logging
#
# Use flask caching of graph-plots; Better performance? - Completed - 09/22/2023
#
# Use python-dotenv package to read in api keys - 09/20/2023 - Decided not to implement.
#
# Refactor code - Completed - 09/19/2023
#
# TODO:  Use a nav bar in place of plot type dropdown
#
# TODO:  Re-engineer link/contacts/etc. section at bottom of document
#
# TODO:  sm, md, lg mobile responsive screen sizes need work
#
# TODO:  Add GA & NC state zipcode shapefiles for zip graph-plot -- WIP
#
# Research using dash data-table for zip responses table - 09/20/2023 - Do not need to do this; The dbc.Table
#  component works fine.
#
# ----------------------------------------------------------------------------------------------------------

from dash import Dash, html, Input, Output
import dash_bootstrap_components as dbc

# from datetime import date

# from datetime import datetime as dt
# import plotly.express as px
import pandas as pd
import geopandas as gpd
from pathlib import Path

from src.graph_plot_functions.graph_functions import (
    display_intensity_plot_1km,
    display_intensity_plot_10km,
    display_zip_plot,
    display_response_time_plot,
    display_intensity_dist_plot,
    display_dyfi_responses_tbl,
)

from src.components.layout import create_layout

# from utils.set_zoom_level import determine_zoom_level

# DATA_DIR = Path(r"./data")
# ZC_DATA_PATH = Path(r"zipcode_data")
#
# blackbold = {"color": "black", "font-weight": "bold"}
#
# mapbox_access_token = open(".mapbox_token").read()
#
# # Uncomment this line to display all dataframe columns in the console.
# pd.set_option("display.max_columns", 32)
#
# event_file = DATA_DIR / "SC_Earthquake.geojson"
# geo_df = gpd.read_file(event_file)
#
# # TODO:  From here to app definition should be done prior to running the app; usgs_api.py (api module)
#
# geo_df["Event_Date"] = (
#     pd.to_datetime(geo_df.time, unit="ms")
#     .dt.tz_localize("UTC")
#     .dt.tz_convert("America/New_York")
#     .dt.date
# )
#
# geo_df["Event_Time"] = (
#     pd.to_datetime(geo_df.time, unit="ms")
#     .dt.tz_localize("UTC")
#     .dt.tz_convert("America/New_York")
#     # .dt.time
# )
#
# # remove decimal portion of the seconds part of the time
# # for x in range(len(geo_df["Event_Time"])):
# #     geo_df.loc[x, "Event_Time"] = geo_df["Event_Time"][x].replace(microsecond=0)
#
# # Filter dataframe
# geo_df = geo_df[
#     [
#         "id",
#         "mag",
#         "place",
#         "detail",
#         "felt",
#         "cdi",
#         "title",
#         "geometry",
#         "Event_Date",
#         "Event_Time",
#     ]
# ]
# geo_df = geo_df.rename(
#     columns={
#         "mag": "Mag",
#         "place": "Place",
#         "detail": "Url",
#         "felt": "Felt",
#         "cdi": "CDI",
#         "title": "Title",
#     }
# )  # , 'geometry': 'Geometry'})
# geo_df.Felt = geo_df.Felt.fillna(0).astype("int")
# geo_df.CDI = geo_df.CDI.fillna(0).astype("float")
# geo_df.Place = geo_df.Place.fillna("No Location")
#
# geo_df["Depth"] = geo_df.geometry.z
# geo_df["Mag"] = geo_df.Mag.round(1)

# =======================================================================================================================

# geo_df = geo_df.copy()

# print(geo_df.head())


# app = Dash(
#     __name__,
#     external_stylesheets=[dbc.themes.BOOTSTRAP],
#     meta_tags=[
#         {
#             "name": "viewport",
#             "content": "width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,",
#         }
#     ],
# )
# server = app.server


# def determine_zoom_level(longitudes=None, latitudes=None):
#     """Function documentation:\n
#     Basic framework adopted from Krichardson under the following thread:
#     https://community.plotly.com/t/dynamic-zoom-for-mapbox/32658/7
#
#     # NOTE:
#     # THIS IS A TEMPORARY SOLUTION UNTIL THE DASH TEAM IMPLEMENTS DYNAMIC ZOOM
#     # in their plotly-functions associated with mapbox, such as go.Densitymapbox() etc.
#
#     Returns the appropriate zoom-level for these plotly-mapbox-graphics along with
#     the center coordinate tuple of all provided coordinate tuples.
#     """
#
#     # Check whether both latitudes and longitudes have been passed,
#     # or if the list lengths don't match
#     if (latitudes is None or longitudes is None) or (len(latitudes) != len(longitudes)):
#         # Otherwise, return the default values of 0 zoom and the coordinate origin as center point
#         return 0, (0, 0)
#
#     # Get the boundary-box
#     b_box = {
#         "height": latitudes.max() - latitudes.min(),
#         "width": longitudes.max() - longitudes.min(),
#         "center": (np.mean(longitudes), np.mean(latitudes)),
#     }
#
#     # get the area of the bounding box in order to calculate a zoom-level
#     area = b_box["height"] * b_box["width"]
#
#     # * 1D-linear interpolation with numpy:
#     # - Pass the area as the only x-value and not as a list, in order to return a scalar as well
#     # - The x-points "xp" should be in parts in comparable order of magnitude of the given area
#     # - The zoom-levels are adapted to the areas, i.e. start with the smallest area possible of 0
#     # which leads to the highest possible zoom value 20, and so forth decreasing with increasing areas
#     # as these variables are anti-proportional
#     zoom = np.interp(
#         x=area,
#         xp=[0, 5**-10, 4**-10, 3**-10, 2**-10, 1**-10, 1**-5],
#         fp=[20, 15, 14, 13, 12, 7, 5],
#     )
#
#     # Finally, return the zoom level and the associated boundary-box center coordinates
#     return zoom, b_box["center"]


# graph-plot functions
# def display_intensity_plot_1km(evnt_id, sdata):
#     """Display 1km spacing choropleth map of earthquake DYFI intensities
#
#     Plots a 1km spacing choropleth map of the DYFI earthquake intensities for selected event.
#
#     Parameters
#     ----------
#     evnt_id : String
#         The event id identifying the selected earthquake event.
#     sdata : Python dictionary
#         A dictionary containing the basic event data of the selected event.
#
#     Returns
#     -------
#     html.Div which contains a dcc.Graph which contains the figure
#         fig -- A figure containing a 1km spacing choropleth map.
#
#     """
#
#     # print(sdata['points'][0]['customdata'][1])
#
#     filename = DATA_DIR / evnt_id / "dyfi_geo_1km.geojson"
#     # print(filename)
#
#     with open(filename) as file1:
#         cdi_geo_1km_geojson = json.load(file1)
#     cdi_geo_1km_df = pd.json_normalize(cdi_geo_1km_geojson, ["features"])
#
#     ww = list(cdi_geo_1km_df["properties.nresp"])
#     xx = list(cdi_geo_1km_df["properties.name"])
#     yy = list(cdi_geo_1km_df["properties.cdi"])
#     zz = list(cdi_geo_1km_df["properties.dist"])
#
#     nh = np.empty(shape=(len(yy), 4, 1), dtype="object")
#     nh[:, 0] = np.array(xx).reshape(-1, 1)
#     nh[:, 1] = np.array(yy).reshape(-1, 1)
#     nh[:, 2] = np.array(zz).reshape(-1, 1)
#     nh[:, 3] = np.array(ww).reshape(-1, 1)
#
#     # print(cdi_geo_1km_df)
#
#     fig = go.Figure()
#     fig.add_trace(
#         go.Choroplethmapbox(
#             geojson=cdi_geo_1km_geojson,
#             locations=cdi_geo_1km_df["properties.name"],
#             z=cdi_geo_1km_df["properties.cdi"],
#             featureidkey="properties.name",
#             # subplot="mapbox",
#             coloraxis="coloraxis",
#             below="",
#             name="",
#             customdata=nh,
#             hoverlabel={"bgcolor": "#323232"},
#             hovertemplate="UTM Geocode/City: %{customdata[0]}<br>"
#             + "Response Count:  %{customdata[3]} -- "
#             + "CDI: %{customdata[1]} -"
#             + "- Distance %{customdata[2]} km",
#             marker=dict(opacity=0.30),
#         )
#     )
#
#     fig.add_trace(
#         go.Scattermapbox(
#             lon=[sdata["points"][0]["lon"]],
#             lat=[sdata["points"][0]["lat"]],
#             showlegend=False,
#             # subplot="mapbox",
#             mode="markers+lines",
#             marker={"size": 12, "opacity": 1, "symbol": ["star"]},
#             name="",
#             text=[sdata["points"][0]["customdata"][1]],
#             hoverlabel={"bgcolor": "#323232"},
#             hovertemplate="Epicenter -- Latitude:  %{lat},  Longitude:  %{lon}<br>"
#             + "Location -- %{text}",
#         )
#     )
#
#     fig.update_layout(
#         mapbox=dict(
#             zoom=7.5,
#             style="streets",
#             center={"lat": sdata["points"][0]["lat"], "lon": sdata["points"][0]["lon"]},
#             accesstoken=mapbox_access_token,
#         ),
#         coloraxis=dict(colorscale="Portland"),
#         coloraxis_colorbar=dict(
#             orientation="v",
#             lenmode="pixels",
#             len=435,
#             thicknessmode="pixels",
#             thickness=10,
#             xanchor="left",
#             x=-0.025,
#             xpad=1,
#             ticks="inside",
#             tickcolor="white",
#             title=dict(text="CDI"),
#         ),
#         showlegend=False,
#         paper_bgcolor="#FFDEAD",
#         hovermode="closest",
#         hoverdistance=5,
#         title=dict(
#             font=dict(color="#2F4F4F", size=14),
#             text="CDI Choropleth Mapbox Plot - 1km Spacing",
#         ),
#         template="ggplot2",
#         margin={"r": 4, "t": 25, "l": 4, "b": 4},
#     )
#
#     return html.Div(
#         [
#             dcc.Graph(
#                 figure=fig,
#                 config={
#                     "scrollZoom": True,
#                     "responsive": True,
#                     "modeBarButtonsToRemove": [
#                         "zoom",
#                         "pan",
#                         "select",
#                         "lasso2d",
#                         "toImage",
#                         "autoScale",
#                     ],
#                 },
#                 style={
#                     "padding-bottom": "1px",
#                     "padding-top": "2px",
#                     "padding-left": "1px",
#                     "padding-right": "1px",
#                     "flex-grow": "1",
#                     "height": "55vh",
#                     "width": "100%",
#                 },
#             )
#         ]
#     )


# def display_intensity_plot_10km(evnt_id, sdata):
#     """Display 10km spacing choropleth map of earthquake DYFI intensities
#
#     Plots a 10 km spacing choropleth map of the DYFI earthquake intensities for selected event.
#
#     Parameters
#     ----------
#     evnt_id : String
#         The event id identifying the selected earthquake event.
#     sdata : Python dictionary
#         A dictionary containing the basic event data of the selected event.
#
#     Returns
#     -------
#     html.Div which contains a dcc.Graph which contains the figure
#         fig -- A figure containing a 1km spacing and a 10 km spacing choropleth map.
#
#     """
#
#     filename = DATA_DIR / evnt_id / "dyfi_geo_10km.geojson"
#     # print(filename)
#
#     with open(filename) as file2:
#         cdi_geo_10km_geojson = json.load(file2)
#     cdi_geo_10km_df = pd.json_normalize(cdi_geo_10km_geojson, ["features"])
#
#     # print(cdi_geo_10km_df)
#
#     ww = list(cdi_geo_10km_df["properties.nresp"])
#     xx = list(cdi_geo_10km_df["properties.name"])
#     yy = list(cdi_geo_10km_df["properties.cdi"])
#     zz = list(cdi_geo_10km_df["properties.dist"])
#
#     nh = np.empty(shape=(len(yy), 4, 1), dtype="object")
#     nh[:, 0] = np.array(xx).reshape(-1, 1)
#     nh[:, 1] = np.array(yy).reshape(-1, 1)
#     nh[:, 2] = np.array(zz).reshape(-1, 1)
#     nh[:, 3] = np.array(ww).reshape(-1, 1)
#
#     fig = go.Figure()
#     fig.add_trace(
#         go.Choroplethmapbox(
#             geojson=cdi_geo_10km_geojson,
#             locations=cdi_geo_10km_df["properties.name"],
#             z=cdi_geo_10km_df["properties.cdi"],
#             featureidkey="properties.name",
#             # subplot="mapbox2",
#             coloraxis="coloraxis",
#             name="",
#             customdata=nh,
#             hoverlabel={"bgcolor": "#323232"},
#             hovertemplate="UTM Geocode/City: %{customdata[0]}<br>"
#             + "Response Count:  %{customdata[3]} -- "
#             + "CDI: %{customdata[1]} -"
#             + "- Distance %{customdata[2]} km",
#             marker=dict(opacity=0.30),
#         )
#     )
#
#     fig.add_trace(
#         go.Scattermapbox(
#             lon=[sdata["points"][0]["lon"]],
#             lat=[sdata["points"][0]["lat"]],
#             showlegend=False,
#             # subplot="mapbox2",
#             mode="markers+lines",
#             marker={"size": 12, "opacity": 1, "symbol": ["star"]},
#             name="",
#             text=[sdata["points"][0]["customdata"][1]],
#             hoverlabel={"bgcolor": "#323232"},
#             hovertemplate="Epicenter -- Latitude:  %{lat},  Longitude:  %{lon}<br>"
#             + "Location -- %{text}",
#         )
#     )
#
#     fig.update_layout(
#         mapbox=dict(
#             zoom=7.5,
#             style="streets",
#             center={"lat": sdata["points"][0]["lat"], "lon": sdata["points"][0]["lon"]},
#             accesstoken=mapbox_access_token,
#         ),
#         # coloraxis=dict(colorscale='Plotly3'),
#         coloraxis=dict(colorscale="Portland"),
#         coloraxis_colorbar=dict(
#             orientation="v",
#             lenmode="pixels",
#             len=435,
#             thicknessmode="pixels",
#             thickness=10,
#             xanchor="left",
#             x=-0.025,
#             xpad=1,
#             ticks="inside",
#             tickcolor="white",
#             title=dict(text="CDI"),
#         ),
#         showlegend=False,
#         paper_bgcolor="#FFDEAD",
#         hovermode="closest",
#         hoverdistance=5,
#         title=dict(
#             font=dict(color="#2F4F4F", size=14),
#             text="CDI Choropleth Mapbox Plot - 10km Spacing",
#         ),
#         template="ggplot2",
#         margin={"r": 4, "t": 25, "l": 4, "b": 4},
#     )
#
#     return html.Div(
#         [
#             dcc.Graph(
#                 figure=fig,
#                 config={
#                     "scrollZoom": True,
#                     "responsive": True,
#                     "modeBarButtonsToRemove": [
#                         "zoom",
#                         "pan",
#                         "select",
#                         "lasso2d",
#                         "toImage",
#                         "autoScale",
#                     ],
#                 },
#                 style={
#                     "padding-bottom": "1px",
#                     "padding-top": "2px",
#                     "padding-left": "1px",
#                     "padding-right": "1px",
#                     "flex-grow": "1",
#                     "height": "55vh",
#                     "width": "100%",
#                 },
#             )
#         ]
#     )


# def display_zip_plot(evnt_id, sdata):
#     """Display a zipcode choropleth map of the earthquake DYFI intensities.
#
#     Plot a zipcode choropleth map of the DYFI reported intensities of the earthquake event.
#
#     Parameters
#     ----------
#     evnt_id : String
#         The USGS.gov id string of the earthquake event.
#     sdata : Python dictionary
#         A dictionary containing the basic event data of the selected event.
#
#     Returns
#     -------
#     html.Div which contains a dcc.Graph which contains the figure
#         fig -- A figure containing a zipcode DYFI intensities choropleth map.
#
#     """
#     filename = DATA_DIR / evnt_id / "cdi_zip.csv"
#     cdi_zip_df = pd.read_csv(filename)
#     cdi_zip_df.rename({"# Columns: ZIP/Location": "ZIP/Location"}, axis=1, inplace=True)
#
#     # Using NC, SC, & GA region zipcodes instead of just SC
#     # zc_filename = DATA_DIR / "NC_SC_GA_region_zipcodes.geojson"
#     # Used parquet file format for the zip code file because it is read in faster; geojson file read is way too slow
#
#     # zc_filename = DATA_DIR / "NC_SC_GA_region_zipcodes.parquet"
#     # sc_zip_df = gpd.read_parquet(zc_filename, columns=["geometry", "ZCTA5CE10"])
#
#     zc_filename = DATA_DIR / ZC_DATA_PATH / "cb_2010_45_zcta510.shp"
#     sc_zip_df = gpd.read_file(zc_filename)
#
#     # sc_zip_df = gpd.read_file(r"/home/mick/Work/data_science/SC_earthquake/data/zipcode_data/cb_2010_45_zcta510.shp")
#
#     cdi_zip_df["ZIP/Location"] = cdi_zip_df[["ZIP/Location"]].astype("str")
#
#     # sc_zip_df["ZCTA5CE10"] = sc_zip_df[["ZCTA5CE10"]].astype("str")
#     sc_zip_df["Zipcode"] = sc_zip_df[["Zipcode"]].astype("str")
#
#     df = cdi_zip_df.copy()
#     geo_dff = (
#         # gpd.GeoDataFrame(sc_zip_df).merge(df, left_on="ZCTA5CE10", right_on="ZIP/Location").set_index("ZIP/Location")
#         gpd.GeoDataFrame(sc_zip_df).merge(
#             df, left_on="Zipcode", right_on="ZIP/Location"
#         )
#         # .set_index("ZIP/Location")  # FIXME:  Remove this line
#     )
#
#     geo_dff = geo_dff[
#         ["Zipcode", "CDI", "Response_Count", "Hypocentral_Distance", "geometry"]
#     ]
#
#     print(geo_dff)  # FIXME:  Remove this line
#
#     state_zip_json = json.loads(geo_dff.to_json())
#
#     ww = list(df["CDI"])
#     xx = list(df["ZIP/Location"])
#     yy = list(df["Response_Count"])
#     zz = list(df["Hypocentral_Distance"])
#
#     nh = np.empty(shape=(len(yy), 4, 1), dtype="object")
#     nh[:, 0] = np.array(xx).reshape(-1, 1)
#     nh[:, 1] = np.array(yy).reshape(-1, 1)
#     nh[:, 2] = np.array(zz).reshape(-1, 1)
#     nh[:, 3] = np.array(ww).reshape(-1, 1)
#
#     fig = go.Figure()
#     fig.add_trace(
#         go.Choroplethmapbox(
#             geojson=state_zip_json,
#             locations=df["ZIP/Location"],
#             z=df["CDI"],
#             featureidkey="properties.Zipcode",
#             # featureidkey="properties.ZCTA5CE10",
#             marker={"opacity": 0.3, "line_width": 0.5},
#             showscale=True,
#             coloraxis="coloraxis",
#             name="",
#             customdata=nh,
#             hoverlabel={"bgcolor": "#323232"},
#             hovertemplate="ZIP/Postal Code:  %{customdata[0]}<br>"
#             + "Responses:  %{customdata[1]}<br>"
#             + "CDI:  %{customdata[3]}"
#             + " -- Distance:  %{customdata[2]} km",
#         )
#     )
#
#     fig.add_trace(
#         go.Scattermapbox(
#             lon=[sdata["points"][0]["lon"]],
#             lat=[sdata["points"][0]["lat"]],
#             mode="markers+lines",
#             marker={"size": 10, "symbol": ["star"]},
#             name="",
#             text=[sdata["points"][0]["customdata"][1]],
#             hoverlabel={"bgcolor": "#323232"},
#             hovertemplate="Epicenter -- Latitude:  %{lat},  Longitude:  %{lon}<br>"
#             + "Location -- %{text}",
#         )
#     )
#
#     fig.update_layout(
#         # mapbox_style="open-street-map",
#         mapbox_style="streets",
#         mapbox_zoom=7.5,
#         mapbox_center={
#             "lat": sdata["points"][0]["lat"],
#             "lon": sdata["points"][0]["lon"],
#         },
#         mapbox=dict(accesstoken=mapbox_access_token),
#         autosize=True,
#         margin={"r": 4, "t": 25, "l": 4, "b": 4},
#         template="ggplot2",
#         title=dict(font=dict(color="#2F4F4F"), text="Zipcode CDI Choropleth Map"),
#         paper_bgcolor="#FFDEAD",
#         hovermode="closest",
#         hoverdistance=3,
#         coloraxis=dict(colorscale="Portland"),
#         coloraxis_colorbar=dict(
#             orientation="v",
#             lenmode="pixels",
#             len=435,
#             thicknessmode="pixels",
#             thickness=10,
#             xanchor="left",
#             x=-0.025,
#             xpad=1,
#             ticks="inside",
#             tickcolor="white",
#             title=dict(text="CDI"),
#         ),
#         showlegend=False,
#     )
#     # return fig
#     return html.Div(
#         [
#             dcc.Graph(
#                 figure=fig,
#                 config={
#                     "scrollZoom": True,
#                     "responsive": True,
#                     "modeBarButtonsToRemove": [
#                         "zoom",
#                         "pan",
#                         "select",
#                         "lasso2d",
#                         "toImage",
#                         "autoScale",
#                     ],
#                 },
#                 style={
#                     "padding-bottom": "1px",
#                     "padding-top": "2px",
#                     "padding-left": "1px",
#                     "padding-right": "1px",
#                     "flex-grow": "1",
#                     "height": "55vh",
#                     "width": "100%",
#                 },
#             )
#         ],
#         style={"width": "100%"},
#     )
#
#
# def display_intensity_dist_plot(evnt_id):
#     """Display a graph of the event's DYFI reported intensities vs. hypo-central distance from the event.
#
#     Plot a graph figure that contains a graph indicating various intensity vs. distance statistics.
#       First -- Every DYFI intensity reported vs. hypo-central distance
#       Second -- Intensity prediction based on the indicated equation
#       Third -- Mean intensity +/- one Std. Dev. each distance bin
#       Fourth -- Median Intensity for each distance bin
#
#     Parameters
#     ----------
#     evnt_id : String
#         The USGS.gov id string for the earthquake event.
#
#     Returns
#     -------
#     html.Div which contains a dcc.Graph which contains the figure
#         fig -- A figure containing four subplots: first -- Every DYFI reported intensity vs. hypo-central distance
#                                                   second -- Intensity prediction based on the indicated equation
#                                                   third -- Mean intensity +/- one Std. Dev. each distance bin
#                                                   fourth -- Median Intensity for each distance bin
#
#     """
#
#     filename = DATA_DIR / evnt_id / "dyfi_plot_atten.json"
#     intensity_dist_df = pd.read_json(filename)
#
#     # print(len(intensity_dist_df), intensity_dist_df)
#
#     fig = go.Figure()
#     for dsi in range(len(intensity_dist_df)):
#         dataset_df = pd.DataFrame(intensity_dist_df.datasets[dsi])
#         # print(dataset_df)
#         if dataset_df["class"][0] == "scatterplot1":
#             sct_plt_df = dataset_df.from_records(data=dataset_df.data)
#             xi = list(sct_plt_df.x)
#             yi = list(sct_plt_df.y)
#             ylabel = intensity_dist_df.ylabel[0]
#
#             fig.add_trace(
#                 go.Scatter(
#                     x=xi,
#                     y=yi,
#                     mode="markers",
#                     marker=dict(color="rgb(148, 223, 234)", size=6),
#                     name="All Reported Data",
#                     customdata=xi,
#                     text=yi,
#                     hovertemplate="Hypocentral Dist. (km):  %{customdata}<br>"
#                     + "CDI:  %{text}",
#                 )
#             )
#             fig.update_yaxes(title_text=ylabel, range=[0, 10])
#             fig.update_layout(
#                 yaxis=dict(
#                     tickvals=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], fixedrange=True
#                 ),
#                 title_text="Intensity Vs. Distance",
#                 plot_bgcolor="#FAEBD7",
#                 paper_bgcolor="#FFDEAD",
#             )
#
#         elif dataset_df["class"][0] == "estimated1":
#             est_plt_df = dataset_df.from_records(data=dataset_df.data)
#             xi = list(est_plt_df.x)
#             yi = list(est_plt_df.y)
#             name = dataset_df["legend"][0]
#
#             fig.add_trace(
#                 go.Scatter(
#                     x=xi,
#                     y=yi,
#                     name=name,
#                     mode="lines+markers",
#                     line=dict(color="rgb(214, 86, 23)", width=2),
#                     marker=dict(color="rgb(214, 86, 23)", size=6),
#                     customdata=xi,
#                     text=yi,
#                     hovertemplate="Hypocentral Dist. (km):  %{customdata}<br>"
#                     + "Estimated CDI:  %{text:.2f}",
#                 )
#             )
#
#         elif dataset_df["class"][0] == "estimated2":
#             est_plt_df = dataset_df.from_records(data=dataset_df.data)
#             xi = list(est_plt_df.x)
#             yi = list(est_plt_df.y)
#             name = dataset_df["legend"][0]
#
#             fig.add_trace(
#                 go.Scatter(
#                     x=xi,
#                     y=yi,
#                     name=name,
#                     mode="lines+markers",
#                     line=dict(color="orange", width=2),
#                     marker=dict(color="orange", size=6),
#                     customdata=xi,
#                     text=yi,
#                     hovertemplate="Hypocentral Dist. (km):  %{customdata}<br>"
#                     + "Estimated CDI:  %{text:.2f}",
#                 )
#             )
#
#         elif dataset_df["class"][0] == "binned":
#             mean_plt_df = dataset_df.from_records(data=dataset_df.data)
#
#             # print(mean_plt_df)
#
#             xi = mean_plt_df.x
#             yi = mean_plt_df.y
#             yerr = mean_plt_df.stdev
#             xlabel = intensity_dist_df.xlabel[0]
#             ylabel = intensity_dist_df.ylabel[0]
#             name = dataset_df["legend"][0]
#
#             xx = list(mean_plt_df.x)
#             yy = list(mean_plt_df.y)
#             yyerr = list(mean_plt_df.stdev)
#             nk = np.empty(shape=(len(xx), 3, 1))
#             nk[:, 0] = np.array(xx).reshape(-1, 1)
#             nk[:, 1] = np.array(yy).reshape(-1, 1)
#             nk[:, 2] = np.array(yyerr).reshape(-1, 1)
#
#             fig.add_trace(
#                 go.Scatter(
#                     x=xi,
#                     y=yi,
#                     name=name,
#                     error_y=dict(
#                         type="data",
#                         array=yerr,
#                         color="rgb(141, 145, 235)",
#                         visible=True,
#                     ),
#                     mode="markers",
#                     marker=dict(color="rgb(141, 145, 235)", size=6),
#                     customdata=nk,
#                     hovertemplate="Hypocentral Dist. (km):  %{customdata[0]}<br>"
#                     + "Mean CDI:  %{customdata[1]:.1f}<br>"
#                     + "Std. Dev. %{customdata[2]:.2f}",
#                 )
#             )
#             fig.update_xaxes(title_text=xlabel)
#             fig.update_yaxes(title_text=ylabel)
#
#         elif dataset_df["class"][0] == "median":
#             median_plt_df = dataset_df.from_records(data=dataset_df.data)
#             xi = median_plt_df.x  # Distance
#             yi = median_plt_df.y  # CDI
#             xlabel = intensity_dist_df.xlabel[0]
#             name = dataset_df["legend"][0]
#
#             fig.add_trace(
#                 go.Scatter(
#                     x=xi,
#                     y=yi,
#                     mode="markers",
#                     name=name,
#                     marker=dict(color="rgb(254, 77, 85)", size=6),
#                     customdata=xi,
#                     text=yi,
#                     hovertemplate="Hypocentral Dist. (km):  %{customdata}<br>"
#                     + "Median CDI:  %{text}",
#                 )
#             )
#             fig.update_xaxes(title_text=xlabel, range=[0, max(xi)])
#
#     fig.update_layout(
#         margin={"r": 4, "t": 25, "l": 4, "b": 4},
#         legend=dict(
#             orientation="v",
#             x=1,
#             y=1.0,
#             xanchor="right",
#             bordercolor="Black",
#             borderwidth=1.0,
#         ),
#     )
#     # return fig
#     return html.Div(
#         [
#             dcc.Graph(
#                 figure=fig,
#                 config={
#                     "scrollZoom": True,
#                     "responsive": True,
#                     "displayModeBar": False,
#                 },
#                 style={
#                     "padding-bottom": "1px",
#                     "padding-top": "2px",
#                     "padding-left": "1px",
#                     "padding-right": "1px",
#                     "flex-grow": "1",
#                     "height": "55vh",
#                     "width": "100%",
#                 },
#             )
#         ]
#     )
#
#
# def display_response_time_plot(evnt_id):
#     """Display a line graph of DYFI number of responses vs. time since earthquake event.
#
#     Plot a figure that displays a line graph showing the DYFI number of responses vs. time since earthquake.
#
#     Parameters
#     ----------
#     evnt_id : String
#         The USGS.gov id string for the earthquake event.
#
#     Returns
#     -------
#     html.Div which contains a dcc.Graph which contains the graph figure
#         fig -- A figure containing a line graph of responses vs. time.
#
#     """
#
#     filename = DATA_DIR / evnt_id / "dyfi_plot_numresp.json"
#     resp_time_df = pd.read_json(filename)
#
#     # print(len(resp_time_df), resp_time_df)
#
#     resp_time_ds_df = pd.DataFrame(resp_time_df.datasets[0])
#
#     # print(resp_time_ds_df)
#     resp_time_plot_df = resp_time_ds_df.from_records(data=resp_time_ds_df.data)
#
#     xi = list(resp_time_plot_df.x)
#     yi = list(resp_time_plot_df.y)
#     xlabel = resp_time_df.xlabel[0]
#     ylabel = resp_time_df.ylabel[0]
#     title = resp_time_df.title[0]
#
#     fig = go.Figure()
#     fig.add_trace(
#         go.Scatter(
#             x=xi,
#             y=yi,
#             mode="lines+markers",
#             line=dict(color="green", width=2),
#             marker=dict(color="green", size=6),
#             hovertemplate="Responses:  %{y}<br>"
#             + "Time Since Event:  %{x}<extra></extra>",
#         )
#     )
#     fig.update_xaxes(title_text=xlabel)
#     fig.update_yaxes(title_text=ylabel)
#
#     fig.update_layout(
#         title_text=title,
#         plot_bgcolor="#FAEBD7",
#         paper_bgcolor="#FFDEAD",
#         template="ggplot2",
#         margin={"r": 4, "t": 25, "l": 4, "b": 4},
#     )
#
#     return html.Div(
#         [
#             dcc.Graph(
#                 figure=fig,
#                 config={
#                     "scrollZoom": False,
#                     "responsive": True,
#                     "displayModeBar": False,
#                 },
#                 style={
#                     "padding-bottom": "1px",
#                     "padding-top": "2px",
#                     "padding-left": "1px",
#                     "padding-right": "1px",
#                     "flex-grow": "1",
#                     "height": "55vh",
#                     "width": "100%",
#                 },
#             )
#         ]
#     )
#
#
# def display_dyfi_responses_tbl(evnt_id):
#     """Display a table of the DYFI responses information.
#
#     Display a table of DYFI responses based on zipcode which shows the CDI intensity value, number of responses for that
#     location, distance, latitude, and longitude.
#
#     Parameters
#     ----------
#     evnt_id : String
#         The USGS.gov id string for the earthquake event.
#
#     Returns
#     -------
#     html.Div which contains a dbc.Table
#         table -- Object that contains the dbc.Table
#
#     """
#     filename = DATA_DIR / evnt_id / "cdi_zip.csv"
#     dyfi_responses_df = pd.read_csv(filename, index_col=False)
#
#     # print(dyfi_responses_df, dyfi_responses_df.columns)
#
#     # table = dbc.Table.from_dataframe(dyfi_responses_df, striped=True, bordered=True, hover=True)  #, responsive=True)
#
#     table_header = [
#         html.Thead(html.Tr([html.Th(i) for i in dyfi_responses_df.columns]))
#     ]
#
#     table_body = [
#         html.Tbody(
#             [
#                 html.Tr([html.Td(str(c)) for c in r])
#                 for r in dyfi_responses_df.to_records(index=False)
#             ]
#         )
#     ]
#     # noinspection PyTypeChecker
#     table = dbc.Table(
#         table_header + table_body, striped=True, hover=True
#     )  # Table bordered is done in style.css
#     # table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True)
#
#     return html.Div(
#         table,
#         className="table-wrapper table-responsive",
#         style={"width": "100%"},
#         # style={"max-height": "54vh", "width": "100%"},
#     )


# # Application html layout structure
# app.layout = create_layout(app)


# @app.callback(
#     Output("map-graph", "figure"),
#     Input("my-date-picker-range", "start_date"),
#     Input("my-date-picker-range", "end_date"),
#     # Input("min-mag-input", "value"),
#     # Input("max-mag-input", "value"),
# )
# # def update_output(start_date, end_date, input1, input2):
# def update_output(start_date, end_date):
#     """Map callback function
#
#     Callback function that returns a map figure based on the date range and magnitude range inputs.
#
#     Parameters
#     ----------
#     start_date : datetime.datetime.date
#         Start date of date range filter
#     end_date : datetime.datetime.date
#         End date of date range filter
#     input1 : int
#         Minimum magnitude value for filter
#     input2 : int
#         Maximum magnitude value for filter
#
#     Returns
#     -------
#     plotly.graph_objects.Figure
#         fig -- The Plotly Express scatter mapbox map figure object
#
#     """
#     geo_dff = geo_df[
#         (geo_df["Event_Date"] >= date.fromisoformat(start_date))
#         & (geo_df["Event_Date"] <= date.fromisoformat(end_date))
#         # & (geo_df["Mag"] >= input1)
#         # & (geo_df["Mag"] <= input2)
#     ]

# lats = geo_dff.geometry.y
# lons = geo_dff.geometry.x
# zoom_level, map_ctr = determine_zoom_level(lons, lats)

# fig = px.scatter_mapbox(
#     geo_dff,
#     lat=geo_dff.geometry.y,
#     lon=geo_dff.geometry.x,
#     color=geo_dff.Mag,
#     custom_data=[
#         "Title",
#         "Place",
#         "Event_Date",
#         "Event_Time",
#         "Mag",
#         "Depth",
#         "Felt",
#         "CDI",
#         "id",
#     ],
#     color_continuous_scale=px.colors.sequential.Jet,
#     # zoom=11.25,
#     zoom=zoom_level,
#     # center=dict(lat=34.170983, lon=-80.794252),
#     center=dict(lat=map_ctr[1], lon=map_ctr[0]),
#     title="South Carolina Earthquake Swarm Dec - 2021 to Present",
#     template="ggplot2",
# )
#
# fig.update_layout(
#     mapbox_style="streets",
#     mapbox_accesstoken=mapbox_access_token,
#     coloraxis_colorbar=dict(
#         orientation="h",
#         lenmode="pixels",
#         # len=435,
#         len=350,
#         thicknessmode="pixels",
#         thickness=4,
#         xanchor="left",
#         x=0,
#         xpad=3,
#         yanchor="top",
#     ),
#     title=dict(font=dict(color="#2F4F4F", size=14)),
#     autosize=True,
#     margin=dict(t=30, b=0, l=0, r=0),
#     clickmode="event+select",
#     paper_bgcolor="#FAEBD7",
#     uirevision="foo",
#     hovermode="closest",
#     hoverdistance=2,
# )
#
# fig.update_traces(
#     hovertemplate="<br>".join(
#         [
#             "Event Title: %{customdata[0]}",
#             "Event Date: %{customdata[2]}",
#             "Event Time: %{customdata[3]|%I:%M:%S}",
#             "Location: %{customdata[1]}",
#             "Magnitude: %{customdata[4]}",
#             "Lat:  %{lat},  " + "Lon:  %{lon}    " + "Depth(km):  %{customdata[5]}",
#             "DYFI: %{customdata[6]}",
#         ]
#     ),
#     mode="markers",
#     marker={"opacity": 0.75, "size": 10},
#     unselected={"marker": {"opacity": 0.75, "size": 10}},
#     selected={"marker": {"opacity": 1, "size": 25}},
# )
# return fig


# @app.callback(
#     Output("graph-plot", "children"),
#     Output("plot-type-dropdown", "disabled"),
#     Input("map-graph", "selectedData"),
#     Input("plot-type-dropdown", "value"),
#     prevent_initial_call=False,
# )
# def plot_graphs(selected_data, user_input):
#     """graph-plot callback function
#
#     Callback function that returns and displays the graph plot that is selected.
#
#     Parameters
#     ----------
#     selected_data : Python dictionary
#         A Python dictionary containing the event data of the selected point on the map.
#     user_input : string
#         A string representing the graph plot type selected from the dropdown.
#
#     Returns
#     -------
#     html.Div which contains a html.P with a text message if the seledtedData is None or the felt responses is zero or
#     html.Div which was returned from one of the graph-plot functions
#     A boolean -- Indicating whether the plot-type-dropdown is disabled or not
#     """
#
#     if selected_data is None:
#         return (
#             html.Div(
#                 children=[
#                     html.P(
#                         """Filter events displayed by using the date and magnitude filters."""
#                     ),
#                     html.P(
#                         """Select an event marker from the map and a plot type from the
#                                          dropdown for more event information."""
#                     ),
#                 ],
#                 style={
#                     "text-align": "center",
#                     "margin": "10px 0",
#                     "padding": "5px",
#                     "border": "1px solid #999",
#                     "display": "flex",
#                     "flex-direction": "column",
#                     "width": "100%",
#                 },
#                 className="center",
#             ),
#             False,
#         )
#     else:
#         event_id = selected_data["points"][0]["customdata"][8]
#
#         # print(selected_data)
#         # print(selected_data['points'][0]['lat'], selected_data['points'][0]['lon'])
#         # print(selected_data, user_input, event_id)
#         # print(new_loading_style)
#         # print(selected_data['points'][0]['customdata'][6])
#
#         # if DYFI felt is zero
#         if selected_data["points"][0]["customdata"][6] == 0:
#             # return go.Figure()
#             # return select_graph
#             # return None
#             return (
#                 html.Div(
#                     html.P("""Event has no reported DYFI information."""),
#                     style={
#                         "text-align": "center",
#                         "margin": "10px 0",
#                         "padding": "5px",
#                         "border": "1px solid #999",
#                         "display": "flex",
#                         "flex-direction": "column",
#                     },
#                     className="center",
#                 ),
#                 True,
#             )
#         elif event_id and user_input == "Intensity Plot(1km)":
#             return display_intensity_plot_1km(event_id, selected_data), False
#         elif event_id and user_input == "Intensity Plot(10km)":
#             return display_intensity_plot_10km(event_id, selected_data), False
#         elif event_id and user_input == "Zip Map":
#             return display_zip_plot(event_id, selected_data), False
#         elif event_id and user_input == "Intensity Vs. Distance":
#             return display_intensity_dist_plot(event_id), False
#         elif event_id and user_input == "Response Vs. Time":
#             return display_response_time_plot(event_id), False
#         elif event_id and user_input == "DYFI Responses":
#             return display_dyfi_responses_tbl(event_id), False
#
#
# if __name__ == "__main__":
#     app.run(debug=True, use_reloader=False, port=8051)
