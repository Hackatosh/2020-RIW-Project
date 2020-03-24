from typing import List, Tuple, Optional

from common.helpers import generate_file_paths, serialize_object, deserialize_object
from common.typing import BasicInvertedIndex, FrequencyInvertedIndex, FrequencyInvertedIndexWithPos, InvertedIndex
from common.idmap import IdMap

# DOCUMENT PARSING
from indexing.collection_stat import CollectionStatistics
from indexing.document_stat import DocumentStatistics


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


# INVERTED INDEX BUILDING

def build_inverted_index_basic(collection_directory: str, generate_stats: bool = True) -> \
        Tuple[BasicInvertedIndex, IdMap, Optional[CollectionStatistics]]:
    """ Build the most basic inverted index possible : the index indicates in which documents every word
    appears. To lessen the size of the inverted index, we use document ids instead of document path / name.
    The mapping between ids and documents path (relative to the collection_directory) is stored in IdMap.
    If generate_stats is set to True, it generates the collection statistics along with the index."""
    file_paths = generate_file_paths(collection_directory)
    inverted_index = {}
    id_map = IdMap()
    collection_statistics = CollectionStatistics if generate_stats else None
    for (absolute_path, relative_path) in file_paths:
        parsed_document = parse_document(absolute_path)
        document_id = id_map.insert_str(relative_path)
        for term in parsed_document:
            if term in inverted_index.keys():
                if document_id not in inverted_index[term]:
                    inverted_index[term].append(document_id)
            else:
                inverted_index[term] = [document_id]
        if generate_stats:
            document_statistics = DocumentStatistics(parsed_document)
            collection_statistics.add_document_statistics(document_id, document_statistics)
    return inverted_index, id_map, collection_statistics


def build_frequency_inverted_index(collection_directory: str, generate_stats: bool = True) -> \
        Tuple[FrequencyInvertedIndex, IdMap, Optional[CollectionStatistics]]:
    """ Build a frequency inverted index : the index indicates in which documents every word appears and their number of
     appearances. To lessen the size of the inverted index, we use document ids instead of document path / name.
     The mapping between ids and documents path (relative to the collection_directory) is stored in IdMap.
     If generate_stats is set to True, it generates the collection statistics along with the index."""
    file_paths = generate_file_paths(collection_directory)
    inverted_index = {}
    id_map = IdMap()
    collection_statistics = CollectionStatistics if generate_stats else None
    for (absolute_path, relative_path) in file_paths:
        parsed_document = parse_document(absolute_path)
        document_id = id_map.insert_str(relative_path)
        for term in parsed_document:
            if term in inverted_index.keys():
                if document_id not in inverted_index[term]:
                    inverted_index[term][document_id] = 1
                else:
                    inverted_index[term][document_id] += 1
            else:
                inverted_index[term] = {}
                inverted_index[term][document_id] = 1
        if generate_stats:
            document_statistics = DocumentStatistics(parsed_document)
            print(document_statistics)
            collection_statistics.add_document_statistics(document_id, document_statistics)
    return inverted_index, id_map, collection_statistics


def build_frequency_inverted_index_with_pos(collection_directory: str, generate_stats: bool = True) -> \
        Tuple[FrequencyInvertedIndexWithPos, IdMap, Optional[CollectionStatistics]]:
    """ Build a frequency inverted index with positions : the index indicates in which documents every word
    appears, their number of appearances and their position of appearance in the document.
    To lessen the size of the inverted index, we use document ids instead of document path / name. The mapping between
    ids and documents path (relative to the collection_directory) is stored in IdMap.
    If generate_stats is set to True, it generates the collection statistics along with the index."""
    file_paths = generate_file_paths(collection_directory)
    inverted_index = {}
    id_map = IdMap()
    collection_statistics = CollectionStatistics if generate_stats else None
    for (absolute_path, relative_path) in file_paths:
        parsed_document = parse_document(absolute_path)
        document_id = id_map.insert_str(relative_path)
        for i, term in enumerate(parsed_document):
            if term in inverted_index.keys():
                if document_id not in inverted_index[term]:
                    inverted_index[term][document_id] = (1, [i])
                else:
                    inverted_index[term][document_id][0] += 1
                    inverted_index[term][document_id][1].append(i)
            else:
                inverted_index[term] = {}
                inverted_index[term][document_id] = (1, [i])
        if generate_stats:
            document_statistics = DocumentStatistics(parsed_document)
            collection_statistics.add_document_statistics(document_id, document_statistics)
    return inverted_index, id_map, collection_statistics


# SERIALIZATION / DESERIALIZATION

def save_inverted_index(inverted_index: InvertedIndex, absolute_path: str) -> None:
    """Serialize the provided inverted index to the given absolute path"""
    serialize_object(inverted_index, absolute_path)


def load_basic_inverted_index(absolute_path: str) -> BasicInvertedIndex:
    """Deserialize the basic inverted index located at the given absolute path"""
    return deserialize_object(absolute_path)


def load_frequency_inverted_index(absolute_path: str) -> FrequencyInvertedIndex:
    """Deserialize the frequency inverted index located at the given absolute path"""
    return deserialize_object(absolute_path)


def load_frequency_inverted_index_with_pos(absolute_path: str) -> FrequencyInvertedIndexWithPos:
    """Deserialize the frequency inverted index with positions located at the given absolute path"""
    return deserialize_object(absolute_path)
