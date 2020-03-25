from common.idmap import IdMap
from common.typing import FrequencyInvertedIndex, ResultsWithScore
from indexing.collection_stat import CollectionStatistics
from models.query import Query
from models.weighting import get_tf, get_normalized_tf, get_idf, get_log_tf, get_normalized_log_tf

available_weighting_schemes_query = ["binary", "frequency"]
available_weighting_schemes_document = ["binary", "frequency", "tf_idf_normalize", "tf_idf_logarithmic",
                                        "tf_idf_logarithmic_normalize"]


def query_vectorial_model(query: Query, inverted_index: FrequencyInvertedIndex, id_map: IdMap,
                          collection_stats: CollectionStatistics,weighting_scheme_document: str,
                          weighting_scheme_query: str) -> ResultsWithScore:
    """Handle the provided query using a vectorial model : it returns the name of all the documents
        containing the terms of the query and their score"""
    # Input validation
    if weighting_scheme_document not in available_weighting_schemes_document:
        raise ValueError("Unknown document weighting scheme")
    if weighting_scheme_query not in available_weighting_schemes_query:
        raise ValueError("Unknown query weighting scheme")

    relevant_docs = {}
    nbr_documents = collection_stats.nbr_documents
    norm_query = 0
    query_dict = {}
    for term in query:
        if term in query_dict:
            query_dict[term] += 1
        else:
            query_dict[term] = 1

    for term in query_dict.keys():
        if term in inverted_index:
            # Weighting of query terms
            w_term_query = 0
            if weighting_scheme_query == "binary":
                w_term_query = 1
            if weighting_scheme_query == "frequency":
                w_term_query = query_dict[term]
            norm_query = norm_query + w_term_query * w_term_query

            for document_id in inverted_index[term].keys():
                w_term_doc = 0.
                if document_id not in relevant_docs:
                    relevant_docs[document_id] = 0.

                # Weighting of document regarding the term
                if weighting_scheme_document == "binary":
                    w_term_doc = 1
                if weighting_scheme_document == "frequency":
                    w_term_doc = get_tf(term, document_id, inverted_index)
                if weighting_scheme_document == "tf_idf_normalize":
                    w_term_doc = get_normalized_tf(term, document_id, inverted_index, collection_stats) * \
                                 get_idf(term, inverted_index, collection_stats)
                if weighting_scheme_document == "tf_idf_logarithmic":
                    w_term_doc = get_log_tf(term, document_id, inverted_index) * \
                                 get_idf(term, inverted_index, collection_stats)
                if weighting_scheme_document == "tf_idf_logarithmic_normalize":
                    w_term_doc = get_normalized_log_tf(term, document_id, inverted_index, collection_stats) * \
                                 get_idf(term, inverted_index, collection_stats)

                relevant_docs[document_id] += w_term_doc * w_term_query
    # Final sorting
    ordered_relevant_docs = []
    for doc_id in sorted(relevant_docs, key=relevant_docs.get, reverse=True):
        ordered_relevant_docs.append((id_map[doc_id], relevant_docs[doc_id]))
    return ordered_relevant_docs
