
import pandas as pd
import re

# file_path = "Building_Footprints_22404699.csv"
file_path = "sf/resources/sf_building_footprints_10k.csv"


data = pd.read_csv(file_path)


print(data.describe())