#!/usr/bin/env python3
# encoding: utf-8

#  TODO:  Add program/app documentation


__author__ = "Michael Biel"
__copyright__ = "Copyright 2023, The Earthquake Vis. Project"
__license__ = ""
__version__ = "1.0.0"
__maintainer__ = "Michael Biel"
__email__ = "mick.the.linux.geek@hotmail.com"
__status__ = "development"

import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import html, dcc, Dash, Input, Output
import dash_bootstrap_components as dbc
from datetime import datetime as dt
from datetime import date
import json
from pathlib import Path
import numpy as np

DATA_DIR = Path(r"./data")
ZC_DATA_PATH = Path(r"zipcode_data")

rowEvenColor = 'Wheat'
rowOddColor = 'NavajoWhite'

loading_style = {'position': 'absolute', 'align-self': 'center'}

select_graph = go.Figure()
select_graph = select_graph.update_layout(
    plot_bgcolor='AntiqueWhite',
    paper_bgcolor='#FFDEAD',
    xaxis={"visible": False},
    yaxis={"visible": False},
    annotations=[
        {"text": "Filter events displayed by using the date and magnitude filters.<br>" +
            "<br>Select an event marker from the map and a plot type from the dropdown for more event information.",
         "xref": "paper",
         "yref": "paper",
         "showarrow": False,
         "font": {"size": 28}}
    ]
)

# read in mapbox access token
# px.set_mapbox_access_token(open(".mapbox_token").read())  FIXME:  Remove
mapbox_access_token = open(".mapbox_token").read()

# Uncomment this line to display all dataframe columns in the console.
pd.set_option('display.max_columns', 32)

event_file = DATA_DIR / "SC_Earthquake.geojson"
geo_df = gpd.read_file(event_file)

geo_df['Event_Date'] = pd.to_datetime(geo_df.time, unit="ms") \
    .dt.tz_localize('UTC') \
    .dt.tz_convert('America/New_York').dt.date

geo_df['Event_Time'] = pd.to_datetime(geo_df.time, unit="ms") \
    .dt.tz_localize('UTC') \
    .dt.tz_convert('America/New_York').dt.time

# remove decimal portion of the seconds part of the time
for x in range(len(geo_df['Event_Time'])):
    geo_df.loc[x, 'Event_Time'] = geo_df['Event_Time'][x].replace(microsecond=0)

# Filtered the eq event id into the dataframe
geo_df = geo_df[['id', 'mag', 'place', 'detail', 'felt', 'cdi', 'title', 'geometry', 'Event_Date', 'Event_Time']]
geo_df = geo_df.rename(columns={'mag': 'Mag', 'place': 'Place', 'detail': 'Url', 'felt': 'Felt',
                                'cdi': 'CDI', 'title': 'Title'})  # , 'geometry': 'Geometry'})
geo_df.Felt = geo_df.Felt.fillna(0).astype('int')
geo_df.CDI = geo_df.CDI.fillna(0).astype('float')

geo_df['Depth'] = geo_df.geometry.z
geo_df['Mag'] = geo_df.Mag.round(1)

geo_df = geo_df.copy()

print(geo_df.head())  # FIXME Remove this line when finished

blackbold = {'color': 'black', 'font-weight': 'bold'}

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.A(
                            html.Img(
                                className="logo",
                                src=app.get_asset_url("dash-logo-new.png"),
                            ),
                            # href="https://plotly.com/dash/",
                        ),
                        html.H3("DASH - EARTHQUAKE DATA APP"),
                        dbc.Label("""Date Range Filter"""),
                        html.Div(
                            # className="div-for-dropdown",
                            children=[
                                dcc.DatePickerRange(
                                    id="my-date-picker-range",
                                    calendar_orientation='horizontal',
                                    min_date_allowed=dt(2021, 12, 1),
                                    max_date_allowed=date.today(),
                                    initial_visible_month=dt(2021, 12, 1),
                                    start_date=dt(2021, 12, 1).date(),
                                    end_date=date.today(),
                                    display_format="MM-DD-Y",
                                    updatemode='bothdates',
                                    style={'border': '1px solid black', 'border-radius': '2px', 'border-spacing': '0px'}
                                ),
                                html.Label('Min./Max. Magnitude Filter'),
                                html.Div(children=[
                                    dbc.Input(id="min-mag-input",
                                              type="number", min=1, max=10, step=0.5,
                                              size="sm",
                                              placeholder="Min.",
                                              debounce=True,
                                              value=1,
                                              autofocus=True,
                                              style={"width": "21.5%"},
                                              ),
                                    dbc.Input(id="max-mag-input",
                                              type="number", min=1, max=10, step=0.5,
                                              size="sm",
                                              placeholder="Max.",
                                              debounce=True,
                                              value=10,
                                              style={"width": "21.5%"},
                                              ),
                                ], style={'display': 'flex'}
                                ),
                                html.Label("Plot Type"),
                                dcc.Dropdown(id='plot-type-dropdown',
                                             options=['Intensity Plot', 'Zip Map', 'Intensity Vs. Distance',
                                                      'Response Vs. Time', 'DYFI Responses'],
                                             value='Intensity Plot',
                                             clearable=False,
                                             style={"width": '65%'},
                                             ),
                            ],
                        ),
                    ],
                ),
                # Column for app map and graph plots
                html.Div(
                    className="eight columns",
                    children=[
                        dcc.Graph(id="map-graph",
                                  config={'displayModeBar': True,
                                          'scrollZoom': True,
                                          'modeBarButtonsToRemove': ['zoom', 'pan', 'select', 'lasso2d',
                                                                     'toImage']},
                                  style={'padding-bottom': '2px', 'padding-top': '1px',
                                         'padding-left': '2px', 'padding-right': '2px',
                                         'height': '45vh'},
                                  ),
                        ],
                ),
                html.Div(
                    className="twelve columns",
                    children=[
                        dcc.Graph(id="graph-plot",
                                  config={'displayModeBar': False,
                                          'scrollZoom': False,
                                          'modeBarButtonsToRemove': ['zoom', 'pan', 'select', 'lasso2d', 'toImage']},
                                  style={'padding-bottom': '1px', 'padding-top': '2px',
                                         'padding-left': '1px', 'padding-right': '1px', 'flex-grow': '1',
                                         'height': '512px'},
                                  ),
                        dcc.Loading(id='loading', parent_style=loading_style, type='default'),
                        ],
                    style={'position': 'relative', 'display': 'flex', 'justify-content': 'center'},
                ),
            ],
        ),
    ],
)


@app.callback(
    Output('map-graph', 'figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('min-mag-input', 'value'),
    Input('max-mag-input', 'value'))
def update_output(start_date, end_date, input1, input2):
    """ Map callback function

    Callback function that returns a map figure based on the date range and magnitude range inputs.

    Parameters
    ----------
    start_date : datetime.datetime.date
        Start date of date range filter
    end_date : datetime.datetime.date
        End date of date range filter
    input1 : int
        Minimum magnitude value for filter
    input2 : int
        Maximum magnitude value for filter

    Returns
    -------
    plotly.graph_objects.Figure
        fig -- The Plotly Express scatter mapbox map figure object

    """
    geo_dff = geo_df[(geo_df['Event_Date'] >= date.fromisoformat(start_date)) &
                     (geo_df['Event_Date'] <= date.fromisoformat(end_date)) &
                     (geo_df['Mag'] >= input1) & (geo_df['Mag'] <= input2)]

    fig = px.scatter_mapbox(geo_dff,
                            lat=geo_dff.geometry.y,
                            lon=geo_dff.geometry.x,
                            color=geo_dff.Mag,
                            custom_data=['Title', 'Place', 'Event_Date', 'Event_Time', 'Mag', 'Depth', 'Felt', 'CDI',
                                         'id'],
                            color_continuous_scale=px.colors.sequential.Jet,
                            zoom=11.25,
                            center=dict(lat=34.170983, lon=-80.794252),
                            # mapbox_style='streets',  # FIXME:  Remove
                            title='South Carolina Earthquake Swarm Dec - 2021 to Present',
                            template='ggplot2')

    fig.update_layout(mapbox_style="streets", mapbox_accesstoken=mapbox_access_token)

    fig.update_layout(coloraxis_colorbar=dict(orientation='h',
                                              lenmode='pixels',
                                              len=435,
                                              thicknessmode='pixels',
                                              thickness=10,
                                              xanchor='left',
                                              x=0,
                                              xpad=3,
                                              yanchor='top'))

    fig.update_layout(title=dict(font=dict(color='#2F4F4F')),
                      autosize=True,
                      margin=dict(t=25, b=0, l=0, r=0),
                      clickmode='event+select',
                      paper_bgcolor='#FAEBD7',
                      uirevision='foo',
                      hovermode='closest',
                      hoverdistance=2)

    fig.update_traces(hovertemplate="<br>".join(["Event Title: %{customdata[0]}",
                                                 "Event Date: %{customdata[2]}",
                                                 "Event Time: %{customdata[3]}",
                                                 "Location: %{customdata[1]}",
                                                 "Magnitude: %{customdata[4]}",
                                                 "Lat:  %{lat},  " + "Lon:  %{lon}    " +
                                                 "Depth(km):  %{customdata[5]}",
                                                 "DYFI: %{customdata[6]}"]))

    fig.update_traces(mode='markers',
                      marker={'size': 10},
                      unselected={'marker': {'opacity': 0.75}},
                      selected={'marker': {'opacity': 1, 'size': 25}})
    return fig


# graph-plot functions
def display_intensity_plot(evnt_id, sdata):
    """ Display 1km and 10km spacing choropleth map of earthquake DYFI intensities

    Plots a 1km and a 10 km spacing choropleth map of the DYFI earthquake intensities for selected event.

    Parameters
    ----------
    evnt_id : String
        The event id identifying the selected earthquake event.
    sdata : Python dictionary
        A dictionary containing the basic event data of the selected event.

    Returns
    -------
    plotly.graph_objects.Figure
        fig -- A figure containing a 1km spacing and a 10 km spacing choropleth map.

    """
    filename = DATA_DIR / evnt_id / "dyfi_geo_1km.geojson"
    print(filename)  # FIXME:  Remove after testing

    with open(filename) as file1:
        cdi_geo_1km_geojson = json.load(file1)
    cdi_geo_1km_df = pd.json_normalize(cdi_geo_1km_geojson, ['features'])

    print(cdi_geo_1km_df)  # FIXME:  Remove after testing

    filename = DATA_DIR / evnt_id / "dyfi_geo_10km.geojson"
    print(filename)  # FIXME:  Remove after testing

    with open(filename) as file2:
        cdi_geo_10km_geojson = json.load(file2)

    cdi_geo_10km_df = pd.json_normalize(cdi_geo_10km_geojson, ['features'])

    print(cdi_geo_10km_df)  # FIXME:  Remove after testing

    fig = make_subplots(rows=1, cols=2, subplot_titles=['CDI Choropleth Mapbox Plot - 1km Spacing',
                                                        'CDI Choropleth Mapbox Plot - 10km Spacing'],
                        column_widths=[0.5, 0.5],
                        horizontal_spacing=0.004,
                        specs=[[{"type": "mapbox"}, {"type": "mapbox"}]])

    fig.add_trace(go.Choroplethmapbox(geojson=cdi_geo_1km_geojson,
                                      locations=cdi_geo_1km_df['properties.name'],
                                      z=cdi_geo_1km_df['properties.cdi'],
                                      featureidkey='properties.name',
                                      subplot="mapbox",
                                      coloraxis="coloraxis",
                                      below="", name='',
                                      text=list(cdi_geo_1km_df['properties.name']),
                                      hovertemplate='UTM Geocode/City: %{text}<br>' +
                                                    'CDI: %{z}',
                                      marker=dict(opacity=0.50)), row=1, col=1)

    fig.add_trace(go.Choroplethmapbox(geojson=cdi_geo_10km_geojson,
                                      locations=cdi_geo_10km_df['properties.name'],
                                      z=cdi_geo_10km_df['properties.cdi'],
                                      featureidkey='properties.name',
                                      subplot="mapbox2",
                                      coloraxis="coloraxis",
                                      name='',
                                      text=list(cdi_geo_10km_df['properties.name']),
                                      hovertemplate='UTM Geocode/City: %{text}<br>' +
                                                    'CDI: %{z}',
                                      marker=dict(opacity=0.50)), row=1, col=2)

    fig.add_trace(go.Scattermapbox(lon=[sdata['points'][0]['lon']],
                                   lat=[sdata['points'][0]['lat']],
                                   showlegend=False,
                                   subplot="mapbox",
                                   mode='markers+lines',
                                   marker={'size': 12, 'opacity': 1, 'symbol': ['star']},
                                   name='',
                                   hoverlabel={'bgcolor': 'DimGrey'},
                                   hovertemplate='Epicenter:  %{lon}, %{lat}'))

    fig.add_trace(go.Scattermapbox(lon=[sdata['points'][0]['lon']],
                                   lat=[sdata['points'][0]['lat']],
                                   showlegend=False,
                                   subplot="mapbox2",
                                   mode='markers+lines',
                                   marker={'size': 12, 'opacity': 1, 'symbol': ['star']},
                                   name='',
                                   hoverlabel={'bgcolor': 'DimGrey'},
                                   hovertemplate='Epicenter:  %{lon}, %{lat}'))

    fig.update_layout(mapbox1=dict(zoom=7.5, style='streets', center={"lat": 34.0007, "lon": -81.0348},
                                   accesstoken=mapbox_access_token),
                      mapbox2=dict(zoom=7.5, style='streets', center={"lat": 34.0007, "lon": -81.0348},
                                   accesstoken=mapbox_access_token),
                      coloraxis=dict(colorscale='Plotly3'),
                      coloraxis_colorbar=dict(orientation='v', lenmode='pixels', len=435, thicknessmode='pixels',
                                              thickness=10, xanchor='left', x=-0.025, xpad=1, ticks='inside',
                                              tickcolor='white', title=dict(text='CDI')),
                      showlegend=False,
                      paper_bgcolor='#FFDEAD',
                      hovermode='closest', hoverdistance=5,
                      margin={"r": 4, "t": 25, "l": 4, "b": 4})
    return fig


def display_zip_plot(evnt_id, sdata):
    """ Display a zipcode choropleth map of the earthquake DYFI intensities.

    Plot a zipcode choropleth map of the DYFI reported intensities of the earthquake event.

    Parameters
    ----------
    evnt_id : String
        The USGS.gov id string of the earthquake event.
    sdata : Python dictionary
        A dictionary containing the basic event data of the selected event.

    Returns
    -------
    plotly.graph_objects.Figure
        fig -- A figure containing a zipcode DYFI intensities choropleth map.

    """
    filename = DATA_DIR / evnt_id / "cdi_zip.csv"
    cdi_zip_df = pd.read_csv(filename)
    cdi_zip_df.rename({'# Columns: ZIP/Location': 'ZIP/Location'}, axis=1, inplace=True)

    zc_filename = DATA_DIR / ZC_DATA_PATH / "tl_2010_45_zcta510.shp"
    sc_zip_df = gpd.read_file(zc_filename)

    cdi_zip_df['ZIP/Location'] = cdi_zip_df[['ZIP/Location']].astype('str')
    sc_zip_df['ZCTA5CE10'] = sc_zip_df[['ZCTA5CE10']].astype('str')
    df = cdi_zip_df
    geo_dff = gpd.GeoDataFrame(sc_zip_df).merge(df, left_on="ZCTA5CE10", right_on='ZIP/Location').set_index('ZIP/Location')

    state_zip_json = json.loads(geo_dff.to_json())

    df['ZIP/Location'] = df[['ZIP/Location']].astype('str')
    df.set_index('ZIP/Location')
    fig = go.Figure()
    fig.add_choroplethmapbox(geojson=state_zip_json, locations=df['ZIP/Location'], z=df['CDI'],
                             colorscale='Plotly3',
                             featureidkey='properties.ZCTA5CE10',
                             marker={'opacity': 0.5, 'line_width': 0},
                             showscale=True,
                             name='',
                             customdata=df['ZIP/Location'],
                             text=list(df['CDI']),
                             hovertemplate="ZIP/Postal Code:  %{customdata}<br>" +
                                           "CDI:  %{text}",
                             colorbar=dict(orientation='v', lenmode='pixels', len=435, thicknessmode='pixels',
                                           thickness=10, xanchor='left', x=-0.025, xpad=1, ticks='inside',
                                           tickcolor='white', title=dict(text='CDI',)))

    fig.add_trace(go.Scattermapbox(lon=[sdata['points'][0]['lon']],
                                   lat=[sdata['points'][0]['lat']],
                                   mode='markers+lines',
                                   marker={'size': 10, 'symbol': ['star']},
                                   name='',
                                   hoverlabel={'bgcolor': 'DimGrey'},
                                   hovertemplate='Epicenter:  %{lon}, %{lat}'))

    fig.update_layout(mapbox_style="streets",  # "open-street-map",
                      mapbox_zoom=7.5, mapbox_center={"lat": 34.0007, "lon": -81.0348},
                      mapbox=dict(accesstoken=mapbox_access_token),
                      autosize=True,
                      margin={"r": 4, "t": 25, "l": 4, "b": 4},
                      template='ggplot2',
                      title=dict(font=dict(color='#2F4F4F'), text="Zipcode CDI Choropleth Map"),
                      paper_bgcolor='#FFDEAD',
                      hovermode='closest', hoverdistance=3)
    return fig


def display_intensity_dist_plot(evnt_id):
    """ Display a graph of the event's DYFI reported intensities vs. hypo-central distance from the event.

    Plot a graph figure that contains four subplots indicating various intensity vs. distance statistics.

    Parameters
    ----------
    evnt_id : String
        The USGS.gov id string for the earthquake event.

    Returns
    -------
    plotly.graph_objects.Figure
        fig -- A figure containing four subplots: first -- Every DYFI reported intensity vx. hypo-central distance
                                                  second -- Intensity prediction based on the indicated equation
                                                  third -- Mean intensity +/- one Std. Dev. each distance bin
                                                  fourth -- Median Intensity for each distance bin

    """
    filename = DATA_DIR / evnt_id / "dyfi_plot_atten.json"
    intensity_dist_df = pd.read_json(filename)

    print(len(intensity_dist_df), intensity_dist_df)  # FIXME:  Remove after testing

    fig = make_subplots(rows=2, cols=2, subplot_titles=('All Reported Data',
                                                        'Estimated Intensity',
                                                        'Mean Intensity',
                                                        'Median Intensity Each Distance Bin'),
                        row_heights=[0.5, 0.5],
                        column_widths=[0.5, 0.5],
                        horizontal_spacing=0.06,
                        vertical_spacing=0.16,
                        specs=[[{"type": "xy"}, {"type": "xy"}], [{"type": "xy"}, {"type": "xy"}]])

    for dsi in range(len(intensity_dist_df)):
        dataset_df = pd.DataFrame(intensity_dist_df.datasets[dsi])
        # print(dataset_df)  # FIXME:  Remove after testing
        if dataset_df['class'][0] == 'scatterplot1':
            sct_plt_df = dataset_df.from_records(data=dataset_df.data)
            xi = list(sct_plt_df.x)
            yi = list(sct_plt_df.y)
            # xlabel = intensity_dist_df.xlabel[0]
            ylabel = intensity_dist_df.ylabel[0]

            fig.add_trace(go.Scatter(x=xi, y=yi, mode='markers', marker=dict(color='green', size=6),
                                     name='All Reported Data', customdata=xi, text=yi,
                                     hovertemplate="Hypocentral Dist. (km):  %{customdata}<br>" +
                                                   "CDI:  %{text}"), row=1, col=1)
            fig.update_yaxes(title_text=ylabel, range=[0, 10], row=1, col=1)
            fig.update_layout(yaxis=dict(tickvals=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], fixedrange=True),
                              title_text="Intensity Vs. Distance",
                              plot_bgcolor='#FAEBD7', paper_bgcolor='#FFDEAD',
                              legend=dict(orientation='h', xanchor='left', yanchor='top', x=0.25, y=1.15,
                                          bordercolor='Black', borderwidth=1))

        elif dataset_df['class'][0] == 'estimated1':
            est_plt_df = dataset_df.from_records(data=dataset_df.data)
            xi = list(est_plt_df.x)
            yi = list(est_plt_df.y)
            # xlabel = intensity_dist_df.xlabel[0]
            # ylabel = intensity_dist_df.ylabel[0]
            name = dataset_df['legend'][0]

            fig.add_trace(go.Scatter(x=xi, y=yi, name=name, mode='lines+markers', line=dict(color='green', width=2),
                                     marker=dict(color='green', size=6),
                                     customdata=xi, text=yi,
                                     hovertemplate="Hypocentral Dist. (km):  %{customdata}<br>" +
                                                   "Estimated CDI:  %{text:.2f}"), row=1, col=2)

        elif dataset_df['class'][0] == 'estimated2':
            est_plt_df = dataset_df.from_records(data=dataset_df.data)
            xi = list(est_plt_df.x)
            yi = list(est_plt_df.y)
            # xlabel = intensity_dist_df.xlabel[0]
            # ylabel = intensity_dist_df.ylabel[0]
            name = dataset_df['legend'][0]

            fig.add_trace(go.Scatter(x=xi, y=yi, name=name, mode='lines+markers', line=dict(color='orange', width=2),
                                     marker=dict(color='orange', size=6),
                                     customdata=xi, text=yi,
                                     hovertemplate="Hypocentral Dist. (km):  %{customdata}<br>" +
                                                   "Estimated CDI:  %{text:.2f}"), row=1, col=2)

        elif dataset_df['class'][0] == 'binned':
            mean_plt_df = dataset_df.from_records(data=dataset_df.data)
            print(mean_plt_df)  # FIXME:  Remove after testing
            xi = mean_plt_df.x
            yi = mean_plt_df.y
            yerr = mean_plt_df.stdev
            xlabel = intensity_dist_df.xlabel[0]
            ylabel = intensity_dist_df.ylabel[0]
            name = dataset_df['legend'][0]

            xx = list(mean_plt_df.x)
            yy = list(mean_plt_df.y)
            yyerr = list(mean_plt_df.stdev)
            nk = np.empty(shape=(len(xx), 3, 1))
            nk[:, 0] = np.array(xx).reshape(-1, 1)
            nk[:, 1] = np.array(yy).reshape(-1, 1)
            nk[:, 2] = np.array(yyerr).reshape(-1, 1)

            fig.add_trace(go.Scatter(x=xi, y=yi, name=name,
                                     error_y=dict(type='data', array=yerr, color='#778899', visible=True),
                                     mode='markers',
                                     marker=dict(color='blue', size=6),
                                     customdata=nk,
                                     hovertemplate="Hypocentral Dist. (km):  %{customdata[0]}<br>" +
                                                   "Mean CDI:  %{customdata[1]}<br>" +
                                                   "Std. Dev. %{customdata[2]:.2f}"), row=2, col=1)
            fig.update_xaxes(title_text=xlabel, row=2, col=1)
            fig.update_yaxes(title_text=ylabel, row=2, col=1)

        elif dataset_df['class'][0] == 'median':
            median_plt_df = dataset_df.from_records(data=dataset_df.data)
            xi = median_plt_df.x
            yi = median_plt_df.y
            xlabel = intensity_dist_df.xlabel[0]
            # ylabel = intensity_dist_df.ylabel[0]
            name = dataset_df['legend'][0]

            fig.add_trace(go.Scatter(x=xi, y=yi, mode='markers', name=name,
                                     marker=dict(color='red', size=6),
                                     customdata=xi, text=yi,
                                     hovertemplate="Hypocentral Dist. (km):  %{customdata}<br>" +
                                                   "Median CDI:  %{text}"), row=2, col=2)
            fig.update_xaxes(title_text=xlabel, row=2, col=2)

    fig.update_layout(margin={"r": 5, "t": 20, "l": 5, "b": 50})
    return fig


def display_response_time_plot(evnt_id):
    """ Display a line graph of DYFI number of responses vs. time since earthquake event.

     Plot a figure that displays a line graph showing the DYFI number of responses vs. time since earthquake.

     Parameters
     ----------
     evnt_id : String
         The USGS.gov id string for the earthquake event.

     Returns
     -------
     plotly.graph_objects.Figure
         fig -- A figure containing a line graph of responses vs. time.

     """
    filename = DATA_DIR / evnt_id / "dyfi_plot_numresp.json"
    resp_time_df = pd.read_json(filename)

    print(len(resp_time_df), resp_time_df)  # FIXME:  Remove after testing

    resp_time_ds_df = pd.DataFrame(resp_time_df.datasets[0])

    print(resp_time_ds_df)  # FIXME:  Remove after testing
    resp_time_plot_df = resp_time_ds_df.from_records(data=resp_time_ds_df.data)

    xi = list(resp_time_plot_df.x)
    yi = list(resp_time_plot_df.y)
    xlabel = resp_time_df.xlabel[0]
    ylabel = resp_time_df.ylabel[0]
    title = resp_time_df.title[0]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xi, y=yi, mode='lines+markers', line=dict(color='green', width=2),
                             marker=dict(color='green', size=6),
                             hovertemplate='Responses:  %{y}<br>' +
                                           'Time Since Event:  %{x}<extra></extra>'))
    fig.update_xaxes(title_text=xlabel)
    fig.update_yaxes(title_text=ylabel)

    fig.update_layout(title_text=title,
                      plot_bgcolor='#FAEBD7',
                      paper_bgcolor='#FFDEAD',
                      margin={"r": 4, "t": 25, "l": 4, "b": 4})

    return fig


def display_dyfi_responses_tbl(evnt_id):
    """ Display a table of the DYFI responses information.

    Display a table of DYFI responses based on zipcode which shows the CDI intensity value, number of responses for that
    location, distance, latitude, and longitude.

    Parameters
    ----------
    evnt_id : String
        The USGS.gov id string for the earthquake event.

    Returns
    -------
    plotly.graph_objects.Figure
        fig -- A figure which contains a plotly.graph_objects.Table which contains the DYFI responses info.

    """
    filename = DATA_DIR / evnt_id / "cdi_zip.csv"
    dyfi_responses_df = pd.read_csv(filename)

    dyfi_responses_df.State.fillna('No State', inplace=True)

    fig = go.Figure(data=[go.Table(header=dict(values=list(dyfi_responses_df.columns),
                                               line_color='darkslategray',
                                               fill_color='SandyBrown',
                                               line={'color': '#483D8B', 'width': 2},
                                               align='left'),
                                   cells=dict(values=[dyfi_responses_df['ZIP/Location'],
                                                      dyfi_responses_df.CDI,
                                                      dyfi_responses_df['Response_Count'],
                                                      dyfi_responses_df['Hypocentral_Distance'],
                                                      dyfi_responses_df.Latitude,
                                                      dyfi_responses_df.Longitude,
                                                      dyfi_responses_df.City,
                                                      dyfi_responses_df.State],
                                              line={'color': '#483D8B', 'width': 2},
                                              line_color='darkslategray',
                                              fill_color=[[rowOddColor, rowEvenColor, rowOddColor, rowEvenColor,
                                                           rowOddColor, rowEvenColor, rowOddColor, rowEvenColor]*len(dyfi_responses_df)],
                                              align='left',
                                              ))
                          ])

    fig.update_layout(title_text='Did You Feel It (DYFI) Responses',
                      plot_bgcolor='#FAEBD7',
                      paper_bgcolor='#FFDEAD',
                      autosize=False,
                      margin={"r": 20, "t": 35, "l": 5, "b": 25})

    return fig


@app.callback(Output("graph-plot", "figure"),
              Output("loading", 'parent_style'),
              Input("map-graph", "selectedData"),
              Input("plot-type-dropdown", "value"),
              prevent_initial_call=False)
def plot_graphs(selectedData, user_input):
    """ graph-plot callback function

    Callback function that returns and displays the graph plot that is selected.

    Parameters
    ----------
    selectedData : Python dictionary
        A Python dictionary containing the event data of the selected point on the map.
    user_input : string
        A string representing the graph plot type selected from the dropdown.

    Returns
    -------
    plotly.graph_objects.Figure
        fig -- A figure object containing the graph to be plotted.
    A Python dictionary
        new_loading_style -- The style dictionary for the dcc.Loading component.

    """
    new_loading_style = loading_style
    if selectedData is None:
        return select_graph, new_loading_style
    else:
        event_id = selectedData['points'][0]['customdata'][8]

        print(selectedData['points'][0]['lat'], selectedData['points'][0]['lon'])  # FIXME:  Remove after testing
        print(selectedData, user_input, event_id)  # FIXME:  Remove after testing
        print(new_loading_style)

        if event_id and user_input == "Intensity Plot":
            return display_intensity_plot(event_id, selectedData), new_loading_style
        elif event_id and user_input == "Zip Map":
            return display_zip_plot(event_id, selectedData), new_loading_style
        elif event_id and user_input == "Intensity Vs. Distance":
            return display_intensity_dist_plot(event_id), new_loading_style
        elif event_id and user_input == "Response Vs. Time":
            return display_response_time_plot(event_id), new_loading_style
        elif event_id and user_input == "DYFI Responses":
            return display_dyfi_responses_tbl(event_id), new_loading_style


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=8050)
