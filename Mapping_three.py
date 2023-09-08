# The purpose of this program:
# Create a visual representation of the earth surface
# Use grid coordinates pulled from traceroute.py
# Plot grid coordinates using longitude and latitude
# Calculate the distance between the plotted points
# Border the United States in green
# Border the Counties in purple

# The program runs slow


import geopandas as gpd
import matplotlib.pyplot as plt
import math


# Haversine formula to calculate distance
def haversine(lon1, lat1, lon2, lat2):
    R = 3958.8  # Earth radius in miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


# Coordinate data
coordinates = [
    {'lon': -122.4383, 'lat': 47.2455, 'name': 'Location A'},
    {'lon': -122.2127, 'lat': 47.9793, 'name': 'Location B'},
    {'lon': -122.3300, 'lat': 47.6038, 'name': 'Location C'},
    {'lon': -122.0832, 'lat': 37.3893, 'name': 'Location D'},
]

# Read world shapefile
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Read US states shapefile
us_states = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
us_states = us_states[us_states['iso_a3'] == 'USA']

# Read US counties shapefile
us_counties = gpd.read_file("tl_2019_us_county.shp")

# Create a single plot with subplots (here only one)
fig, ax = plt.subplots(1, 1)

# Plot world boundaries
world.boundary.plot(ax=ax)

# Plot US state boundaries
us_states.boundary.plot(ax=ax, color='green')

# Plot US county boundaries
us_counties.boundary.plot(ax=ax, color='purple')

# Plot and label points
for point in coordinates:
    plt.scatter(point['lon'], point['lat'])
    plt.annotate(f"{point['name']} ({point['lon']}, {point['lat']})", (point['lon'], point['lat']),
                 textcoords="offset points", xytext=(0, 10), ha='center')

# Calculate and display distances
for i in range(len(coordinates)):
    for j in range(i + 1, len(coordinates)):
        distance = haversine(coordinates[i]['lon'], coordinates[i]['lat'], coordinates[j]['lon'], coordinates[j]['lat'])
        midpoint_x = (coordinates[i]['lon'] + coordinates[j]['lon']) / 2
        midpoint_y = (coordinates[i]['lat'] + coordinates[j]['lat']) / 2
        plt.annotate(f"{distance:.2f} miles", (midpoint_x, midpoint_y), textcoords="offset points", xytext=(0, -10),
                     ha='center')

# Show plot
plt.show()
