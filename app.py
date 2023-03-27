from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import math
import requests

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points on Earth in kilometers.
    
    Args:
        lat1 (float): Latitude of the first point in decimal degrees.
        lon1 (float): Longitude of the first point in decimal degrees.
        lat2 (float): Latitude of the second point in decimal degrees.
        lon2 (float): Longitude of the second point in decimal degrees.
    
    Returns:
        float: The great-circle distance between the two points in kilometers.
    """
    R = 6371  # Earth's radius in km

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def calculate_max_distance(altitude):
    """Calculate the maximum distance to the horizon based on the observer's altitude in meters.
    
    Args:
        altitude (float): The observer's altitude in meters.
    
    Returns:
        float: The maximum distance to the horizon in kilometers.
    """
    R = 6371  # Earth's radius in km
    altitude_km = altitude / 1000  # Convert altitude to km

    max_distance = math.sqrt(altitude_km * (2 * R + altitude_km))
    return max_distance

def visible_points(latitude, longitude, altitude, max_distance, tilt, fov):
    """Retrieve visible points of interest within the specified maximum distance.
    
    Args:
        latitude (float): The observer's latitude in decimal degrees.
        longitude (float): The observer's longitude in decimal degrees.
        altitude (float): The observer's altitude in meters.
        max_distance (float): The maximum distance to search for points of interest in kilometers.
    
    Returns:
        list: A list of visible points of interest sorted by distance.
    """
    conn = sqlite3.connect("offline/osm_poi.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, latitude, longitude, elevation FROM peaks")
    rows = cursor.fetchall()

    visible_rows = []
    for row in rows:
        id, name, lat, lon, elevation = row
        distance = haversine(latitude, longitude, lat, lon)

        try:
            if  elevation > 220:
                visible_rows.append((id, name, lat, lon, elevation, distance))  # Keep distance in each row
        except:
            pass

    conn.close()

    # Sort visible_rows by distance (the 6th element in each tuple)
    sorted_visible_rows = sorted(visible_rows, key=lambda x: x[5])

    return sorted_visible_rows

def get_elevation(latitude, longitude):
    url = f"https://api.opentopodata.org/v1/srtm30m?locations={latitude},{longitude}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        elevation = data['results'][0]['elevation']
        return elevation
    else:
        return None


@app.route("/get_peaks", methods=["GET"])
def get_peaks():
    latitude = float(request.args.get("latitude"))
    longitude = float(request.args.get("longitude"))
    tilt = float(request.args.get("tilt"))
    fov = float(request.args.get("fov"))

    altitude = get_elevation(latitude, longitude) + 2  # Call the get_elevation function, add two due to camera height

    if altitude is None:
        return jsonify({"error": "Failed to fetch elevation data"}), 500

    max_distance = calculate_max_distance(altitude)  # Calculate the max distance in kilometers

    visible_peaks = visible_points(latitude, longitude, altitude, max_distance, tilt, fov)

    return jsonify(visible_peaks)

if __name__ == "__main__":
    app.run(debug=True)
