import os
import pickle
from typing import Iterator, Tuple, Any, List
from models.query import Query
import argparse


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

def generate_parser() -> Any:
    """ Generates the parser for the command line argument of the research
    tool"""
    parser = argparse.ArgumentParser(prog='DuckDuckQwant')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    parser.add_argument('--query', '-q', help="your query OR the path to your query file. \
    Example of query : 'how to replace google'. Example of path : \
    'Queries/dev_queries/query.1'. Flag --file-path must be added in order for the \
    argument to be considered as a path.")
    parser.add_argument('--engine', '-e', default="vect",help="choose your search engine.\
     It must be in this list : 'bool', 'vect', 'wordtovec'. Default is 'vect'",
                        choices=['bool', 'vect', 'wordtovec'])
    parser.add_argument("--file-path", nargs="?", default=False, const=True, help="Add \
    this flag if you are using a file as an input for your queries.")
    parser.add_argument("--index", nargs="?", const="freq", choices=['basic', 'freq', 'pos'],
    help="recreates the index with specified type of index among 'basic', 'freq',  'pos'")
    parser.add_argument("--output", "-o", help="output file")
    parser.add_argument("--limit", "-l", type=int, default=20, help="Specify the \
    number of results display. Default is 20")
    parser.add_argument("--ws-doc", default="okapi_bm_25", help="Path to weighting scheme doc for \
    vectorial model")
    parser.add_argument("--ws-query", default="frequency", help="Path to weighting scheme query for \
    vectorial model")
    parser.add_argument("--kv-vect", help="Path to word2vec model")
    parser.add_argument("--test", nargs="?", default=False, const=True,
                help="Add this flag if you wish to run the testing routine")
    return parser

def get_vocabulary(main_directory: str) -> set:
    """Return a set containing all the different words in the dataset : the vocabulary"""
    file_paths = generate_file_paths(main_directory)
    vocabulary = set()
    for (absolute_path, relative_path) in file_paths:
        parsed_document = parse_document(absolute_path)
        for word in parsed_document:
            vocabulary.add(word)
    return vocabulary
