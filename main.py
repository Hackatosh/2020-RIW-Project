import os
from typing import Iterator


def generate_file_paths(main_directory: str) -> Iterator[str]:
    """Recursively browse the directory provided and create a generator containing the name
    of every file contained in the folder or its subfolders"""
    for (dirpath, dirnames, filenames) in os.walk(main_directory):
        for filename in filenames:
            yield os.path.join(dirpath, filename)


file_paths = generate_file_paths("Data")

for file_path in file_paths:
    print(file_path)