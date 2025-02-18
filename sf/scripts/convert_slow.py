import pandas as pd
import re

FEET_TO_CM = 30.48

def feet_to_cm(feet):
    return feet * FEET_TO_CM

def parse_coordinates(coords_str):
    coords_str = re.sub(r"MULTIPOLYGON\s*\(\(\(|\)\)\)", "", coords_str)
    coords_str = coords_str.replace('(', '').replace(')', "")
    return [tuple(map(float, coord.strip().split())) for coord in coords_str.split(', ')]

def process_building_data(data, building_base, building_roof):
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')
    min_height, max_height = float('inf'), float('-inf')
    coordinates_list = []

    for index, row in data.iterrows():
        try:
            coordinates = parse_coordinates(row['shape'])
        except ValueError as e:
            print(f"Error parsing coordinates for row {index}: {e}")
            continue

        coordinates_list.append((index, coordinates))
        x_coords, y_coords = zip(*coordinates)
        min_x = min(min_x, *x_coords)
        max_x = max(max_x, *x_coords)
        min_y = min(min_y, *y_coords)
        max_y = max(max_y, *y_coords)

        z_min = row[building_base] if pd.notna(row[building_base]) else 0
        z_max = row[building_roof] if pd.notna(row[building_roof]) else z_min
        height = z_max - z_min
        min_height = min(min_height, height)
        max_height = max(max_height, height)

    return min_x, max_x, min_y, max_y, min_height, max_height, coordinates_list

def write_obj_file(data, coordinates_list, building_base, building_roof, min_x, max_x, min_y, max_y, min_height, max_height, obj_file):
    offset_x = (min_x + max_x) / 2
    offset_y = (min_y + max_y) / 2
    scaling_factor = 1
    height_range = max_height - min_height

    with open(obj_file, "w") as obj:
        vertex_count = 1

        for index, coordinates in coordinates_list:
            row = data.iloc[index]
            z_min = row[building_base] if pd.notna(row[building_base]) else 0
            z_max = row[building_roof] if pd.notna(row[building_roof]) else z_min

            base_indices = []
            top_indices = []

            for (x, y) in coordinates:
                x_centered = (x - offset_x) * scaling_factor
                y_centered = (y - offset_y) * scaling_factor
                z_centered = (z_min - min_height) / height_range * 10

                obj.write(f"v {x_centered} {y_centered} {z_centered}\n")
                base_indices.append(vertex_count)
                vertex_count += 1

                z_max_centered = (z_max - min_height) / height_range * 10
                obj.write(f"v {x_centered} {y_centered} {z_max_centered}\n")
                top_indices.append(vertex_count)
                vertex_count += 1

            for i in range(len(base_indices) - 1):
                obj.write(f"f {base_indices[i]} {base_indices[i+1]} {top_indices[i+1]} {top_indices[i]}\n")

            if len(base_indices) > 2:  # Write top and bottom faces if they form a valid polygon
                obj.write(f"f {' '.join(map(str, base_indices))}\n")
                obj.write(f"f {' '.join(map(str, reversed(top_indices)))}\n")

# Constants and file paths
file_path = "sf/resources/sf_building_footprints_20k.csv"
obj_file = "full_raw.obj"
building_base = "hgt_mincm"
building_roof = "hgt_maxcm"

# Load data and process
data = pd.read_csv(file_path)
min_x, max_x, min_y, max_y, min_height, max_height, coordinates_list = process_building_data(data, building_base, building_roof)
write_obj_file(data, coordinates_list, building_base, building_roof, min_x, max_x, min_y, max_y, min_height, max_height, obj_file)
