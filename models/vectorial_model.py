from collections import Counter

from common.typing import FrequencyInvertedIndex
from indexing.collection_stat import CollectionStatistics
from models.query import Query


def query_vectorial_model(query: Query, inverted_index: FrequencyInvertedIndex, collection_stats: CollectionStatistics,
                          weighting_scheme_document: str, weighting_scheme_query: str):
    relevant_docs = {}
    counter_query = Counter()
    nbr_documents = collection_stats.nbr_documents
    norm_query = 0
    for term in query:
        if term in inverted_index:
            w_term_query = 0.
            counter_query.update([term])
            if weighting_scheme_query == "binary":
                w_term_query = 1
            if weighting_scheme_query == "frequency":
                w_term_query = counter_query[term]
            norm_query = norm_query + w_term_query * w_term_query
            for doc in inverted_index[term]:
                w_term_doc = 0.
                relevant_docs[doc] = 0.
                if weighting_scheme_document == "binary":
                    w_term_doc = 1
                if weighting_scheme_document == "frequency":
                    w_term_doc = get_tf(term, doc, inverted_index)
                if weighting_scheme_document == "tf_idf_normalize":
                    w_term_doc = get_tf_normalise(term, doc, inverted_index, stats_collection) * get_idf(term,
                                                                                                         inverted_index,
                                                                                                         nb_doc)
                if weighting_scheme_document == "tf_idf_logarithmic":
                    w_term_doc = get_tf_logarithmique(term, doc, inverted_index) * get_idf(term, inverted_index, nb_doc)
                if weighting_scheme_document == "tf_idf_logarithmic_normalize":
                    w_term_doc = get_tf_logarithme_normalise(term, doc, inverted_index, stats_collection) * get_idf(
                        term, inverted_index, nb_doc)
                relevant_docs[doc] = relevant_docs[doc] + w_term_doc * w_term_query
    ordered_relevant_docs = OrderedDict(sorted(relevant_docs.items(), key=lambda t: t[1], reverse=True))
    return ordered_relevant_docs
