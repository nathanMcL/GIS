# The purpose of this program:
# Using Matplotlib create a visual representation using grid coordinates pulled from traceroute.py
# Plot grid coordinates using longitude and latitude
# calculate the distance between the plotted points


import matplotlib.pyplot as plt
import math


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
    {'lon': -132.4383, 'lat': 45.2455, 'name': 'Location A'},
    {'lon': -127.2127, 'lat': 42.9793, 'name': 'Location B'},
    {'lon': -112.3300, 'lat': 49.6038, 'name': 'Location C'},
    {'lon': -140.0832, 'lat': 30.3893, 'name': 'Location D'},
]

# Print geolocation data to the console
print("Geolocation Data:")
for point in coordinates:
    print(f"{point['name']}: Longitude = {point['lon']}, Latitude = {point['lat']}")

fig, ax = plt.subplots()

# Use the `plt.scatter()` function to plot the coordinates as a scatter plot
for point in coordinates:
    plt.scatter(point['lon'], point['lat'])

# Label the points
for point in coordinates:
    ax.annotate(f"{point['name']} ({point['lon']}, {point['lat']})", (point['lon'], point['lat']),
                textcoords="offset points", xytext=(0, 10), ha='center')

# Calculate and display distances between each pair of points
for i in range(len(coordinates)):
    for j in range(i + 1, len(coordinates)):
        distance = haversine(coordinates[i]['lon'], coordinates[i]['lat'], coordinates[j]['lon'], coordinates[j]['lat'])

        # Label the distance on the midpoint between two coordinates
        midpoint_x = (coordinates[i]['lon'] + coordinates[j]['lon']) / 2
        midpoint_y = (coordinates[i]['lat'] + coordinates[j]['lat']) / 2
        ax.annotate(f"{distance:.2f} miles", (midpoint_x, midpoint_y), textcoords="offset points", xytext=(0, -10),
                    ha='center')

        print(
            f"Distance between {coordinates[i]['name']} ({coordinates[i]['lon']}, {coordinates[i]['lat']}) and {coordinates[j]['name']} ({coordinates[j]['lon']}, {coordinates[j]['lat']}) is {distance:.2f} miles")

# Set the x-axis and y-axis labels
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Show the plot
plt.show()
