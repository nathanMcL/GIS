# The purpose of this program:
# Create a visual representation of the earth surface
# Use grid coordinates pulled from traceroute.py
# Plot grid coordinates using longitude and latitude
# Calculate the distance between the plotted points


import geopandas as gpd
import matplotlib.pyplot as plt
import math
import pyproj


# Haversine formula to calculate the distance between two points given their latitude and longitude
def haversine(lon1, lat1, lon2, lat2):
    R = 3958.8  # Radius of Earth in miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance


# Create a list of longitude, latitude, and geolocation data
coordinates = [
    {'lon': -122.4383, 'lat': 47.2455, 'name': 'Location A'},
    {'lon': -122.2127, 'lat': 47.9793, 'name': 'Location B'},
    {'lon': -122.3300, 'lat': 47.6038, 'name': 'Location C'},
    {'lon': -122.0832, 'lat': 37.3893, 'name': 'Location D'},
]

# No actual transformation in this case, just a placeholder
wgs84_coordinates = coordinates.copy()

# Read in the shapefile of the world
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot the world boundaries
world.boundary.plot()

# Plot the coordinates on top of the world map
for point in wgs84_coordinates:
    plt.scatter(point['lon'], point['lat'])

# Label the points
for point in wgs84_coordinates:
    plt.annotate(f"{point['name']} ({point['lon']}, {point['lat']})", (point['lon'], point['lat']),
                 textcoords="offset points", xytext=(0, 10), ha='center')

# Calculate and display distances between each pair of points
for i in range(len(wgs84_coordinates)):
    for j in range(i + 1, len(wgs84_coordinates)):
        distance = haversine(wgs84_coordinates[i]['lon'], wgs84_coordinates[i]['lat'], wgs84_coordinates[j]['lon'],
                             wgs84_coordinates[j]['lat'])

        # Label the distance on the midpoint between two coordinates
        midpoint_x = (wgs84_coordinates[i]['lon'] + wgs84_coordinates[j]['lon']) / 2
        midpoint_y = (wgs84_coordinates[i]['lat'] + wgs84_coordinates[j]['lat']) / 2
        plt.annotate(f"{distance:.2f} miles", (midpoint_x, midpoint_y), textcoords="offset points", xytext=(0, -10),
                     ha='center')

# Show the plot
plt.show()
