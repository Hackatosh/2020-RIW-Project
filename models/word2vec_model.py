from common.idmap import IdMap
from common.typing import FrequencyInvertedIndex, ResultsWithScore
from indexing.collection_stat import CollectionStatistics
from models.query import Query
from models.weighting import get_tf, get_normalized_tf, get_idf, get_log_tf, get_normalized_log_tf
from gensim.models import KeyedVectors


def query_word2vec_model(query: Query, inverted_index: FrequencyInvertedIndex, id_map: IdMap,
                         collection_stats: CollectionStatistics, word2vec_vectors: KeyedVectors) -> ResultsWithScore:
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
            print(term)
            # Weighting of query terms
            w_term_query = query_dict[term]
            norm_query = norm_query + w_term_query * w_term_query
            similar_terms = word2vec_vectors.most_similar(term)  # top 10 similar terms based on word2vec model
            similar_terms.append((term, 1))
            print(similar_terms)
            for similar_term, similarity in similar_terms:
                print(similar_term)
                if similar_term in inverted_index:
                    for document_id in inverted_index[similar_term].keys():
                        w_term_doc = 0.
                        if document_id not in relevant_docs:
                            relevant_docs[document_id] = 0.

                        w_term_doc = get_normalized_log_tf(similar_term, document_id, inverted_index, collection_stats)
                        w_term_doc *= get_idf(similar_term, inverted_index, collection_stats)
                        w_term_doc *= similarity
                        relevant_docs[document_id] += w_term_doc * w_term_query
    # Final sorting
    ordered_relevant_docs = []
    for doc_id in sorted(relevant_docs, key=relevant_docs.get, reverse=True):
        ordered_relevant_docs.append((id_map[doc_id], relevant_docs[doc_id]))
    return ordered_relevant_docs
