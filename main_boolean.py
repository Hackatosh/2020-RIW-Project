from common.idmap import IdMap
from indexing.basic_indexing import build_inverted_index_basic, save_inverted_index_pickle, load_inverted_index_pickle
import time

from models.boolean_model import query_boolean_model
from models.query import Query

"""
    This script aims to test the basic boolean model.
"""

if __name__ == '__main__':

    global_begin_time = time.time()

    # CONFIG

    imap_path = "TestSerialization/test1.imap"
    invind_path = "TestSerialization/test1.ii"
    collection_path = "Data/0"
    query_path = "Queries/dev_queries/query.2"

    """

    # INDEXING AND SERIALIZATION

    print("Starting indexing...")
    begin_time = time.time()

    inverted_index, id_map = build_inverted_index_basic(collection_path)

    end_time = time.time()
    print(f"Indexing finished. Time taken : {end_time - begin_time}")

    print("Starting serializing...")
    begin_time = time.time()

    id_map.save_to_file(imap_path)
    save_inverted_index_pickle(inverted_index, invind_path)

    end_time = time.time()
    print(f"Serialization finished. Time taken : {end_time - begin_time}")
    """
    # DESERIALIZATION AND QUERY HANDLING

    print("Starting deserializing...")
    begin_time = time.time()

    id_map_loaded = IdMap.load_id_map_file(imap_path)
    inverted_index_loaded = load_inverted_index_pickle(invind_path)

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

    global_end_time = time.time()
    print(f"Script finished. Total time taken : {global_end_time - global_begin_time}")