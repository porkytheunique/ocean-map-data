import requests
import json
import os

# This tells Python to print messages to the log immediately.
os.environ['PYTHONUNBUFFERED'] = "1"

print("--- Starting Final Paginated Biodiversity Data Fetch ---")

base_url = "https://services9.arcgis.com/IkktFdUAcY3WrH25/arcgis/rest/services/Global_Marine_Species_Patterns_(55km)/FeatureServer/0/query"
params = {
    'where': 'Rich_all >= 1',
    'outFields': 'Rich_all',
    'outSR': '4326',
    'f': 'geojson',
    'resultOffset': 0,
    'resultRecordCount': 2000 # Max records per request
}

all_features = []

while True:
    print(f"Fetching features starting at offset {params['resultOffset']}...")
    try:
        # We will use a long timeout to allow the server time to process
        response = requests.get(base_url, params=params, timeout=300) # 5 minute timeout
        response.raise_for_status()
        data = response.json()
        
        features = data.get('features', [])
        
        # THIS IS THE CORRECT LOGIC: Stop when the server returns no more features.
        if not features:
            print("No more features returned, fetch complete.")
            break
        
        all_features.extend(features)
        print(f"Fetched {len(features)} features. Total so far: {len(all_features)}")
        
        # Update the offset for the next page
        params['resultOffset'] += len(features)

    except requests.exceptions.RequestException as e:
        print(f"!!! An error occurred during the network request: {e}")
        exit(1) # Exit with an error code

# Reconstruct the final GeoJSON object with all features
final_geojson = {
    "type": "FeatureCollection",
    "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::4326" } },
    "features": all_features
}

with open("biodiversity_richness.geojson", "w") as f:
    json.dump(final_geojson, f)

print(f"\nSuccessfully fetched a total of {len(all_features)} biodiversity features and saved to biodiversity_richness.geojson")
