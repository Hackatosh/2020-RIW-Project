from typing import List

from common.idmap import IdMap
from common.typing import BasicInvertedIndex
from models.query import Query


def query_boolean_model(inverted_index: BasicInvertedIndex, id_map: IdMap, query: Query) -> List[str]:
    """Handle the provided query using a boolean model : it returns the name of all the documents
    containing the terms of the query"""
    result_set = None
    for term in query:
        if term not in inverted_index:
            # The query has a term which is not in any document
            return []
        else:
            if result_set is None:
                result_set = set(inverted_index[term])
            else:
                result_set = result_set.intersection(set(inverted_index[term]))
    if result_set is None:
        return []
    else:
        document_ids = list(result_set)
        return [id_map[id] for id in document_ids]
