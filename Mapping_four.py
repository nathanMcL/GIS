# The purpose of this program:
# Create a visual representation of the earth surface
# Use grid coordinates pulled from traceroute.py
# Plot grid coordinates using longitude and latitude
# Calculate the distance between the plotted points
# Border the United States in black
# Inserted county border overlay
# Border the Counties in purple
# Inserted bodies of water overlay in light blue
# Inserted national forests overlay in green

# The program runs slow
# MtnRange turns things red, maybe needs different overlay


import geopandas as gpd
import matplotlib.pyplot as plt
import math

# Flags to toggle layers, and labels
# Set too False to remove labels
plot_world_boundary = True
plot_country_labels = True
plot_us_state_boundary = True
plot_us_county_boundary = True
plot_bodies_of_water = True
plot_national_forests = True
plot_roads = True
plot_time_zones = True
plot_state_labels = True


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

# Read Bodies of Water shapefile
bodies_of_water = gpd.read_file("ne_10m_geography_marine_polys.shp")

# Read Mountain Ranges shapefile (make sure the file exists in your directory)
mountain_ranges = gpd.read_file("ne_10m_geography_regions_polys.shp")

# Read Forests shapefile (make sure the file exists in your directory)
national_forests = gpd.read_file("S_USA.AdministrativeRegion.shp")

# Read Forests shapefile (make sure the file exists in your directory)
roads = gpd.read_file("tl_2019_us_primaryroads.shp")

# Read Time Zones shapefile (make sure the file exists in your directory)
time_zones = gpd.read_file("World_Time_Zones.shp")

# Create a single plot with subplots (here only one)
fig, ax = plt.subplots(1, 1)

# Conditional plotting
if plot_world_boundary:
    world.boundary.plot(ax=ax)

if plot_country_labels:
    for idx, country in world.iterrows():
        plt.text(country.geometry.centroid.x, country.geometry.centroid.y, country['name'], fontsize=8, ha='center',
                 color='black')

if plot_us_state_boundary:
    us_states.boundary.plot(ax=ax, color='black')

if plot_us_county_boundary:
    us_counties.boundary.plot(ax=ax, linewidth=2, color='purple')

if plot_bodies_of_water:
    bodies_of_water.plot(ax=ax, facecolor='lightblue')

if plot_national_forests:
    national_forests.plot(ax=ax, color='green')

if plot_roads:
    roads.plot(ax=ax, linewidth=1, color='lightgrey')

if plot_time_zones:
    time_zones.boundary.plot(ax=ax, linewidth=2, color='orange')

if plot_state_labels:
    for idx, state in us_states.iterrows():
        plt.text(state.geometry.centroid.x, state.geometry.centroid.y, state['name'], fontsize=8, ha='center',
                 color='white')

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
