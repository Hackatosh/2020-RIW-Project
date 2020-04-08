import os
import pickle
from typing import Iterator, Tuple, Any
from models.query import Query

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


def serialize_object(o: Any, absolute_path: str) -> None:
    """ Serialize the object and save it at the given absolute path using the pickle module. For proper typing,
    this must be wrapped."""
    with open(absolute_path, "wb") as f:
        pickle.dump(o, f)
        f.close()


def deserialize_object(absolute_path: str) -> Any:
    """Deserialize the object located at the given absolute path using the pickle module. For proper typing,
    this must be wrapped."""
    with open(absolute_path, 'rb') as fb:
        o = pickle.load(fb)
        return o

def load_query(absolute_path: str, consider_as_path: bool) -> Query:
    if consider_as_path:
        return Query.build_from_file(absolute_path)
    else:
        return Query(absolute_path)
