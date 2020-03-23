import os
from typing import Iterator, List


def generate_file_paths(main_directory: str) -> Iterator[str]:
    """Recursively browse the directory provided and create a generator containing the name
    of every file contained in the folder or its subfolders"""
    for (dirpath, dirnames, filenames) in os.walk(main_directory):
        for filename in filenames:
            yield os.path.join(dirpath, filename)


def parse_document(document_path: str) -> List[str]:
    """Given the path to the document, returns the list of the filtered and tokenized words, in their order of appearance.
    For now, as the words are already tokenized and there is no stop word list, it just split every line of the file."""
    result = []
    with open(document_path, 'r') as f:
        line = f.readline()
        while line:
            parsed = line.split()
            result += parsed
            line = f.readline()
    return result


print(parse_document("test.txt"))
