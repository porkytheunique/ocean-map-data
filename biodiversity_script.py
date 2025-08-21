import requests
import os

# This tells Python to print messages to the log immediately.
os.environ['PYTHONUNBUFFERED'] = "1"

print("--- Starting SIMPLEST API Fetch Test ---")

# A very simple URL that asks for just ONE record from the dataset.
test_url = "https://services9.arcgis.com/IkktFdUAcY3WrH25/arcgis/rest/services/Global_Marine_Species_Patterns_(55km)/FeatureServer/0/query?where=1%3D1&outFields=Rich_all&outSR=4326&f=geojson&resultRecordCount=1"

print(f"Requesting URL: {test_url}")

try:
    # We will try to connect with a 60-second timeout.
    response = requests.get(test_url, timeout=60)
    response.raise_for_status()
    print("\n--- SUCCESS! ---")
    print("Successfully connected to the API and received a response.")
    print("\nResponse Text:")
    print(response.text)

except requests.exceptions.RequestException as e:
    print(f"\n!!! FETCH FAILED: {e}")

print("\n--- Test Complete ---")
