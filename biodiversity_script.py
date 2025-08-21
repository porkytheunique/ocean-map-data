import requests
import json

print("--- Starting Paginated Biodiversity Data Fetch ---")

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
        response = requests.get(base_url, params=params, timeout=300) # 5 minute timeout
        response.raise_for_status()
        data = response.json()
        
        features = data.get('features', [])
        if not features:
            print("No more features returned, fetch complete.")
            break
        
        all_features.extend(features)
        print(f"Fetched {len(features)} features. Total so far: {len(all_features)}")
        
        if not data.get('properties', {}).get('exceededTransferLimit', False):
            print("Transfer limit not exceeded, fetch complete.")
            break
        
        params['resultOffset'] += len(features)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        break

# Reconstruct the final GeoJSON object with all features
final_geojson = {
    "type": "FeatureCollection",
    "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::4326" } },
    "features": all_features
}

with open("biodiversity_richness.geojson", "w") as f:
    json.dump(final_geojson, f)

print(f"Successfully fetched a total of {len(all_features)} biodiversity features and saved to biodiversity_richness.geojson")
