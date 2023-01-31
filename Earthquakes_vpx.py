#!/usr/bin/env python
# coding: utf-8

# In[73]:


import pandas as pd
import geopandas as gpd
import geojson
import plotly.express as px

# In[74]:


pd.set_option('display.max_columns', 32)

# In[75]:


# geo_df = gpd.read_file('2022-07-19-SC-Earthquake.geojson')
# geo_df = gpd.read_file('./data/2022-09-03-SC-Earthquake.geojson')
geo_df = gpd.read_file(r'./data/20221218_SC_Earthquake.geojson')

# In[76]:


# geo_df.columns


# In[77]:


geo_df['Event_Date'] = pd.to_datetime(geo_df.time, unit="ms") \
    .dt.tz_localize('UTC') \
    .dt.tz_convert('America/New_York').dt.date

geo_df['Event_Time'] = pd.to_datetime(geo_df.time, unit="ms") \
    .dt.tz_localize('UTC') \
    .dt.tz_convert('America/New_York').dt.time

# In[78]:


# remove decimal portion of the seconds part of the time

for x in range(len(geo_df['Event_Time'])):
    geo_df.loc[x, 'Event_Time'] = geo_df['Event_Time'][x].replace(microsecond=0)

# In[79]:


geo_df = geo_df[['mag', 'place', 'detail', 'felt', 'cdi', 'title', 'geometry', 'Event_Date', 'Event_Time']]

# In[80]:


geo_df = geo_df.rename(columns={'mag': 'Mag', 'place': 'Place', 'detail': 'Url', 'felt': 'Felt',
                                'cdi': 'CDI', 'title': 'Title'})  # , 'geometry': 'Geometry'})

# In[81]:


geo_df.Felt = geo_df.Felt.fillna(0).astype('int')
geo_df.CDI = geo_df.CDI.fillna(0).astype('float')

# In[82]:


# Fix this to make it a date type
# geo_df.Event_Date = pd.to_datetime(geo_df.Event_Date)


# In[83]:


geo_df['Depth'] = geo_df.geometry.z

# In[84]:


geo_df = geo_df.copy()

# In[85]:


geo_df.head()

# In[87]:


# read in mapbox access token
px.set_mapbox_access_token(open(r".mapbox_token").read())

fig = px.scatter_mapbox(geo_df,
                        lat=geo_df.geometry.y,
                        lon=geo_df.geometry.x,
                        color=geo_df.Mag,
                        custom_data=['Title', 'Place', 'Event_Date', 'Event_Time', 'Mag', 'Depth', 'Felt', 'CDI'],
                        size=geo_df.Mag,
                        color_continuous_scale=px.colors.sequential.Jet,
                        zoom=11,
                        center=dict(lat=34.170983, lon=-80.794252),
                        mapbox_style='dark',
                        title='South Carolina Earthquake Swarm Dec - 2021 to Present',
                        height=510,
                        template='ggplot2',
                        labels={'Mag': 'Magnitude'})

# Sets the global font. Note that fonts used in traces and other layout components inherit from the global font.
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

fig.show()

# In[88]:


# import plotly.io as pio
# pio.templates


# In[89]:


# Save geo_df without the Event_Date and Event_Time columns by dropping those columns.
# Saved to a new GeoDataFrame - shape_df which is saved to a shapefile

# shape_df = geo_df.drop(columns = ['Event_Date', 'Event_Time'], axis = 1)


# In[90]:


# Save GeoDataFrame to an ESRI shapefile
# Save earthquake points to an ESRI shapefile to be loaded into QGIS

# shape_df.to_file('./data/2022-08-07_SC_Earthquakes.shp')
