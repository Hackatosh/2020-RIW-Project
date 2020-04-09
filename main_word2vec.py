from common.idmap import IdMap
from indexing.collection_stat import CollectionStatistics
from indexing.indexing import save_inverted_index, build_frequency_inverted_index, load_frequency_inverted_index
import time
from models.query import Query
from models.word2vec_model import query_word2vec_model
from gensim.models import KeyedVectors


def test_word2vec_model(imap_path: str, invind_path: str, stats_path: str, collection_path: str, query_path: str,
                        word2vec_model_path: str) -> None:

    global_begin_time = time.time()

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
    word2vec_vectors = KeyedVectors.load(word2vec_model_path)

    results = query_word2vec_model(query_loaded, inverted_index_loaded, id_map_loaded, collection_stats_loaded,
                                   word2vec_vectors)

    print("Results :")
    for result in results:
        print(f"Document : {result[0]}, Score: {result[1]}")

    end_time = time.time()
    print(f"Querying finished. Time taken : {end_time - begin_time}")

    global_end_time = time.time()
    print(f"Script finished. Total time taken : {global_end_time - global_begin_time}")


if __name__ == '__main__':
    c_imap_path = "TestSerialization/test1.imap"
    c_invind_path = "TestSerialization/test1.ii"
    c_stats_path = "TestSerialization/test1.stats"
    c_collection_path = "Data/0"
    c_query_path = "Queries/dev_queries/query.2"
    c_word2vec_path = "indexing/word2vec_google.kv"

    test_word2vec_model(c_imap_path, c_invind_path, c_stats_path, c_collection_path, c_query_path, c_word2vec_path)