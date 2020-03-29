from typing import Optional

from common.idmap import IdMap
from indexing.indexing import build_inverted_index_basic, save_inverted_index, load_basic_inverted_index
import time

from models.boolean_model import query_boolean_model
from models.evaluation import calculate_precision_and_recall, parse_out_file
from models.query import Query

"""
    This script aims to test the basic boolean model.
"""


def test_boolean_model(imap_path: str, invind_path: str, collection_path: str, query_path: str,
                       out_file: str, filter_folder_out_file: Optional[str],) -> None:
    """
        This script aims to test the basic boolean model.
        imap_path and invind_path are used for serialization and deserialization of the IdMap and the Inverted Index.
        collection_path is the path to the main directory which contains all the documents of the collection.
        query_path is the path to the text file containing the query.
        out_file is the path to the text file containing the relevant documents and filter_folder_out_file is the
        name of the subfolder of the collection you want to keep relevant docs for.
        """
    global_begin_time = time.time()

    # INDEXING AND SERIALIZATION

    print("Starting indexing...")
    begin_time = time.time()

    inverted_index, id_map, _ = build_inverted_index_basic(collection_path)

    end_time = time.time()
    print(f"Indexing finished. Time taken : {end_time - begin_time}")

    print("Starting serializing...")
    begin_time = time.time()

    id_map.save_to_file(imap_path)
    save_inverted_index(inverted_index, invind_path)

    end_time = time.time()
    print(f"Serialization finished. Time taken : {end_time - begin_time}")

    # DESERIALIZATION AND QUERY HANDLING

    print("Starting deserializing...")
    begin_time = time.time()

    id_map_loaded = IdMap.load_id_map_file(imap_path)
    inverted_index_loaded = load_basic_inverted_index(invind_path)

    end_time = time.time()
    print(f"Deserialization finished. Time taken : {end_time - begin_time}")

    print("Starting querying...")
    begin_time = time.time()

    query_loaded = Query.build_from_file(query_path)

    results = query_boolean_model(inverted_index_loaded, id_map_loaded, query_loaded)

    print("Results :")
    for result in results:
        print(result)

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


if __name__ == '__main__':

    # Serialization paths
    c_imap_path = "TestSerialization/test1.imap"
    c_invind_path = "TestSerialization/test1.ii"

    # Collection, queries and out
    c_collection_path = "Data/0"
    c_filter_folder_out_file = "0"
    c_query_path = "Queries/dev_queries/query.1"
    c_out_file = "Queries/dev_output/1.out"

    test_boolean_model(c_imap_path, c_invind_path, c_collection_path, c_query_path, c_out_file, c_filter_folder_out_file)
