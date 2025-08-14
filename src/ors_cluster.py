import csv
import openrouteservice
import numpy as np
from sklearn.cluster import KMeans

# === CONFIGURATION ===
ORS_HOST = 'http://localhost:8080/ors'
PROFILES = ['driving-car']     #cannot do foot-walking or cycling-regular since distances are too long
BASE_PATH = '/Users/adellemelnikov/Downloads/TAU-Summer2025/openrouteservice/data/csv/inputs/'     #concat BASE_PATH + SOURCE_CSV[i] for each iteration at (1)
SOURCE_CSV = ['drexel-hill_sources.csv', 'mount-airy_sources.csv', 'northeast_sources.csv']     #change which sources and targets we are drawing points from
#SOURCE_CSV = ['drexel-hill_sources.csv']
TARGET_CSV = '/Users/adellemelnikov/Downloads/TAU-Summer2025/openrouteservice/data/csv/inputs/targets.csv'    

# === FUNCTIONS ===
def load_coordinates(file_path):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        return [[float(row['Longitude']), float(row['Latitude'])] for row in reader]
    
def save_matrix_to_csv(matrix, profile, matrix_type, source):
    file_name = f'{source}_{matrix_type}_matrix_{profile}.csv'
    df = pd.DataFrame(matrix)
    df.to_csv(file_name, index=False)
    print(f"Saved {matrix_type} matrix for {profile} to {file_name}")

# Convert the highway segments into individual lists [start_lon, start_lat, end_lon, end_lat]
# return points: a list of highway segments
def get_coord(segments):
    points = []
    for segment in segments:
        line = []
        start_lon, start_lat = segment['start']
        end_lon, end_lat = segment['end']
        line.append(start_lon)
        line.append(start_lat)
        line.append(end_lon)
        line.append(end_lat)
        points.append(line)

    return points

# Cluster the highway segments using scikit-learn k-means 
def k_means(points):
    X = np.array(points)
    kmeans = KMeans(n_clusters = 8, random_state = 0, n_init = "auto")
    centers = kmeans.fit_predict(X)

    print("Centroid values:")
    print(kmeans.cluster_centers_)
    return centers

def main():
    # Initialize ORS client first
    client = openrouteservice.Client(base_url=ORS_HOST)

    # List of highway segments used for clustering
    highway_segments = []

    # Get DIRECTIONS for each pair of sources to targets
    # --------------------------------------------------------------------------------------------------------------------------------
    with open("highway_segments_list.csv", "w", newline = '') as f_seg:
        writer_seg = csv.writer(f_seg)
        writer_seg.writerow(["start_lon", "start_lat", "end_lon", "end_lat"])

        for source_name in SOURCE_CSV:
            print('Using source: ',source_name)
            
            sources = load_coordinates(BASE_PATH + source_name)
            targets = load_coordinates(TARGET_CSV)
            sources = sources
            targets = targets

            with open(f"{source_name[:-12]}_directions_routes.csv", "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["source_index", "target_index", "distance_m", "duration_s", "waycategory"]) # header
                # create an empty matrix
                rows = len(sources)
                cols = len(targets)
                matrix = [[0 for _ in range(cols)] for _ in range(rows)]    # matrix representing which paths contain highways

                # Loop over each pair
                for i, source in enumerate(sources):
                    for j, target in enumerate(targets):
                        if source == target:
                            continue    # distance needs to be > 0
                        try:
                            response = client.directions(
                                coordinates = [source, target],
                                profile = 'driving-car',
                                format = 'geojson',
                                instructions = False,
                                geometry = True,
                                extra_info = ['waycategory', 'waytype']
                            )
                            
                            summary = response['features'][0]['properties']['summary']

                            # get coordinates of each path using geometry attribute
                            geometry = response['features'][0]['geometry']['coordinates']
                            #coordinates = str(geometry)    # convert geometry to string to save in one cell in writing to file 

                            # additional feature, waytype corresponding to parts of a route: 
                            # https://github.com/GIScience/openrouteservice/blob/main/docs/api-reference/endpoints/directions/extra-info/waytype.md

                            # here we use way category ids to see which roads are highways
                            # waycat_def = {
                            #     0: 'no category',
                            #     1: 'highway',
                            #     2: 'tollways',
                            #     4: 'steps',
                            #     8: 'ferry',
                            #     16: 'ford'
                            # }

                            waycat = response['features'][0]['properties']['extras']['waycategory']['values']
                            waycat_str = str(waycat)

                            writer.writerow([source, target, summary['distance'], summary['duration'], waycat_str])

                            # store 1 if contains highway, 0 otherwise
                            contains_highway = any(category[2] == 1 for category in waycat)
                            matrix[i][j] = 1 if contains_highway else 0

                            # map segments from waycategory to actual lat, lon coordinates and save to a list 
                            for start, end, category, in waycat:
                                if category == 1:
                                    if 0 <= start < len(geometry) and 0 <= end < len(geometry):
                                        start_lon, start_lat = geometry[start]
                                        end_lon, end_lat = geometry[end]
                                        highway_segments.append({
                                            'source': source,
                                            'target': target,
                                            'start': (start_lon, start_lat),
                                            'end': (end_lon, end_lat),
                                            'category': category
                                        })
                                        writer_seg.writerow([start_lon, start_lat, end_lon, end_lat])

                        except Exception as e:
                            print(f"Error processing route {i}->{j}: {e}")
                            writer.writerow([i, j, None, None, "ERROR"])

                # save full matrix to csv file
                # save_matrix_to_csv(matrix, 'driving-car', 'waycat', source_name[:-12])s

    highway_lines = get_coord(highway_segments)

    centroids = k_means(highway_lines)
    print(centroids)

# --------------------------------------------------------------------------------------------------------------------------------

# === RUN ===
if __name__ == '__main__':
    main()