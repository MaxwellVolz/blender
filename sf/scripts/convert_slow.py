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

def write_obj_file(data, coordinates_list, building_base, building_roof, ground_base, min_x, max_x, min_y, max_y, min_height, max_height, obj_file, hill_multiplier=2.0):
    offset_x = (min_x + max_x) / 2
    offset_y = (min_y + max_y) / 2
    x_scale, y_scale, z_scale = 5000, 5000, 0.5  # Scale factors for x, y, and z dimensions
    height_range = max_height - min_height

    with open(obj_file, "w") as obj:
        vertex_count = 1

        for index, coordinates in coordinates_list:
            row = data.iloc[index]
            ground_z = row[ground_base] if pd.notna(row[ground_base]) else 0
            z_min = (row[building_base] if pd.notna(row[building_base]) else 0) + ground_z
            z_max = (row[building_roof] if pd.notna(row[building_roof]) else z_min) + ground_z

            base_indices = []
            top_indices = []

            for (x, y) in coordinates:
                x_centered_scaled = (x - offset_x) * x_scale
                y_centered_scaled = (y - offset_y) * y_scale
                z_min_scaled = ((z_min - min_height) / height_range * 10 * hill_multiplier) * z_scale
                z_max_scaled = ((z_max - min_height) / height_range * 10 * hill_multiplier) * z_scale

                obj.write(f"v {x_centered_scaled} {y_centered_scaled} {z_min_scaled}\n")
                base_indices.append(vertex_count)
                vertex_count += 1

                obj.write(f"v {x_centered_scaled} {y_centered_scaled} {z_max_scaled}\n")
                top_indices.append(vertex_count)
                vertex_count += 1

            for i in range(len(base_indices)):
                next_i = (i + 1) % len(base_indices)
                obj.write(f"f {base_indices[i]} {base_indices[next_i]} {top_indices[next_i]} {top_indices[i]}\n")

            if len(base_indices) > 2:
                obj.write(f"f {' '.join(map(str, base_indices))}\n")
                obj.write(f"f {' '.join(map(str, reversed(top_indices)))}\n")

# Custom Params
hill_multiplier = 10.0

# Constants for fields in the dataset
ground_base = 'gnd_mediancm'
building_base = 'hgt_mincm'
building_roof = 'hgt_maxcm'


# Constants and file paths
file_path = "sf/resources/sf_building_footprints.csv"
obj_file = "hills_5.obj"


# Load data and process
data = pd.read_csv(file_path)
min_x, max_x, min_y, max_y, min_height, max_height, coordinates_list = process_building_data(data, building_base, building_roof)
write_obj_file(data, coordinates_list, building_base, building_roof, ground_base, min_x, max_x, min_y, max_y, min_height, max_height, obj_file, hill_multiplier)
