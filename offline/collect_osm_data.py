import requests
import sqlite3

overpass_url = "https://overpass-api.de/api/interpreter"

# Bounding box coordinates for Powys, Wales
west_lon, south_lat, east_lon, north_lat = -6.805994, 49.463492, 3.191136, 61.179499

query = f"""
[out:json];
(
  node[natural=peak]({south_lat},{west_lon},{north_lat},{east_lon});
  node[natural=summit]({south_lat},{west_lon},{north_lat},{east_lon});
);
out center;
"""

response = requests.get(overpass_url, params={"data": query})

if response.status_code == 200:
    data = response.json()

    # Extract mountain peaks data
    mountain_peaks = []
    for element in data['elements']:
        peak_id = element['id']
        latitude = element['lat']
        longitude = element['lon']
        name = element['tags'].get('name', 'N/A')
        elevation = element['tags'].get('ele', 'N/A')
        mountain_peaks.append((peak_id, name, latitude, longitude, elevation))

    # Connect to the SQLite database (this will create a new file named "osm_poi.db" if it doesn't exist)
    conn = sqlite3.connect("osm_poi.db")
    cursor = conn.cursor()

    # Create the "peaks" table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS peaks (
        id INTEGER PRIMARY KEY,
        name TEXT,
        latitude REAL,
        longitude REAL,
        elevation REAL
    )
    """)

    # Insert the mountain peaks data into the "peaks" table
    cursor.executemany("""
    INSERT OR REPLACE INTO peaks (id, name, latitude, longitude, elevation) VALUES (?, ?, ?, ?, ?)
    """, mountain_peaks)

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

    print("Data saved to the SQLite database 'osm_poi.db'")
else:
    print(f"Request failed with status code {response.status_code}")
