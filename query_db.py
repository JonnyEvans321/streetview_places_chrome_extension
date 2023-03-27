# import sqlite3

# # Bounding box coordinates
# west_lon, south_lat, east_lon, north_lat = -3.221313, 51.843106, -3.048952, 51.925540

# # Connect to the SQLite database
# conn = sqlite3.connect("offline/osm_poi.db")
# cursor = conn.cursor()

# # Query the "peaks" table for rows within the bounding box
# cursor.execute("""
# SELECT id, name, latitude, longitude, elevation
# FROM peaks
# WHERE latitude >= ? AND latitude <= ? AND longitude >= ? AND longitude <= ?
# """, (south_lat, north_lat, west_lon, east_lon))

# # Fetch and print the query results
# rows = cursor.fetchall()
# for row in rows:
#     print(row)

# # Close the database connection
# conn.close()

import sqlite3
import math

def haversine(lat1, lon1, lat2, lon2):
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

def visible_points(latitude, longitude, altitude, max_distance):
    conn = sqlite3.connect("offline/osm_poi.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, latitude, longitude, elevation FROM peaks")
    rows = cursor.fetchall()

    visible_rows = []
    for row in rows:
        id, name, lat, lon, elevation = row
        distance = haversine(latitude, longitude, lat, lon)

        if distance <= max_distance:
            visible_rows.append(row)

    conn.close()
    return visible_rows

if __name__ == "__main__":
    latitude = 51.862619
    longitude = -3.139846
    altitude = 166 # in meters. 2m is what you'd see from sea level.

    # Calculate the maximum visible distance based on altitude and Earth's radius (in meters)
    R = 6371000  # Earth's radius in meters
    max_distance = math.sqrt(altitude * (2 * R + altitude)) / 1000  # Distance in km
    print('max distance:', max_distance)

    visible_peaks = visible_points(latitude, longitude, altitude, max_distance)

    for peak in visible_peaks:
        print(peak)
