import argparse
import time
from main_vectorial import *
from main_boolean import *
from main_word2vec import *
from subprocess import call
from typing import Any

from common.helpers import generate_parser
from common.idmap import IdMap
from indexing.collection_stat import CollectionStatistics
from indexing.indexing import build_inverted_index_basic, save_inverted_index,\
 load_basic_inverted_index, build_frequency_inverted_index, load_frequency_inverted_index

from models.evaluation import parse_out_file, calculate_precision_and_recall
from models.query import Query
from models.vectorial_model import query_vectorial_model
from models.boolean_model import query_boolean_model
from models.word2vec_model import query_word2vec_model




def build_index(name_index: str) -> Any:
    """Creates the index given the name of the index."""
    print("Starting indexing...")

    if name_index =="basic":
        inverted_index, id_map, _ = build_inverted_index_basic(c_collection_path)

        id_map.save_to_file(c_imap_path_basic)
        save_inverted_index(inverted_index, c_invind_path_basic)
    elif name_index == "freq":
        inverted_index, id_map, collection_stats = build_frequency_inverted_index(c_collection_path)

        id_map.save_to_file(c_imap_path_freq)
        save_inverted_index(inverted_index, c_invind_path_freq)
        collection_stats.save_to_file(c_stats_path_freq)

    print("Done indexing and serializing")

def run_query(query: str, engine: str, file_path:bool) -> Any:
    """Runs query routine"""
    if engine in ["vect", "wordtovec"]:

        id_map_loaded = IdMap.load_id_map_file(c_imap_path_freq)
        inverted_index_loaded = load_frequency_inverted_index(c_invind_path_freq)
        collection_stats_loaded = CollectionStatistics.load_collection_statistics_file(c_stats_path_freq)

        query_loaded = Query.load_query(query, file_path)
        if engine == "vect":
            results = query_vectorial_model(query_loaded, inverted_index_loaded, id_map_loaded, collection_stats_loaded,
                                    args.ws_doc, args.ws_query)
        elif engine == "wordtovec":
            word2vec_vectors = KeyedVectors.load(args.kv_vect)
            results = query_word2vec_model(query_loaded, inverted_index_loaded, id_map_loaded, collection_stats_loaded,
                                   word2vec_vectors)

        for i in range(args.limit):
            print("Document : {}, Score : {}".format(results[i][0], results[i][1]))

    if engine == "bool":
        id_map_loaded = IdMap.load_id_map_file(c_imap_path_basic)
        inverted_index_loaded = load_basic_inverted_index(c_invind_path_basic)

        query_loaded = Query.load_query(query, file_path)
        results = query_boolean_model(inverted_index_loaded, id_map_loaded, query_loaded)

        for i in range(args.limit):
            print(results[i], results[i])
    return results

def run_test_routine(query:str, engine:str, file_path:bool, index:str):
    """Run testing routine with evaluation"""
    build_index(index)
    results = run_query(query, engine, file_path)

    relevant_docs = parse_out_file(args.output, c_filter_folder_out_file)
    precision, recall = calculate_precision_and_recall(results, relevant_docs)
    print(f"Precision : {precision}")
    print(f"Recall : {recall}")



"""
This script runs the whole research engine given some command line arguments.
"""
# Creating parser for command line arguments
parser = generate_parser()
# Parsing arguments
args = parser.parse_args()
if not (args.query or args.index):
    parser.error("Please specify at least --query and/or --index flags")

# Initialisation
# Serialization paths
c_imap_path_basic = "Serialization/basic.imap"
c_invind_path_basic = "Serialization/basic.ii"
c_stats_path_freq = "Serialization/freq.stats"
c_imap_path_freq = "Serialization/freq.imap"
c_invind_path_freq = "Serialization/freq.ii"


# Collection, queries and out
c_collection_path = "Data"
c_filter_folder_out_file = "0"
c_word2vec_path = 'indexing/word2vec_google.kv'

# INDEXING AND SERIALIZATION
if args.test:
    run_test_routine(args.query, args.engine, args.file_pat, args.index)
else:
    if args.index:
        build_index(args.index)

    if args.query:
        run_query(args.query, args.engine, args.file_path)
