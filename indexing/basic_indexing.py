import pickle
from typing import List, Tuple

from common.helpers import generate_file_paths
from common.typing import BasicInvertedIndex
from common.idmap import IdMap


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


def build_inverted_index_basic(collection_directory: str) -> Tuple[BasicInvertedIndex, IdMap]:
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


def save_inverted_index_pickle(inverted_index: BasicInvertedIndex, absolute_path: str) -> None:
    """Serialize the provided inverted index to the given absolute path using the pickle"""
    with open(absolute_path, "wb") as f:
        pickle.dump(inverted_index, f)
        f.close()


def load_inverted_index_pickle(absolute_path: str) -> BasicInvertedIndex:
    """Deserialize the inverted index located at the given absolute path"""
    with open(absolute_path, 'rb') as fb:
        index = pickle.load(fb)
        return index
