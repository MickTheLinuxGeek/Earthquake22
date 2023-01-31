#!/usr/bin/env python3
# encoding: utf-8

#  TODO:  Work on adding intensity and zip graph plots; Create a test app to work on and test each one first
#  TODO:  Add a data-table to the plot-dropdown
#  TODO:  Change the Event info. section from an html.Pre to a dash data-table
#  TODO:  Add program/app documentation

__version__ = "1.0.0"

import pandas as pd
import geopandas as gpd
import plotly.express as px
from dash import html, dcc, Dash, Input, Output
import dash_bootstrap_components as dbc
from datetime import datetime as dt
from datetime import date

# import numpy as np

# read in mapbox access token
px.set_mapbox_access_token(open(".mapbox_token").read())

pd.set_option('display.max_columns', 32)

geo_df = gpd.read_file('./data/20221218_SC_Earthquake.geojson')  # FIXME:  Use a generic file name

geo_df['Event_Date'] = pd.to_datetime(geo_df.time, unit="ms") \
    .dt.tz_localize('UTC') \
    .dt.tz_convert('America/New_York').dt.date

geo_df['Event_Time'] = pd.to_datetime(geo_df.time, unit="ms") \
    .dt.tz_localize('UTC') \
    .dt.tz_convert('America/New_York').dt.time

# remove decimal portion of the seconds part of the time
for x in range(len(geo_df['Event_Time'])):
    geo_df.loc[x, 'Event_Time'] = geo_df['Event_Time'][x].replace(microsecond=0)

geo_df = geo_df[['mag', 'place', 'detail', 'felt', 'cdi', 'title', 'geometry', 'Event_Date', 'Event_Time']]
geo_df = geo_df.rename(columns={'mag': 'Mag', 'place': 'Place', 'detail': 'Url', 'felt': 'Felt',
                                'cdi': 'CDI', 'title': 'Title'})  # , 'geometry': 'Geometry'})
geo_df.Felt = geo_df.Felt.fillna(0).astype('int')
geo_df.CDI = geo_df.CDI.fillna(0).astype('float')

geo_df['Depth'] = geo_df.geometry.z
geo_df['Mag'] = geo_df.Mag.round(1)

geo_df = geo_df.copy()

geo_df.head()

app = Dash(__name__)
blackbold = {'color': 'black', 'font-weight': 'bold'}

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
                            href="https://plotly.com/dash/",
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
                                    max_date_allowed=dt(2023, 1, 31),
                                    initial_visible_month=dt(2021, 12, 1),
                                    start_date=dt(2021, 12, 1).date(),
                                    end_date=dt(2023, 1, 7).date(),  # FIXME:  Change this to the current date
                                    display_format="MM-DD-Y",
                                    updatemode='bothdates',
                                    style={'border': '1px solid black', 'border-radius': '2px', 'border-spacing': '0px'}
                                    # style={"border": "1px solid black", "display": "inline-block",
                                    #        'border-radius': '2px', 'border-spacing': '0'}
                                ),
                                # html.Div(id='output-container-date-picker-range'),
                                html.Label('Min./Max. Magnitude Filter'),
                                html.Div(children=[
                                    # dbc.Label("Min."),
                                    dbc.Input(id="min-mag-input",
                                              type="number", min=1, max=10, step=0.5,
                                              size="sm",
                                              placeholder="Min.",
                                              debounce=True,
                                              value=1,
                                              autofocus=True,
                                              style={"width": "21.5%"},
                                              ),
                                    # dbc.Label("Max."),
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
                                dcc.Dropdown(id='plot-dropdown',
                                             options=['Intensity Plot', 'Zip Map', 'DYFI Responses',
                                                      'Intensity Vs. Distance', 'Response Vs. Time'],
                                             value='Intensity Plot',
                                             clearable=False,
                                             style={"width": '65%'},
                                             ),
                                html.Div(
                                    [
                                        html.Br(),
                                        html.Label(['Event Info.'], style=blackbold),
                                        html.Pre(id='event-info-pre', children=[],
                                                 style={},
                                                 # style={'white-space': 'pre-wrap', 'word-break': 'break-all',
                                                 #        'border': '1px solid black', 'text-align': 'left',
                                                 #        'padding': '1px 12px 1px 12px', 'color': 'blue',
                                                 #        'margin-top': '3px'}
                                                 ),
                                    ],
                                    style={'padding-top': '2px'},
                                ),
                            ],
                        ),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns",
                    children=[
                        dcc.Graph(id="map-graph",
                                  config={'displayModeBar': True,
                                          'scrollZoom': True,
                                          'modeBarButtonsToRemove': ['zoom', 'pan', 'select', 'lasso2d',
                                                                     'toImage']},
                                  style={'background': '#00FC87',
                                         'padding-bottom': '0px', 'padding-top': '0px',
                                         'padding-left': '2px', 'padding-right': '2px',
                                         'height': '50vh'},
                                  ),
                        dcc.Graph(id="histogram"),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(
    # Output('output-container-date-picker-range', 'children'),
    Output('map-graph', 'figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('min-mag-input', 'value'),
    Input('max-mag-input', 'value'))
def update_output(start_date, end_date, input1, input2):
    # string_prefix = 'You have selected: '
    # if start_date is not None:
    #     start_date_object = date.fromisoformat(start_date)
    #     start_date_string = start_date_object.strftime('%B %d, %Y')
    #     string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    # if end_date is not None:
    #     end_date_object = date.fromisoformat(end_date)
    #     end_date_string = end_date_object.strftime('%B %d, %Y')
    #     string_prefix = string_prefix + 'End Date: ' + end_date_string
    # if len(string_prefix) == len('You have selected: '):
    #     string_prefix = 'Select a date to see it displayed here'

    geo_dff = geo_df[(geo_df['Event_Date'] >= date.fromisoformat(start_date)) &
                     (geo_df['Event_Date'] <= date.fromisoformat(end_date)) &
                     (geo_df['Mag'] >= input1) & (geo_df['Mag'] <= input2)]

    fig = px.scatter_mapbox(geo_dff,
                            lat=geo_dff.geometry.y,
                            lon=geo_dff.geometry.x,
                            color=geo_dff.Mag,
                            custom_data=['Title', 'Place', 'Event_Date', 'Event_Time', 'Mag', 'Depth', 'Felt', 'CDI'],
                            color_continuous_scale=px.colors.sequential.Jet,
                            zoom=11.25,
                            center=dict(lat=34.170983, lon=-80.794252),
                            mapbox_style='streets',
                            title='South Carolina Earthquake Swarm Dec - 2021 to Present',
                            template='ggplot2',
                            # labels={'Mag': 'Magnitude'})
                            )

    # fig.update_layout(coloraxis_showscale=False)

    fig.update_layout(coloraxis_colorbar=dict(orientation='h',
                                              lenmode='pixels',
                                              len=435,
                                              thicknessmode='pixels',
                                              thickness=10,
                                              xanchor='left',
                                              x=0,
                                              xpad=3,
                                              yanchor='top'))

    fig.update_layout(title=dict(font=dict(color='#2F4F4F')))

    fig.update_layout(autosize=True, margin=dict(t=25, b=0, l=0, r=0))

    fig.update_layout(clickmode='event+select',
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
                      unselected={'marker': {'opacity': 1}},
                      selected={'marker': {'opacity': 0.5, 'size': 25}})
    # print(fig.data[0]['marker']['color'][92])
    # print(fig.data[0])
    # print(fig)
    return fig


# ---------------------------------------------------------------
# callback for event data
@app.callback(
    Output('event-info-pre', 'children'),
    Output('event-info-pre', 'style'),
    Input('map-graph', 'selectedData'))
def display_click_data(selectedData):
    if selectedData is None:
        return html.P("Click on any map marker"), {'white-space': 'pre-wrap', 'word-break': 'break-all',
                                                   'border': '1px solid black', 'text-align': 'center',
                                                   'padding': '1px 12px 1px 12px', 'color': 'blue',
                                                   'margin-top': '3px'}
    else:
        # print(selectedData)
        # print(selectedData['points'][0]['marker.color'])
        event_title = "Event Title:  " + selectedData['points'][0]['customdata'][0]
        event_date = "Event Date:  " + selectedData['points'][0]['customdata'][2]
        event_time = "Event Time:  " + selectedData['points'][0]['customdata'][3]
        event_loc = "Location:  " + selectedData['points'][0]['customdata'][1]
        event_mag = "Magnitude:  " + str(selectedData['points'][0]['customdata'][4])
        event_lat = "Latitude:  " + str(selectedData['points'][0]['lat'])
        event_lon = "Longitude:  " + str(selectedData['points'][0]['lon'])
        event_depth = "Depth:  " + str(selectedData['points'][0]['customdata'][5])
        event_dyfi = "DYFI:  " + str(selectedData['points'][0]['customdata'][6])

        return [html.P(event_title), html.P(event_date), html.P(event_time), html.P(event_loc),
                html.P(event_mag), html.P(event_lat), html.P(event_lon), html.P(event_depth),
                html.P(event_dyfi)], {'white-space': 'pre-wrap', 'word-break': 'break-all',
                                      'border': '1px solid black', 'text-align': 'left',
                                      'padding': '1px 12px 1px 12px',
                                      'color': 'black', 'font-weight': 'bold',
                                      'margin-top': '3px'}


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=8050)
