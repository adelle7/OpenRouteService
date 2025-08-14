import csv
import openrouteservice
import pandas as pd

# === CONFIGURATION ===
ORS_HOST = 'http://localhost:8080/ors'
PROFILES = ['driving-car']     #cannot do foot-walking or cycling-regular since distances are too long
BASE_PATH = '/Users/adellemelnikov/Downloads/TAU-Summer2025/openrouteservice/data/csv/inputs/'     #concat BASE_PATH + SOURCE_CSV[i] for each iteration at (1)
SOURCE_CSV = ['drexel-hill_sources.csv', 'mount-airy_sources.csv', 'northeast_sources.csv']     #change which sources and targets we are drawing points from
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

def main():
    # Load coordinates from CSVs
    for source_name in SOURCE_CSV:
        #(1)
        sources = load_coordinates(BASE_PATH + source_name)
        targets = load_coordinates(TARGET_CSV)
        sources = sources
        targets = targets

        #Initialize ORS client (no API key needed for local)
        client = openrouteservice.Client(base_url=ORS_HOST)

        # Loop over travel profiles (currently only driving profile is set)
        for profile in PROFILES:
            print(f"Requesting matrix for profile: {profile}")
            response = client.distance_matrix(
                locations = sources + targets,
                profile = profile,
                metrics = ['distance', 'duration'],
                sources = list(range(len(sources))),  #indeces treated as origins
                destinations = list(range(len(sources), len(sources) + len(targets))),    #indeces treated as targets
            )

            # Save both distance and duration matrices
            # if 'distances' in response:
            #     save_matrix_to_csv(response['distances'], profile, 'distance')
            if 'durations' in response:
                save_matrix_to_csv(response['durations'], profile, 'duration', source_name[:-12])

    # --------------------------------------------------------------------------------------------------------------------------------

# === RUN ===
if __name__ == '__main__':
    main()
