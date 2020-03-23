import os
from typing import Iterator, Tuple


def generate_file_paths(main_directory: str) -> Iterator[Tuple[str, str]]:
    """Recursively browse the directory provided and create a generator containing Tuples composed of
    the absolute path and the relative path (relative to main_directory) of every file contained in the folder or its
    subfolders"""
    wd = os.getcwd()
    for (dirpath, dirnames, filenames) in os.walk(main_directory):
        for filename in filenames:
            absolute_path = os.path.join(wd, dirpath, filename)
            relative_path = os.path.relpath(absolute_path, main_directory)
            yield absolute_path, relative_path
