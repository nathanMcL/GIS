# The Purpose of this program:
# Experiment with the Folium static map library
# Create a visual representation of the earth surface
# Use grid coordinates pulled from traceroute.py
# Plot grid coordinates using longitude and latitude
# Calculate the distance between the plotted points
# Open Folium map through # Save map, created html browser link

# Folium Map Features:
# Zoom in/out or Shift left-click-hold
# US states highlighted borers, toggle
# US highlighted National forests, toggle
# Street map, terrain and water overlay choices

# Dash Interactive Map dashboard features:
# Running: kinda slow, click http:// link in console
# Option to plot coordinates between to separate locations
# Calculates distance between coordinates
# Displays weather temperature at coordinated locations

import dash
from dash import dcc, html  # Directly import from `dash` instead of deprecated packages
from dash.dependencies import Input, Output
import json
import folium
import math
import requests


# Function to calculate distance using Haversine formula
def haversine(lon1, lat1, lon2, lat2):
    R = 3958.8  # Earth radius in miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


# Fetch weather data from OpenWeather API
def fetch_weather(lon, lat):
    API_KEY = " "  # Replace with your API key
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp'] - 273.15  # Convert Kelvin to Celsius
        return f"{temp:.2f}°C"
    else:
        return "Weather data not available"


# Initialize a Folium map centered around one of the Start Points(sp).
sp = folium.Map(location=[47.6038, -122.3300], zoom_start=4)

# Load GeoJSON (replace 'us_states.json' with the path to your GeoJSON file)
with open('gz_2010_us_040_00_500k.json', 'r') as f:
    us_states_data = json.load(f)

# Add GeoJSON overlay for US states
folium.GeoJson(us_states_data, name='US States').add_to(sp)

# Load GeoJSON (replace 'National_Park_Service_Land.json' with the path to your GeoJSON file)
with open('National_Park_Service_Land.geojson', 'r') as f:
    parks_recreation = json.load(f)

# Add GeoJSON overlay for National Parks
folium.GeoJson(parks_recreation, name='US National Parks').add_to(sp)

# Coordinates
coordinates = [
    {'lon': -122.3300, 'lat': 47.6038, 'color': 'green'},
    {'lon': -122.0832, 'lat': 37.3893, 'color': 'orange'}

]

# Add markers and lines
points = []
for coord in coordinates:
    folium.Marker([coord['lat'], coord['lon']], popup=f"Lon: {coord['lon']}, Lat: {coord['lat']}",
                  icon=folium.Icon(color=coord['color'])).add_to(sp)
    points.append(tuple([coord['lat'], coord['lon']]))
folium.PolyLine(points, color="blue", weight=2.5, opacity=1).add_to(sp)

# Add circles around points
for coord in coordinates:
    folium.Circle(
        radius=10000,
        location=[coord['lat'], coord['lon']],
        color=coord['color'],
        fill=False,
    ).add_to(sp)

# Calculate distance
lon1, lat1 = coordinates[0]['lon'], coordinates[0]['lat']
lon2, lat2 = coordinates[1]['lon'], coordinates[1]['lat']
distance = haversine(lon1, lat1, lon2, lat2)

print(f"The distance between the points is {distance:.2f} miles.")

# Different tile layers
folium.TileLayer('stamenterrain').add_to(sp)
folium.TileLayer('stamenwatercolor').add_to(sp)

# Layer control
folium.LayerControl().add_to(sp)

# Save map
sp.save('map_folium_enhanced.html')

# Dash app initialization
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Interactive Map Dashboard"),

    html.Label("Enter Longitude for Point 1:"),
    dcc.Input(id='lon1', type='number', value=-122.3300),

    html.Label("Enter Latitude for Point 1:"),
    dcc.Input(id='lat1', type='number', value=47.6038),

    html.Label("Enter Longitude for Point 2:"),
    dcc.Input(id='lon2', type='number', value=-122.0832),

    html.Label("Enter Latitude for Point 2:"),
    dcc.Input(id='lat2', type='number', value=37.3893),

    html.Button(id='submit-button', n_clicks=0, children='Calculate'),

    html.Div(id='output-weather1'),
    html.Div(id='output-weather2'),
    html.Div(id='output-distance'),

    # Embedding Folium map in an iframe
    html.Iframe(id='map', srcDoc=open('map_folium_enhanced.html', 'r').read(), width='100%', height='600')
])


@app.callback(
    [Output('output-weather1', 'children'),
     Output('output-weather2', 'children'),
     Output('output-distance', 'children')],
    [Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('lon1', 'value'),
     dash.dependencies.State('lat1', 'value'),
     dash.dependencies.State('lon2', 'value'),
     dash.dependencies.State('lat2', 'value')]
)
def update_output(n_clicks, lon1, lat1, lon2, lat2):
    weather1 = fetch_weather(lon1, lat1)
    weather2 = fetch_weather(lon2, lat2)
    distance = haversine(lon1, lat1, lon2, lat2)

    return f"Weather at Point 1: {weather1}", f"Weather at Point 2: {weather2}", f"Distance: {distance:.2f} miles"


if __name__ == '__main__':
    app.run_server(debug=True)