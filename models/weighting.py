from math import log

from common.typing import FrequencyInvertedIndex
from indexing.collection_stat import CollectionStatistics


def get_tf(term: str, document_id: int, frequency_inverted_index: FrequencyInvertedIndex) -> int:
    """Get the frequency of the term (tf means 'term frequency')"""
    if term in frequency_inverted_index:
        return frequency_inverted_index[term][document_id]
    else:
        return 0


def get_log_tf(term: str, document_id: int, frequency_inverted_index: FrequencyInvertedIndex) -> float:
    """ Get the log frequency of the term"""
    tf = get_tf(term, document_id, frequency_inverted_index)
    if tf > 0:
        return 1 + log(tf)
    else:
        return 0


def get_normalized_tf(term: str, document_id: int, frequency_inverted_index: FrequencyInvertedIndex,
                      collection_stats: CollectionStatistics) -> float:
    """ Get the frequency of the term normalized using the maximum frequency of the document"""
    tf = get_tf(term, document_id, frequency_inverted_index)
    normalized_tf = 0.5 + 0.5 * (tf / collection_stats.get_document_statistics(document_id).max_freq)
    return normalized_tf


def get_normalized_log_tf(term: str, document_id: int, frequency_inverted_index: FrequencyInvertedIndex,
                          collection_stats: CollectionStatistics) -> float:
    """ Get the log frequency of the term normalized using the average frequency of the document"""
    log_tf = get_log_tf(term, document_id, frequency_inverted_index)
    normalized_log_tf = log_tf / (1 + log(collection_stats.get_document_statistics(document_id).avg_freq))
    return normalized_log_tf


def get_okapi_bm_25(term: str, document_id: int, frequency_inverted_index: FrequencyInvertedIndex,
                    collection_stats: CollectionStatistics, k1: float = 1.6, b: float = 0.75) -> float:
    tf = get_tf(term, document_id, frequency_inverted_index)
    d_length = collection_stats.get_document_statistics(document_id).length_doc
    avg_length = collection_stats.avg_document_length
    okapi = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (d_length / avg_length)))
    return okapi


def get_idf(term: str, frequency_inverted_index: FrequencyInvertedIndex,
            collection_stats: CollectionStatistics) -> float:
    """Global indicator of the term frequency in the whole corpus. This can be used for weigthing.-"""
    if term in frequency_inverted_index:
        return log(collection_stats.nbr_documents / len(frequency_inverted_index[term].keys()))
    else:
        return log(collection_stats.nbr_documents)
