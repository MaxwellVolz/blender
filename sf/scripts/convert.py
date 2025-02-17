import pandas as pd
import re

# Load data from a CSV file
file_path = "sf/resources/sf_building_footprints_20k.csv"
data = pd.read_csv(file_path)

# Load an OBJ file to write the modified data
obj_file = "building_footprints_3d_normalized_20k.obj"


min_x, min_y = float('inf'), float('inf')
max_x, max_y = float('-inf'), float('-inf')

# Improved regular expression to ensure we capture all coordinate details properly
for index, row in data.iterrows():
    multipolygon = row['shape']
    coords_str = re.sub(r"MULTIPOLYGON\s*\(\(\((.*?)\)\)\)", r"\1", multipolygon)
    coords_str = coords_str.replace("(", "").replace(")", "")
    
    # Process each coordinate pair
    coords_list = coords_str.split(',')
    coordinates = []
    for coord in coords_list:
        # Further cleaning to ensure all extraneous characters are removed
        parts = coord.strip().split()
        if len(parts) == 2:
            try:
                x, y = map(float, parts)
                coordinates.append((x, y))
                if x < min_x: min_x = x
                if x > max_x: max_x = x
                if y < min_y: min_y = y
                if y > max_y: max_y = y
            except ValueError as e:
                print(f"Error converting string to float at row {index}, coordinate {coord}: {e}")
        else:
            print(f"Unexpected format for coordinates in row {index}: {parts}")

z_min = data['p2010_zminn88ft'] if pd.notna(row['p2010_zminn88ft']) else 0
z_max = data['p2010_zmaxn88ft'] if pd.notna(row['p2010_zmaxn88ft']) else 0

height = z_max - z_min
min_height = data['p2010_zminn88ft'].min()
max_height = data['p2010_zmaxn88ft'].max()

offset_x = (min_x + max_x) / 2
offset_y = (min_y + max_y) / 2

scaling_factor = 0.001

target_min_height = -1.0
target_max_height = 3.8
height_range = max_height - min_height

with open(obj_file, "w") as obj:
    vertices = []
    faces = []
    vertex_count = 1

    # Repeat the logic for parsing and writing vertices and faces
    for index, row in data.iterrows():
        multipolygon = row['shape']
        coords_str = re.sub(r"MULTIPOLYGON\s*\(\(\((.*?)\)\)\)", r"\1", multipolygon)
        coords_str = coords_str.replace("(", "").replace(")", "")
        coords_list = coords_str.split(',')
        base_indices = []
        top_indices = []
        for coord in coords_list:
            parts = coord.strip().split()
            if len(parts) == 2:
                try:
                    x, y = map(float, parts)
                    x_centered = (x - offset_x) * scaling_factor
                    y_centered = (y - offset_y) * scaling_factor
                    z_centered = (z_min - min_height) / height_range * (target_max_height - target_min_height) + target_min_height

                    vertices.append((x_centered, y_centered, z_centered))
                    base_indices.append(vertex_count)
                    vertex_count += 1

                    z_max_normalized = z_max / height_range * (target_max_height - target_min_height) + target_min_height
                    vertices.append((x_centered, y_centered, z_max_normalized))
                    top_indices.append(vertex_count)
                    vertex_count += 1
                except ValueError as e:
                    print(f"Error converting string to float at row {index}, coordinate {coord}: {e}")

        for v in vertices:
            obj.write(f"v {v[0]} {v[1]} {v[2]}\n")

        for i in range(len(base_indices)):
            v1 = base_indices[i]
            v2 = top_indices[i]
            next_i = (i + 1) % len(base_indices)
            v3 = base_indices[next_i]
            v4 = top_indices[next_i]

            obj.write(f"f {v1} {v2} {v4} {v3}\n")