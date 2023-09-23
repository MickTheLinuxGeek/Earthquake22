""" Functions for the graph plots

    Each one of these functions is defined with @cache.memoize decorator to add caching to the functions.

A module of functions, one each per graph plot:
    display_intensity_plot_1km()
    display_intensity_plot_10km()
    display_zip_plot()
    display_intensity_dist_plot()
    display_response_time_plot()
    display_dyfi_responses_tbl()
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
import geopandas as gpd
import pandas as pd
import numpy as np
from pathlib import Path
import json
import plotly.graph_objects as go

from . import cache

TIMEOUT = 120
DATA_DIR = Path(r"./data")
ZC_DATA_PATH = Path(r"zipcode_data")
mapbox_access_token = open(".mapbox_token").read()


# graph-plot functions
@cache.memoize(timeout=TIMEOUT)
def display_intensity_plot_1km(evnt_id: str, sdata: dict) -> html.Div:
    """Display 1km spacing choropleth map of earthquake DYFI intensities

    Plots a 1km spacing choropleth map of the DYFI earthquake intensities for selected event.

    Parameters:
    ----------

    evnt_id : String
        The event id identifying the selected earthquake event.
    sdata : Python dictionary
        A dictionary containing the basic event data of the selected event.

    Returns:
    -------

    html.Div which contains a dcc.Graph which contains the figure fig -- A figure containing a 1km spacing choropleth
    map.
    """

    filename = DATA_DIR / evnt_id / "dyfi_geo_1km.geojson"

    with open(filename) as file1:
        cdi_geo_1km_geojson = json.load(file1)

    cdi_geo_1km_df = pd.json_normalize(cdi_geo_1km_geojson, ["features"])

    ww = list(cdi_geo_1km_df["properties.nresp"])
    xx = list(cdi_geo_1km_df["properties.name"])
    yy = list(cdi_geo_1km_df["properties.cdi"])
    zz = list(cdi_geo_1km_df["properties.dist"])

    nh = np.empty(shape=(len(yy), 4, 1), dtype="object")
    nh[:, 0] = np.array(xx).reshape(-1, 1)
    nh[:, 1] = np.array(yy).reshape(-1, 1)
    nh[:, 2] = np.array(zz).reshape(-1, 1)
    nh[:, 3] = np.array(ww).reshape(-1, 1)

    fig = go.Figure()
    fig.add_trace(
        go.Choroplethmapbox(
            geojson=cdi_geo_1km_geojson,
            locations=cdi_geo_1km_df["properties.name"],
            z=cdi_geo_1km_df["properties.cdi"],
            featureidkey="properties.name",
            # subplot="mapbox",
            coloraxis="coloraxis",
            below="",
            name="",
            customdata=nh,
            hoverlabel={"bgcolor": "#323232"},
            hovertemplate="UTM Geocode/City: %{customdata[0]}<br>"
            + "Response Count:  %{customdata[3]} -- "
            + "CDI: %{customdata[1]} -"
            + "- Distance %{customdata[2]} km",
            marker=dict(opacity=0.30),
        )
    )

    fig.add_trace(
        go.Scattermapbox(
            lon=[sdata["points"][0]["lon"]],
            lat=[sdata["points"][0]["lat"]],
            showlegend=False,
            # subplot="mapbox",
            mode="markers+lines",
            marker={"size": 12, "opacity": 1, "symbol": ["star"]},
            name="",
            text=[sdata["points"][0]["customdata"][1]],
            hoverlabel={"bgcolor": "#323232"},
            hovertemplate="Epicenter -- Latitude:  %{lat},  Longitude:  %{lon}<br>" + "Location -- %{text}",
        )
    )

    fig.update_layout(
        mapbox=dict(
            zoom=7.5,
            style="streets",
            center={"lat": sdata["points"][0]["lat"], "lon": sdata["points"][0]["lon"]},
            accesstoken=mapbox_access_token,
        ),
        coloraxis=dict(colorscale="Portland"),
        coloraxis_colorbar=dict(
            orientation="v",
            lenmode="pixels",
            len=435,
            thicknessmode="pixels",
            thickness=10,
            xanchor="left",
            x=-0.025,
            xpad=1,
            ticks="inside",
            tickcolor="white",
            title=dict(text="CDI"),
        ),
        showlegend=False,
        paper_bgcolor="#FFDEAD",
        hovermode="closest",
        hoverdistance=5,
        title=dict(
            font=dict(color="#2F4F4F", size=14),
            text="CDI Choropleth Mapbox Plot - 1km Spacing",
        ),
        template="ggplot2",
        margin={"r": 4, "t": 25, "l": 4, "b": 4},
    )

    return html.Div(
        [
            dcc.Graph(
                figure=fig,
                config={
                    "scrollZoom": True,
                    "responsive": True,
                    "modeBarButtonsToRemove": [
                        "zoom",
                        "pan",
                        "select",
                        "lasso2d",
                        "toImage",
                        "autoScale",
                    ],
                },
                style={
                    "padding-bottom": "1px",
                    "padding-top": "2px",
                    "padding-left": "1px",
                    "padding-right": "1px",
                    "flex-grow": "1",
                    "height": "55vh",
                    "width": "100%",
                },
            )
        ]
    )


@cache.memoize(timeout=TIMEOUT)
def display_intensity_plot_10km(evnt_id: str, sdata: dict) -> html.Div:
    """Display 10km spacing choropleth map of earthquake DYFI intensities

    Plots a 10 km spacing choropleth map of the DYFI earthquake intensities for selected event.

    Parameters:
    ----------

    evnt_id : String
        The event id identifying the selected earthquake event.
    sdata : Python dictionary
        A dictionary containing the basic event data of the selected event.

    Returns:
    -------

    html.Div which contains a dcc.Graph which contains the figure fig -- A figure containing a 1km spacing and a 10 km
    spacing choropleth map.
    """

    filename = DATA_DIR / evnt_id / "dyfi_geo_10km.geojson"

    with open(filename) as file2:
        cdi_geo_10km_geojson = json.load(file2)

    cdi_geo_10km_df = pd.json_normalize(cdi_geo_10km_geojson, ["features"])

    ww = list(cdi_geo_10km_df["properties.nresp"])
    xx = list(cdi_geo_10km_df["properties.name"])
    yy = list(cdi_geo_10km_df["properties.cdi"])
    zz = list(cdi_geo_10km_df["properties.dist"])

    nh = np.empty(shape=(len(yy), 4, 1), dtype="object")
    nh[:, 0] = np.array(xx).reshape(-1, 1)
    nh[:, 1] = np.array(yy).reshape(-1, 1)
    nh[:, 2] = np.array(zz).reshape(-1, 1)
    nh[:, 3] = np.array(ww).reshape(-1, 1)

    fig = go.Figure()
    fig.add_trace(
        go.Choroplethmapbox(
            geojson=cdi_geo_10km_geojson,
            locations=cdi_geo_10km_df["properties.name"],
            z=cdi_geo_10km_df["properties.cdi"],
            featureidkey="properties.name",
            # subplot="mapbox2",
            coloraxis="coloraxis",
            name="",
            customdata=nh,
            hoverlabel={"bgcolor": "#323232"},
            hovertemplate="UTM Geocode/City: %{customdata[0]}<br>"
            + "Response Count:  %{customdata[3]} -- "
            + "CDI: %{customdata[1]} -"
            + "- Distance %{customdata[2]} km",
            marker=dict(opacity=0.30),
        )
    )

    fig.add_trace(
        go.Scattermapbox(
            lon=[sdata["points"][0]["lon"]],
            lat=[sdata["points"][0]["lat"]],
            showlegend=False,
            # subplot="mapbox2",
            mode="markers+lines",
            marker={"size": 12, "opacity": 1, "symbol": ["star"]},
            name="",
            text=[sdata["points"][0]["customdata"][1]],
            hoverlabel={"bgcolor": "#323232"},
            hovertemplate="Epicenter -- Latitude:  %{lat},  Longitude:  %{lon}<br>" + "Location -- %{text}",
        )
    )

    fig.update_layout(
        mapbox=dict(
            zoom=7.5,
            style="streets",
            center={"lat": sdata["points"][0]["lat"], "lon": sdata["points"][0]["lon"]},
            accesstoken=mapbox_access_token,
        ),
        coloraxis=dict(colorscale="Portland"),
        coloraxis_colorbar=dict(
            orientation="v",
            lenmode="pixels",
            len=435,
            thicknessmode="pixels",
            thickness=10,
            xanchor="left",
            x=-0.025,
            xpad=1,
            ticks="inside",
            tickcolor="white",
            title=dict(text="CDI"),
        ),
        showlegend=False,
        paper_bgcolor="#FFDEAD",
        hovermode="closest",
        hoverdistance=5,
        title=dict(
            font=dict(color="#2F4F4F", size=14),
            text="CDI Choropleth Mapbox Plot - 10km Spacing",
        ),
        template="ggplot2",
        margin={"r": 4, "t": 25, "l": 4, "b": 4},
    )

    return html.Div(
        [
            dcc.Graph(
                figure=fig,
                config={
                    "scrollZoom": True,
                    "responsive": True,
                    "modeBarButtonsToRemove": [
                        "zoom",
                        "pan",
                        "select",
                        "lasso2d",
                        "toImage",
                        "autoScale",
                    ],
                },
                style={
                    "padding-bottom": "1px",
                    "padding-top": "2px",
                    "padding-left": "1px",
                    "padding-right": "1px",
                    "flex-grow": "1",
                    "height": "55vh",
                    "width": "100%",
                },
            )
        ]
    )


@cache.memoize(timeout=TIMEOUT)
def display_zip_plot(evnt_id: str, sdata: dict) -> html.Div:
    """Display a zipcode choropleth map of the earthquake DYFI intensities.

    Plot a zipcode choropleth map of the DYFI reported intensities of the earthquake event.

    Parameters:
    ----------

    evnt_id : String
        The USGS.gov id string of the earthquake event.
    sdata : Python dictionary
        A dictionary containing the basic event data of the selected event.

    Returns:
    -------

    html.Div which contains a dcc.Graph which contains the figure fig -- A figure containing a zipcode DYFI intensities
    choropleth map.
    """

    filename = DATA_DIR / evnt_id / "cdi_zip.csv"
    cdi_zip_df = pd.read_csv(filename)
    cdi_zip_df.rename({"# Columns: ZIP/Location": "ZIP/Location"}, axis=1, inplace=True)

    # Using NC, SC, & GA region zipcodes instead of just SC
    # zc_filename = DATA_DIR / "NC_SC_GA_region_zipcodes.geojson"
    # Used parquet file format for the zip code file because it is read in faster; geojson file read is way too slow

    # zc_filename = DATA_DIR / "NC_SC_GA_region_zipcodes.parquet"
    # sc_zip_df = gpd.read_parquet(zc_filename, columns=["geometry", "ZCTA5CE10"])

    zc_filename = DATA_DIR / ZC_DATA_PATH / "cb_2010_45_zcta510.shp"
    sc_zip_df = gpd.read_file(zc_filename)

    # sc_zip_df = gpd.read_file(r"/home/mick/Work/data_science/SC_earthquake/data/zipcode_data/cb_2010_45_zcta510.shp")

    cdi_zip_df["ZIP/Location"] = cdi_zip_df[["ZIP/Location"]].astype("str")

    # sc_zip_df["ZCTA5CE10"] = sc_zip_df[["ZCTA5CE10"]].astype("str")
    sc_zip_df["Zipcode"] = sc_zip_df[["Zipcode"]].astype("str")

    df = cdi_zip_df.copy()
    geo_dff = (
        # gpd.GeoDataFrame(sc_zip_df).merge(df, left_on="ZCTA5CE10", right_on="ZIP/Location").set_index("ZIP/Location")
        gpd.GeoDataFrame(sc_zip_df).merge(df, left_on="Zipcode", right_on="ZIP/Location")
        # .set_index("ZIP/Location")  # FIXME:  Remove this line
    )

    geo_dff = geo_dff[["Zipcode", "CDI", "Response_Count", "Hypocentral_Distance", "geometry"]]
    state_zip_json = json.loads(geo_dff.to_json())

    ww = list(df["CDI"])
    xx = list(df["ZIP/Location"])
    yy = list(df["Response_Count"])
    zz = list(df["Hypocentral_Distance"])

    nh = np.empty(shape=(len(yy), 4, 1), dtype="object")
    nh[:, 0] = np.array(xx).reshape(-1, 1)
    nh[:, 1] = np.array(yy).reshape(-1, 1)
    nh[:, 2] = np.array(zz).reshape(-1, 1)
    nh[:, 3] = np.array(ww).reshape(-1, 1)

    fig = go.Figure()
    fig.add_trace(
        go.Choroplethmapbox(
            geojson=state_zip_json,
            locations=df["ZIP/Location"],
            z=df["CDI"],
            featureidkey="properties.Zipcode",
            # featureidkey="properties.ZCTA5CE10",
            marker={"opacity": 0.3, "line_width": 0.5},
            showscale=True,
            coloraxis="coloraxis",
            name="",
            customdata=nh,
            hoverlabel={"bgcolor": "#323232"},
            hovertemplate="ZIP/Postal Code:  %{customdata[0]}<br>"
            + "Responses:  %{customdata[1]}<br>"
            + "CDI:  %{customdata[3]}"
            + " -- Distance:  %{customdata[2]} km",
        )
    )

    fig.add_trace(
        go.Scattermapbox(
            lon=[sdata["points"][0]["lon"]],
            lat=[sdata["points"][0]["lat"]],
            mode="markers+lines",
            marker={"size": 10, "symbol": ["star"]},
            name="",
            text=[sdata["points"][0]["customdata"][1]],
            hoverlabel={"bgcolor": "#323232"},
            hovertemplate="Epicenter -- Latitude:  %{lat},  Longitude:  %{lon}<br>" + "Location -- %{text}",
        )
    )

    fig.update_layout(
        # mapbox_style="open-street-map",
        mapbox_style="streets",
        mapbox_zoom=7.5,
        mapbox_center={
            "lat": sdata["points"][0]["lat"],
            "lon": sdata["points"][0]["lon"],
        },
        mapbox=dict(accesstoken=mapbox_access_token),
        autosize=True,
        margin={"r": 4, "t": 25, "l": 4, "b": 4},
        template="ggplot2",
        title=dict(font=dict(color="#2F4F4F"), text="Zipcode CDI Choropleth Map"),
        paper_bgcolor="#FFDEAD",
        hovermode="closest",
        hoverdistance=3,
        coloraxis=dict(colorscale="Portland"),
        coloraxis_colorbar=dict(
            orientation="v",
            lenmode="pixels",
            len=435,
            thicknessmode="pixels",
            thickness=10,
            xanchor="left",
            x=-0.025,
            xpad=1,
            ticks="inside",
            tickcolor="white",
            title=dict(text="CDI"),
        ),
        showlegend=False,
    )
    # return fig
    return html.Div(
        [
            dcc.Graph(
                figure=fig,
                config={
                    "scrollZoom": True,
                    "responsive": True,
                    "modeBarButtonsToRemove": [
                        "zoom",
                        "pan",
                        "select",
                        "lasso2d",
                        "toImage",
                        "autoScale",
                    ],
                },
                style={
                    "padding-bottom": "1px",
                    "padding-top": "2px",
                    "padding-left": "1px",
                    "padding-right": "1px",
                    "flex-grow": "1",
                    "height": "55vh",
                    "width": "100%",
                },
            )
        ],
        style={"width": "100%"},
    )


@cache.memoize(timeout=TIMEOUT)
def display_intensity_dist_plot(evnt_id: str) -> html.Div:
    """Display a graph of the event's DYFI reported intensities vs. hypo-central distance from the event.

    Plot a graph figure that contains a graph indicating various intensity vs. distance statistics.
      First -- Every DYFI intensity reported vs. hypo-central distance
      Second -- Intensity prediction based on the indicated equation
      Third -- Mean intensity +/- one Std. Dev. each distance bin
      Fourth -- Median Intensity for each distance bin

    Parameters:
    ----------

    evnt_id : String
        The USGS.gov id string for the earthquake event.

    Returns:
    -------

    html.Div which contains a dcc.Graph which contains the figure fig -- A figure containing four subplots:
        first -- Every DYFI reported intensity vs. hypo-central distance

        second -- Intensity prediction based on the indicated equation

        third -- Mean intensity +/- one Std. Dev. each distance bin

        fourth -- Median Intensity for each distance bin
    """

    filename = DATA_DIR / evnt_id / "dyfi_plot_atten.json"
    intensity_dist_df = pd.read_json(filename)

    fig = go.Figure()
    for dsi in range(len(intensity_dist_df)):
        dataset_df = pd.DataFrame(intensity_dist_df.datasets[dsi])
        # print(dataset_df)
        if dataset_df["class"][0] == "scatterplot1":
            sct_plt_df = dataset_df.from_records(data=dataset_df.data)
            xi = list(sct_plt_df.x)
            yi = list(sct_plt_df.y)
            ylabel = intensity_dist_df.ylabel[0]

            fig.add_trace(
                go.Scatter(
                    x=xi,
                    y=yi,
                    mode="markers",
                    marker=dict(color="rgb(148, 223, 234)", size=6),
                    name="All Reported Data",
                    customdata=xi,
                    text=yi,
                    hovertemplate="Hypocentral Dist. (km):  %{customdata}<br>" + "CDI:  %{text}",
                )
            )
            fig.update_yaxes(title_text=ylabel, range=[0, 10])
            fig.update_layout(
                yaxis=dict(tickvals=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], fixedrange=True),
                title_text="Intensity Vs. Distance",
                plot_bgcolor="#FAEBD7",
                paper_bgcolor="#FFDEAD",
            )

        elif dataset_df["class"][0] == "estimated1":
            est_plt_df = dataset_df.from_records(data=dataset_df.data)
            xi = list(est_plt_df.x)
            yi = list(est_plt_df.y)
            name = dataset_df["legend"][0]

            fig.add_trace(
                go.Scatter(
                    x=xi,
                    y=yi,
                    name=name,
                    mode="lines+markers",
                    line=dict(color="rgb(214, 86, 23)", width=2),
                    marker=dict(color="rgb(214, 86, 23)", size=6),
                    customdata=xi,
                    text=yi,
                    hovertemplate="Hypocentral Dist. (km):  %{customdata}<br>" + "Estimated CDI:  %{text:.2f}",
                )
            )

        elif dataset_df["class"][0] == "estimated2":
            est_plt_df = dataset_df.from_records(data=dataset_df.data)
            xi = list(est_plt_df.x)
            yi = list(est_plt_df.y)
            name = dataset_df["legend"][0]

            fig.add_trace(
                go.Scatter(
                    x=xi,
                    y=yi,
                    name=name,
                    mode="lines+markers",
                    line=dict(color="orange", width=2),
                    marker=dict(color="orange", size=6),
                    customdata=xi,
                    text=yi,
                    hovertemplate="Hypocentral Dist. (km):  %{customdata}<br>" + "Estimated CDI:  %{text:.2f}",
                )
            )

        elif dataset_df["class"][0] == "binned":
            mean_plt_df = dataset_df.from_records(data=dataset_df.data)

            xi = mean_plt_df.x
            yi = mean_plt_df.y
            yerr = mean_plt_df.stdev
            xlabel = intensity_dist_df.xlabel[0]
            ylabel = intensity_dist_df.ylabel[0]
            name = dataset_df["legend"][0]

            xx = list(mean_plt_df.x)
            yy = list(mean_plt_df.y)
            yyerr = list(mean_plt_df.stdev)
            nk = np.empty(shape=(len(xx), 3, 1))
            nk[:, 0] = np.array(xx).reshape(-1, 1)
            nk[:, 1] = np.array(yy).reshape(-1, 1)
            nk[:, 2] = np.array(yyerr).reshape(-1, 1)

            fig.add_trace(
                go.Scatter(
                    x=xi,
                    y=yi,
                    name=name,
                    error_y=dict(
                        type="data",
                        array=yerr,
                        color="rgb(141, 145, 235)",
                        visible=True,
                    ),
                    mode="markers",
                    marker=dict(color="rgb(141, 145, 235)", size=6),
                    customdata=nk,
                    hovertemplate="Hypocentral Dist. (km):  %{customdata[0]}<br>"
                    + "Mean CDI:  %{customdata[1]:.1f}<br>"
                    + "Std. Dev. %{customdata[2]:.2f}",
                )
            )
            fig.update_xaxes(title_text=xlabel)
            fig.update_yaxes(title_text=ylabel)

        elif dataset_df["class"][0] == "median":
            median_plt_df = dataset_df.from_records(data=dataset_df.data)
            xi = median_plt_df.x  # Distance
            yi = median_plt_df.y  # CDI
            xlabel = intensity_dist_df.xlabel[0]
            name = dataset_df["legend"][0]

            fig.add_trace(
                go.Scatter(
                    x=xi,
                    y=yi,
                    mode="markers",
                    name=name,
                    marker=dict(color="rgb(254, 77, 85)", size=6),
                    customdata=xi,
                    text=yi,
                    hovertemplate="Hypocentral Dist. (km):  %{customdata}<br>" + "Median CDI:  %{text}",
                )
            )
            fig.update_xaxes(title_text=xlabel, range=[0, max(xi)])

    fig.update_layout(
        margin={"r": 4, "t": 25, "l": 4, "b": 4},
        legend=dict(
            orientation="v",
            x=1,
            y=1.0,
            xanchor="right",
            bordercolor="Black",
            borderwidth=1.0,
        ),
    )
    # return fig
    return html.Div(
        [
            dcc.Graph(
                figure=fig,
                config={
                    "scrollZoom": True,
                    "responsive": True,
                    "displayModeBar": False,
                },
                style={
                    "padding-bottom": "1px",
                    "padding-top": "2px",
                    "padding-left": "1px",
                    "padding-right": "1px",
                    "flex-grow": "1",
                    "height": "55vh",
                    "width": "100%",
                },
            )
        ]
    )


@cache.memoize(timeout=TIMEOUT)
def display_response_time_plot(evnt_id: str) -> html.Div:
    """Display a line graph of DYFI number of responses vs. time since earthquake event.

    Plot a figure that displays a line graph showing the DYFI number of responses vs. time since earthquake.

    Parameters:
    ----------

    evnt_id : String
        The USGS.gov id string for the earthquake event.

    Returns:
    -------

    html.Div which contains a dcc.Graph which contains the graph figure fig -- A figure containing a line graph of
    responses vs. time.
    """

    filename = DATA_DIR / evnt_id / "dyfi_plot_numresp.json"
    resp_time_df = pd.read_json(filename)

    resp_time_ds_df = pd.DataFrame(resp_time_df.datasets[0])
    resp_time_plot_df = resp_time_ds_df.from_records(data=resp_time_ds_df.data)

    xi = list(resp_time_plot_df.x)
    yi = list(resp_time_plot_df.y)
    xlabel = resp_time_df.xlabel[0]
    ylabel = resp_time_df.ylabel[0]
    title = resp_time_df.title[0]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=xi,
            y=yi,
            mode="lines+markers",
            line=dict(color="green", width=2),
            marker=dict(color="green", size=6),
            hovertemplate="Responses:  %{y}<br>" + "Time Since Event:  %{x}<extra></extra>",
        )
    )
    fig.update_xaxes(title_text=xlabel)
    fig.update_yaxes(title_text=ylabel)

    fig.update_layout(
        title_text=title,
        plot_bgcolor="#FAEBD7",
        paper_bgcolor="#FFDEAD",
        template="ggplot2",
        margin={"r": 4, "t": 25, "l": 4, "b": 4},
    )

    return html.Div(
        [
            dcc.Graph(
                figure=fig,
                config={
                    "scrollZoom": False,
                    "responsive": True,
                    "displayModeBar": False,
                },
                style={
                    "padding-bottom": "1px",
                    "padding-top": "2px",
                    "padding-left": "1px",
                    "padding-right": "1px",
                    "flex-grow": "1",
                    "height": "55vh",
                    "width": "100%",
                },
            )
        ]
    )


@cache.memoize(timeout=TIMEOUT)
def display_dyfi_responses_tbl(evnt_id: str) -> html.Div:
    """Display a table of the DYFI responses information.

    Display a table of DYFI responses based on zipcode which shows the CDI intensity value, number of responses for that
    location, distance, latitude, and longitude.

    Parameters:
    ----------

    evnt_id : String
        The USGS.gov id string for the earthquake event.

    Returns:
    -------

    html.Div which contains a dbc.Table table -- Object that contains the dbc.Table
    """

    filename = DATA_DIR / evnt_id / "cdi_zip.csv"
    dyfi_responses_df = pd.read_csv(filename, index_col=False)

    table_header = [html.Thead(html.Tr([html.Th(i) for i in dyfi_responses_df.columns]))]

    table_body = [
        html.Tbody([html.Tr([html.Td(str(c)) for c in r]) for r in dyfi_responses_df.to_records(index=False)])
    ]
    # noinspection PyTypeChecker
    table = dbc.Table(table_header + table_body, striped=True, hover=True)  # Table bordered is done in style.css

    return html.Div(
        table,
        className="table-wrapper table-responsive",
        style={"width": "100%"},
        # style={"max-height": "54vh", "width": "100%"},
    )
