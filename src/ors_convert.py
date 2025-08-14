import json
import random
import csv

# Suburb of Philadelphia Nodes
# Load the JSON data from file
with open('/Users/adellemelnikov/Downloads/TAU-Summer2025/openrouteservice/data/json/drexel-hill_nodes.json', 'r') as f:
    data = json.load(f)

philadephia_coordinates = []

for element in data.get('elements', []):
    if element.get('type') == 'node':
        lat = element.get('lat')
        lon = element.get('lon')
        if lat is not None and lon is not None:
            philadephia_coordinates.append((lon, lat))

#get random sample of coordinates
sample_size = 50
sample_size = min(sample_size, len(philadephia_coordinates))
philly_sample = random.sample(philadephia_coordinates, sample_size)

print("Suburbs Nodes:")
# Print out the lon/lat pairs
# for lon, lat in philly_sample:
#     print(f"Longitude: {lon}, Latitude: {lat}")

# Write to sources.csv
with open('/Users/adellemelnikov/Downloads/TAU-Summer2025/openrouteservice/data/csv/drexel-hill_sources.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Longitude', 'Latitude'])
    writer.writerows(philly_sample)

print("done")

# COMMENT OUT when generating more suburbs, since we want the center city nodes to stay the same 
# ------------------------------------------ STARTING HERE -------------------------------------------------------------------------------------
#center city of philadelphia NODES
# with open('/Users/adellemelnikov/Downloads/TAU-Summer2025/openrouteservice/data/json/center-city-philadelphia_nodes.json', 'r') as f:
#     data = json.load(f)

# residence_coordinates = []

# #add each elements to list 
# for element in data.get('elements', []):
#     if element.get('type') == 'node':
#         lat = element.get('lat')
#         lon = element.get('lon')
#         if lat is not None and lon is not None:
#             residence_coordinates.append((lon, lat))

# #get random sample of coordinates
# residence_sample = random.sample(residence_coordinates, sample_size)
# # Print out the lon/lat pairs
# print("Residence Areas Nodes:")
# # for lon, lat in residence_sample:
# #     print(f"Longitude: {lon}, Latitude: {lat}")

# #write to targets.csv file 
# with open('/Users/adellemelnikov/Downloads/TAU-Summer2025/openrouteservice/data/csv/targets.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(['Longitude', 'Latitude'])
#     writer.writerows(residence_sample)

# print("done")
# ----------------------------------------------------------------------------------------------------------------------------------------------
