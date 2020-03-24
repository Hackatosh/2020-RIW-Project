from common.idmap import IdMap
from indexing.collection_stat import CollectionStatistics
from indexing.indexing import save_inverted_index, build_frequency_inverted_index, load_frequency_inverted_index
import time

from models.query import Query
from models.vectorial_model import query_vectorial_model

"""
    This script aims to test the vectorial model.
"""

if __name__ == '__main__':

    global_begin_time = time.time()

    # CONFIG

    imap_path = "TestSerialization/test1.imap"
    invind_path = "TestSerialization/test1.ii"
    stats_path = "TestSerialization/test1.stats"
    collection_path = "Data/0"
    query_path = "Queries/dev_queries/query.2"
    weighting_scheme_document = "frequency"
    weighting_scheme_query = "frequency"

    # INDEXING AND SERIALIZATION

    print("Starting indexing...")
    begin_time = time.time()

    inverted_index, id_map, collection_stats = build_frequency_inverted_index(collection_path)

    end_time = time.time()
    print(f"Indexing finished. Time taken : {end_time - begin_time}")

    print("Starting serializing...")
    begin_time = time.time()

    id_map.save_to_file(imap_path)
    save_inverted_index(inverted_index, invind_path)
    collection_stats.save_to_file(stats_path)

    end_time = time.time()
    print(f"Serialization finished. Time taken : {end_time - begin_time}")

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

    query_loaded = Query.build_from_file(query_path)

    results = query_vectorial_model(query_loaded, inverted_index_loaded, id_map_loaded, collection_stats_loaded,
                                    weighting_scheme_document,
                                    weighting_scheme_query)

    print("Results :")
    for result in results:
        print(f"Document : {result[0]}, Score: {result[1]}")

    end_time = time.time()
    print(f"Querying finished. Time taken : {end_time - begin_time}")

    global_end_time = time.time()
    print(f"Script finished. Total time taken : {global_end_time - global_begin_time}")
