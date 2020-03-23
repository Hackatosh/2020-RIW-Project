import os
from typing import Iterator, List, Dict, Tuple

from idmap import IdMap

InvertedIndex = Dict[str, List[int]]


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


def parse_document(document_absolute_path: str) -> List[str]:
    """Given the absolute path to the document, returns the list of the filtered and tokenized words, in their order of appearance.
    For now, as the words are already tokenized and there is no stop word list, it just split every line of the file."""
    result = []
    with open(document_absolute_path, 'r') as f:
        line = f.readline()
        while line:
            parsed = line.split()
            result += parsed
            line = f.readline()
    return result


def build_inverted_index_basic(collection_directory: str) -> Tuple[InvertedIndex, IdMap]:
    """ Build the most basic inverted index possible : the index indicates in which documents every word
    appears. To lessen the size of the inverted index, we use document ids instead of document path / name.
    The mapping between ids and documents path (relative to the collection_directory) is stored in IdMap."""
    file_paths = generate_file_paths(collection_directory)
    inverted_index = {}
    id_map = IdMap()
    for (absolute_path, relative_path) in file_paths:
        parsed_document = parse_document(absolute_path)
        document_id = id_map.insert_str(relative_path)
        for term in parsed_document:
            if term in inverted_index.keys():
                if document_id not in inverted_index[term]:
                    inverted_index[term].append(document_id)
            else:
                inverted_index[term] = [document_id]
    return inverted_index, id_map


print("TEST")

for file in generate_file_paths("Queries"):
    print(file)
