import pandas as pd
import re
import numpy as np
import pyproj
from bokeh.plotting import figure, show, output_file
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models import ColumnDataSource
import geopy
import geopy.distance
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

path = '/Users/ljohnson/repo/livjab/food-desert-DS-liv/food_desert/'
business_csv = path + 'clean.csv'
df_test = pd.read_csv(business_csv)

#change to a different map projection
project_projection = pyproj.Proj("+init=EPSG:3857") # Output map projections
google_projection = pyproj.Proj("+init=EPSG:4326") # Input map projections

# Save Coordinates to a list
longitude = df_test['LONGITUDE'].values
latitude = df_test['LATITUDE'].values

# Output mercator map projections where x=longitude and y=latitude
x, y = pyproj.transform(google_projection, project_projection, longitude, latitude)

#Bokeh plot

# HTML file
output_file('market_location.html')
# Name of tile used for plotting
tile = get_provider(Vendors.STAMEN_TERRAIN)

# Instantiate the figure
p = figure(plot_width=1000, plot_height=1000, x_axis_type = "mercator", y_axis_type = "mercator")

# Define the data to a dictionary
source = ColumnDataSource(data = dict(lat=y,lon=x))

# Add the tile/map
p.add_tile(tile)
# Plot it to the tile
p.circle(x='lon', y='lat', source=source, alpha=0.1)

# Display the map
show(p)

#GEOPY - Get the distance of 'n' miles

def travel(lat, lon, bearing=0, miles=0.5):
    # Starting point
    start = geopy.Point(lat, lon)

    # Initialized with a distance of 2 mi.
    d = geopy.distance.geodesic(miles=miles)

    # Destination method which takes the starting point and bearings(North=0).
    # Return coordinates from start to distance,d, traveled
    coord = d.destination(point=start, bearing=bearing)
    return coord
    # printing(coord) gives degrees, min, and sec
    # Slice it coord gets you google mapping

#SHAPELY - Make a circle around the target and the groceries within the circle

def make_circle(lat, lon, miles=0.5):
    circle_points = []
    for i in range(360):
        new_point = travel(lat, lon, bearing=i, miles=miles)
        new_point = new_point[0], new_point[1]
        circle_points.append(new_point)
    circle = Polygon(circle_points)
    return circle

def get_groceries_within_circle(df, circle):
    df_test_copy = df.copy()
    in_circle = []
    for i in range(len(df_test_copy)):
        lat = df_test_copy.iloc[i]['LATITUDE']
        lon = df_test_copy.iloc[i]['LONGITUDE']
        point = Point(lat, lon)

        if circle.contains(point):
            # In Circle
            in_circle.append(True)
        else:
            # Not In Circle
            in_circle.append(False)

    df_test_copy['in_circle'] = in_circle

    # Returns a data frame containing all grocery stores within the circle
    return df_test_copy[df_test_copy['in_circle'] == True]
