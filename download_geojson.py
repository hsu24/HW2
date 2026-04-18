import urllib.request
import json

url = "https://raw.githubusercontent.com/g0v/twgeojson/master/json/twCounty2010.geo.json"
output_file = "taiwan.geojson"

print("Downloading Taiwan GeoJSON...")
urllib.request.urlretrieve(url, output_file)
print("Download complete.")

with open(output_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Let's inspect the first feature to see property keys for counties
print(data['features'][0]['properties'])
