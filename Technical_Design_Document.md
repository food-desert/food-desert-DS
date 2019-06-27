# Technical Design Document
## Overview

We will find the areas of Los Angeles that are food deserts. The United States Department of Agriculture considers homes that are far away from wholesome food as a food desert.

We will plot a map of Los Angeles with colors indicating presence/absence of wholesome food.

## Data
We found data on [LA businesses](https://data.lacity.org/A-Prosperous-City/Listing-of-Active-Businesses/6rrh-rzua/data)
We have found LA county restaurant and market inventory data from the [Los Angeles County GIS data portal](https://egis3.lacounty.gov/dataportal/). It contains data from LA city and other cities within LA county.

Both data sources contains the type of grocery store, it's location as an address, and it's location as GPS coordinates.

There were other ways of getting data:
### Yelp API
With the Yelp API, you can search for "Grocery store" in LA city. This would be great, except for:
  * It provides a max of 50 addresses at a time. You have to specify an offset of 50+ for the other addresses.
  * The maximum number of stores it provided was much lower than the maximum number provided on the Yelp website
On workaround for this would have been to scrape the yelp wensite, but the data was already available as a CSV elsewhere.

## Processing the data
### Grid method
Create a grid of data points (latitude/longitude) around and within LA county. Evaluate if each data point lies within LA county. To do this, check if the point is within a polygon given by each city within LA city. The LA county city boundaries are available at [LA County City Boundaries](https://hub.arcgis.com/datasets/7b0998f4e2ea42bda0068afc8eeaf904_19/geoservice?geometry=-122.257%2C32.988%2C-114.347%2C34.586).

The Shapely library is used to determine if the point is within LA city. The library is available [here](https://shapely.readthedocs.io/en/latest/manual.html)

Another possibility would be to specify the grid of points manually. This way we could be sure they're within LA city. Maybe we can specify boundary points by putting pins on a Google Map of LA city, and then create a grid by sampling the width/height.

For the list of points within LA city:
  * Create an octagon around each point.
  * See if there is a grocery store within that octagon using Shapely.
  * If there are no grocery stores, that point is colored as a food desert point
### Shapes method
For each grocery store within LA city:
  * Draw a circle around that store to denote customers living within easy distance of that store.
  * Color that circle with a color representing a food oasis.
  * Specify background color for all of LA city to be the color of the food desert.
### Method selected - Grid method
The shapes method is easier in terms of processing, but only produces a map. It does not give you a list of points which are in the food desert.

The grid method requires more processing, but provides a list of points that are in the food desert.
