import requests
import json
import os

# This tells Python to print messages to the log immediately.
os.environ['PYTHONUNBUFFERED'] = "1"

print("--- Starting Paginated & Processed Biodiversity Data Fetch ---")

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
        print(f"An error occurred during the network request: {e}")
        exit(1)

print(f"\nSuccessfully fetched {len(all_features)} total features. Now processing...")

# Process the features into a simple [lat, lon, intensity] format
heatmap_data = []
for feature in all_features:
    if feature.get('geometry') and feature['geometry'].get('coordinates'):
        # Find the center of the polygon by averaging its corner points
        coords = feature['geometry']['coordinates'][0]
        lon_sum = 0
        lat_sum = 0
        point_count = len(coords)
        
        for point in coords:
            lon_sum += point[0]
            lat_sum += point[1]
        
        center_lon = lon_sum / point_count
        center_lat = lat_sum / point_count
        richness = feature['properties']['Rich_all']
        
        heatmap_data.append([center_lat, center_lon, richness])

# Save the much smaller, processed data file
with open("biodiversity_heatmap_data.json", "w") as f:
    json.dump(heatmap_data, f)

print(f"Successfully processed and saved {len(heatmap_data)} data points to biodiversity_heatmap_data.json")
