from typing import Optional

from common.typing import ResultsWithScore
from common.idmap import IdMap
from indexing.collection_stat import CollectionStatistics
from indexing.indexing import save_inverted_index, build_frequency_inverted_index, load_frequency_inverted_index
import time

from models.evaluation import parse_out_file, calculate_precision_and_recall
from models.query import Query
from models.vectorial_model import query_vectorial_model


def test_vectorial_model(imap_path: str, invind_path: str, stats_path: str, collection_path: str, query_path: str,
                         out_file: str, filter_folder_out_file: Optional[str],
                         weighting_scheme_document: str, weighting_scheme_query: str, query_path_given: bool) -> ResultsWithScore:
    """
        This script aims to test the vectorial model.
        imap_path, invind_path and stats_path are used for serialization and deserialization of the IdMap, the Inverted
        Index and the Collection Statistics.
        collection_path is the path to the main directory which contains all the documents of the collection.
        query_path is the path to the text file containing the query.
        out_file is the path to the text file containing the relevant documents and filter_folder_out_file is the
        name of the subfolder of the collection you want to keep relevant docs for.
        weighting_scheme_document and weighting_scheme_query are the weighting used by the vectorial model.
    """

    global_begin_time = time.time()
    # DESERIALIZATION AND QUERY HANDLING

    print("Starting deserializing...")
    begin_time = time.time()

    id_map_loaded = IdMap.load_id_map_file(imap_path)
    inverted_index_loaded = load_frequency_inverted_index(invind_path)
    collection_stats_loaded = CollectionStatistics.load_collection_statistics_file(stats_path)

    end_time = time.time()
    print(f"Deserialization finished. Time taken : {end_time - begin_time}")

    print("Starting querying...")
    begin_time = time.time()

    query_loaded = Query.load_query(query_path, query_path_given)
    results = query_vectorial_model(query_loaded, inverted_index_loaded, id_map_loaded, collection_stats_loaded,
                                    weighting_scheme_document,
                                    weighting_scheme_query)

    #print("Results :")
    #for result in results:
    #    print(f"Document : {result[0]}, Score: {result[1]}")

    end_time = time.time()
    print(f"Querying finished. Time taken : {end_time - begin_time}")

    # EVALUATION

    print("Starting evaluation...")
    begin_time = time.time()

    relevant_docs = parse_out_file(out_file, filter_folder_out_file)
    precision, recall = calculate_precision_and_recall(results, relevant_docs)
    print(f"Precision : {precision}")
    print(f"Recall : {recall}")

    end_time = time.time()
    print(f"Evaluation finished. Time taken : {end_time - begin_time}")

    global_end_time = time.time()
    print(f"Script finished. Total time taken : {global_end_time - global_begin_time}")
    return results

if __name__ == '__main__':
    # Serialization paths
    c_imap_path = "TestSerialization/test1.imap"
    c_invind_path = "TestSerialization/test1.ii"
    c_stats_path = "TestSerialization/test1.stats"

    # Collection, queries and out
    c_collection_path = "Data/0"
    c_filter_folder_out_file = "0"
    c_query_path = "Queries/dev_queries/query.2"
    c_out_file = "Queries/dev_output/2.out"

    # Weighting schemes
    c_weighting_scheme_document = "okapi_bm_25"
    c_weighting_scheme_query = "frequency"

    test_vectorial_model(c_imap_path, c_invind_path, c_stats_path, c_collection_path, c_query_path,
                         c_out_file, c_filter_folder_out_file, c_weighting_scheme_document, c_weighting_scheme_query, True)
