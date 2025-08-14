import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# === CONFIGURATION ===
CSV_ORS = '/Users/adellemelnikov/Downloads/TAU-Summer2025/openrouteservice/data/csv/matrices/ors_constant/mount-airy_ors_duration_matrix_driving-car.csv'
NAMES = ['drexel-hill', 'mount-airy', 'northeast']
DATE = ['07_29_8:00', '07_29_13:30', '07_29_17:00']
TIME = ['morning', 'afternoon', 'evening']
CSV_MAPS = '/Users/adellemelnikov/Downloads/TAU-Summer2025/openrouteservice/data/csv/matrices'
EXTEN = 'maps_duration_matrix_driving-car.csv'

# Read data from CSV files into dataframes
df_ors = pd.read_csv(CSV_ORS, header=0)
file_name = (f'{CSV_MAPS}/{DATE[2]}/{NAMES[1]}_{TIME[2]}_{EXTEN}')
print(file_name)
print(CSV_ORS)
df_maps = pd.read_csv(file_name, header=0)

# Check that matrices are the same size
if df_ors.shape != df_maps.shape:
    raise ValueError("Matrices cannot be compared: different sizes")

# Find the difference between maps point and ors point and convert to 1D array
result = df_maps - df_ors
#result.round(4).to_csv("drexel-hill_evening_difference_matrix.csv", index=True)

differences = result.values.flatten()

# Creating a customized histogram with a density plot
sns.histplot(differences, bins=30, kde=True, color='lightgreen', edgecolor='red')
mean = np.mean(differences)
median = np.median(differences)
std = np.std(differences)

# Print the mean, median, and standard deviation
print("Differences Between Google Maps and ORS Durations")
print("Mean: ", mean)
print("Median: ", median)
print("Standard Deviation: ", std)

# Adding labels and title
# plt.xlabel('Differences')
# plt.ylabel('Frequency')
# plt.title('Differences Between Google Maps and ORS Durations')

# Save the graph to a file
#plt.savefig("mount-airy_morning_diff_histogram.png", dpi=300, bbox_inches='tight')

# Display the plot
#plt.show()

