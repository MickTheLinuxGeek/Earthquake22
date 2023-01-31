#!/usr/bin/env python3
# encoding: utf-8

#  TODO: Add selection criteria Div/section to app layout; Based on date and then magnitude range
#  TODO: Add a selection for the plot to be viewed
#  TODO: Filter events shown on the map based on selection criteria
#  TODO: Add an empty Div below the map graph that will contain the selected plot

# In[1]:

__version__ = "1.0.0"

import pandas as pd
import geopandas as gpd
import plotly.express as px
from dash import html, dcc, Dash

# In[2]:


pd.set_option('display.max_columns', 32)

# In[3]:


# geo_df = gpd.read_file('2022-07-19-SC-Earthquake.geojson')
geo_df = gpd.read_file('./data/2022-09-03-SC-Earthquake.geojson')

# In[4]:


geo_df['Event_Date'] = pd.to_datetime(geo_df.time, unit="ms") \
    .dt.tz_localize('UTC') \
    .dt.tz_convert('America/New_York').dt.date

geo_df['Event_Time'] = pd.to_datetime(geo_df.time, unit="ms") \
    .dt.tz_localize('UTC') \
    .dt.tz_convert('America/New_York').dt.time

# In[5]:


# remove decimal portion of the seconds part of the time

for x in range(len(geo_df['Event_Time'])):
    geo_df.loc[x, 'Event_Time'] = geo_df['Event_Time'][x].replace(microsecond=0)

# In[6]:


geo_df = geo_df[['mag', 'place', 'detail', 'felt', 'cdi', 'title', 'geometry', 'Event_Date', 'Event_Time']]

# In[7]:


geo_df = geo_df.rename(columns={'mag': 'Mag', 'place': 'Place', 'detail': 'Url', 'felt': 'Felt',
                                'cdi': 'CDI', 'title': 'Title'})  # , 'geometry': 'Geometry'})

# In[8]:


geo_df.Felt = geo_df.Felt.fillna(0).astype('int')
geo_df.CDI = geo_df.CDI.fillna(0).astype('float')

# In[9]:


# geo_df.Event_Date = pd.to_datetime(geo_df.Event_Date)


# In[10]:


geo_df['Depth'] = geo_df.geometry.z

# In[11]:


geo_df = geo_df.copy()

# In[ ]:


geo_df.head()

# In[14]:


# read in mapbox access token
px.set_mapbox_access_token(open(".mapbox_token").read())

fig = px.scatter_mapbox(geo_df,
                        lat=geo_df.geometry.y,
                        lon=geo_df.geometry.x,
                        color=geo_df.Mag,
                        custom_data=['Title', 'Place', 'Event_Date', 'Event_Time', 'Mag', 'Depth', 'Felt', 'CDI'],
                        size=geo_df.Mag,
                        # color_continuous_scale = px.colors.cyclical.Phase,
                        color_continuous_scale=px.colors.sequential.Jet,
                        zoom=11,
                        center=dict(lat=34.170983, lon=-80.794252),
                        mapbox_style='streets',
                        title='South Carolina Earthquake Swarm Dec - 2021 to Present',
                        # height=510,
                        template='ggplot2',
                        labels={'Mag': 'Magnitude'})

fig.update_layout(font=dict(family="Times New Roman",
                            size=12,
                            color="White"))

fig.update_layout(paper_bgcolor="#8B4513",
                  autosize=True,
                  margin=dict(t=50, b=5, l=5, r=5),
                  title_font_color="#00FF7F",
                  title_font_family="Courier New, monospace",
                  title_font_size=16)

fig.update_traces(hovertemplate="<br>".join(["Event Title: %{customdata[0]}",
                                             "Event Date: %{customdata[2]}",
                                             "Event Time: %{customdata[3]}",
                                             "Location: %{customdata[1]}",
                                             "Magnitude: %{customdata[4]}",
                                             "Lat:  %{lat},  " + "Lon:  %{lon}    " +
                                             "Depth(km):  %{customdata[5]}",
                                             "DYFI: %{customdata[6]}"]))

# fig.show()

app = Dash(__name__)
app.layout = html.Div([
    html.Div([
        html.H2("SC Earthquake Swarm Information App",
                style={'text-align': 'center', 'color': 'SteelBlue'}),
    ]),
    html.Div([
        dcc.Graph(figure=fig,
                  config={'displayModeBar': False, 'scrollZoom': True},
                  style={'padding-bottom': '2px', 'padding-left': '2px', 'height': '50vh', 'width': '50vw'}
                  )
        ],  # className="five columns offset-by-six"
    ),
])

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=8050)
