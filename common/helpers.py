import os
import pickle
from typing import Iterator, Tuple, Any, List


# DOCUMENT PARSING

def parse_document(document_absolute_path: str) -> List[str]:
    """Given the absolute path to the document, returns the list of the filtered and tokenized words, in their order
    of appearance. For now, as the words are already tokenized and there is no stop word list, it just split every
    line of the file. """
    result = []
    with open(document_absolute_path, 'r') as f:
        line = f.readline()
        while line:
            parsed = line.split()
            result += parsed
            line = f.readline()
    return result


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
