# Description: This script is used to format the decimal of the coordinates in the POSCAR file.
import re

def is_valid_float(value):
    pattern = re.compile(r'[0-9]*\.[0-9]+$')
    return bool(pattern.match(value))

input_file = "POSCAR_BZO_ROTATION"
output_file = "formatted_POSCAR_BZO_ROTATION"

with open(input_file, 'r') as f:
    lines = f.readlines()

formatted_lines = []
for line in lines:
    parts = line.strip().split()
    if len(parts) == 3 and is_valid_float(parts[0]) and is_valid_float(parts[1]) and is_valid_float(parts[2]):
        formatted_coordinates = [format(float(coord), '.8f') for coord in parts]
        formatted_line = " ".join(formatted_coordinates) + "\n"
        formatted_lines.append(formatted_line)
    else:
        formatted_lines.append(line)

with open(output_file, 'w') as f:
    f.writelines(formatted_lines)

