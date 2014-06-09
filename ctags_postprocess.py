#!/usr/bin/env python

import os.path
import sys


def find_python_package_root(file_path):
    current_directory = os.path.dirname(file_path)
    while current_directory:
        if os.path.isfile(os.path.join(current_directory, "setup.py")):
            return current_directory
        current_directory = os.path.dirname(current_directory)
    return None


output_lines = []

for line in sys.stdin:
    data = line.split("\t")
    tag_name = data[0]
    file_path = data[1]

    if file_path.endswith(".py"):
        _, _, tag_type = line.partition(';"\t')  # wow magical ctags sequence woot woot
        tag_type = tag_type[:1]
        if tag_type in ["v", "i"]:
            continue

        package_root = find_python_package_root(file_path)
        if package_root is not None:
            module_full_name = os.path.relpath(file_path, package_root)
            module_full_name = module_full_name[:-len(".py")]
            module_full_name = module_full_name.replace("/", ".")

            new_data = list(data)
            new_data[0] = module_full_name + ";" + tag_name
            output_lines.append("\t".join(new_data))

    output_lines.append(line)

output_lines.sort()
sys.stdout.write("".join(output_lines))
