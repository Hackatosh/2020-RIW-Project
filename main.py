import argparse
import time
from main_vectorial import *
from main_boolean import *
from subprocess import call

from common.helpers import generate_parser
from common.idmap import IdMap
from indexing.collection_stat import CollectionStatistics
from indexing.indexing import build_inverted_index_basic, save_inverted_index,\
 load_basic_inverted_index, build_frequency_inverted_index, load_frequency_inverted_index

from models.evaluation import parse_out_file, calculate_precision_and_recall
from models.query import Query
from models.vectorial_model import query_vectorial_model
from models.boolean_model import query_boolean_model

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
c_stats_path_freq = "Serialization/test1.stats"
c_imap_path_freq = "Serialization/freq.imap"
c_invind_path_freq = "Serialization/freq.ii"


# Collection, queries and out
c_collection_path = "Data/0"
c_filter_folder_out_file = "0"
c_query_path = "Queries/dev_queries/query.1"
c_out_file = "Queries/dev_output/1.out"

# INDEXING AND SERIALIZATION
if args.index =="basic":
    print("Starting indexing...")
    inverted_index, id_map, _ = build_inverted_index_basic(c_collection_path)
    print("Strating serliazing...")
    id_map.save_to_file(c_imap_path_basic)
    save_inverted_index(inverted_index, c_invind_path_basic)
elif args.index == "freq":
    inverted_index, id_map, collection_stats = build_frequency_inverted_index(c_collection_path)
    id_map.save_to_file(c_imap_path_freq)
    save_inverted_index(inverted_index, c_invind_path_freq)
    collection_stats.save_to_file(c_stats_path_freq)


if args.engine == "vect":

    # Weighting schemes
    c_weighting_scheme_document = args.ws_doc if args.ws_doc else "okapi_bm_25"
    c_weighting_scheme_query = args.ws_query if args.ws_query else "frequency"

    if args.test:
        results = test_vectorial_model(c_imap_path_freq, c_invind_path_freq, c_stats_path_freq, c_collection_path, args.query,
                         c_out_file, c_filter_folder_out_file, c_weighting_scheme_document, c_weighting_scheme_query, args.file_path)
    else:
        id_map_loaded = IdMap.load_id_map_file(c_imap_path_freq)
        inverted_index_loaded = load_frequency_inverted_index(c_invind_path_freq)
        collection_stats_loaded = CollectionStatistics.load_collection_statistics_file(c_stats_path_freq)

        query_loaded = Query.load_query(args.query, args.file_path)
        results = query_vectorial_model(query_loaded, inverted_index_loaded, id_map_loaded, collection_stats_loaded,
                                    c_weighting_scheme_document,
                                    c_weighting_scheme_query)

    for i in range(args.limit):
        print(results[i][0], results[i][1])

if args.engine == "bool":
    if args.test:
        results = test_boolean_model(c_imap_path_basic, c_invind_path_basic, c_collection_path, args.query, c_out_file, c_filter_folder_out_file, args.file_path)
    else:
        id_map_loaded = IdMap.load_id_map_file(c_imap_path_basic)
        inverted_index_loaded = load_basic_inverted_index(c_invind_path_basic)

        query_loaded = Query.load_query(args.query, args.file_path)
        results = query_boolean_model(inverted_index_loaded, id_map_loaded, query_loaded)

    for i in range(args.limit):
        print(results[i], results[i])
