import pandas as pd
import re

FEET_TO_CM = 30.48

def feet_to_cm(feet):
    return feet * FEET_TO_CM
# file_path = "Building_Footprints_22404699.csv"
file_path = "sf/resources/sf_building_footprints_20k.csv"
obj_file = "full_raw.obj"

# building options
building_base= "hgt_mincm"
building_roof= "hgt_maxcm"

data = pd.read_csv(file_path)

min_x, min_y = float('inf'), float('inf')
max_x, max_y = float('-inf'), float('-inf')
min_height, max_height = float('inf'), float('-inf')

for index, row in data.iterrows():
    multipolygon = row['shape']

    coords_str = re.sub(r"MULTIPOLYGON\s*\(\(\(|\)\)\)", "", multipolygon)
    coords_str = coords_str.replace('(', '').replace(')', "")

    try:
        coordinates = [tuple(map(float, coord.strip().split())) for coord in coords_str.split(', ')]
    except ValueError as e:
        print(f"Error parsing coordinates for row {index}: {e}")
        continue

    for (x, y) in coordinates:
        if x < min_x: min_x = x
        if x > max_x: max_x = x
        if y < min_y: min_y = y
        if y > max_y: max_y = y

    z_min = row[building_base] if pd.notna(row[building_base]) else 0
    z_max = row[building_roof] if pd.notna(row[building_roof]) else z_min

    height = z_max - z_min

    if height < min_height: min_height = height
    if height > max_height: max_height = height

    print(f"height: {height} min_height: {min_height} max_height: {max_height}")


offset_x = (min_x + max_x) / 2
offset_y = (min_y + max_y) / 2

scaling_factor = 1

target_min_height = 0.0
target_max_height = 10.0

height_range = max_height - min_height


with open(obj_file, "w") as obj:
    vertices = []
    faces = []
    vertex_count = 1

    for index, row in data.iterrows():
        multipolygon = row['shape']

        coords_str = re.sub(r"MULTIPOLYGON\s*\(\(\(|\)\)\)", '', multipolygon)
        coords_str = coords_str.replace('(', '').replace(')', '')

        try:
            coordinates = [tuple(map(float, coord.strip().split())) for coord in coords_str.split(', ')]
        except ValueError as e:
            print(f"Error parsing coordinates for row {index}: {e}")
            continue

        z_min = row[building_base] if pd.notna(row[building_base]) else 0
        z_max = row[building_roof] if pd.notna(row[building_roof]) else z_min

        height = z_max - z_min
        normalized_height = height
        z_min_normalized = 0
        z_max_normalized = normalized_height

        print(f"normalized_height: {normalized_height} ")

        base_indices = []
        top_indices = []

        # Center and scale coordinates
        for (x, y) in coordinates:
            x_centered = (x - offset_x) * scaling_factor
            y_centered = (y - offset_y) * scaling_factor
            z_centered = (z_min - min_height) / height_range * (target_max_height - target_min_height) + target_min_height

            vertices.append((x_centered, y_centered, z_centered))
            obj.write(f"v {x_centered} {y_centered} {z_centered}\n")

            base_indices.append(vertex_count)
            vertex_count += 1

            z_max_normalized = z_max / height_range * (target_max_height - target_min_height) + target_min_height
            # Top vertex at (x_centered, y_centered, z_max_normalized)
            vertices.append((x_centered, y_centered, z_max))
            obj.write(f"v {x_centered} {y_centered} {z_max}\n")
            top_indices.append(vertex_count)
            vertex_count += 1

            # print(base_indices)
            # print(top_indices)

        # Create faces for the sides, connect each base vertex to the corresponding top vertex
        for i in range(len(base_indices)):
            next_i = (i + 1) % len(base_indices)
            v1 = base_indices[i]
            v2 = base_indices[next_i]
            v3 = top_indices[next_i]
            v4 = top_indices[i]
            faces.append((v1, v2, v3, v4))

        # Create face for the base (bottom face)
        if len(base_indices) > 2:
            faces.append(tuple(base_indices))

        # Create face for the top (top face)
        if len(top_indices) > 2:
            faces.append(tuple(reversed(top_indices)))  # Reverse to ensure normal direction is correct


    # Write faces to the OBJ file
    for face in faces:
        obj.write("f {}\n".format(" ".join(map(str, face))))
