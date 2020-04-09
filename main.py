import argparse
import time
from main_vectorial import *
from main_boolean import *
from subprocess import call

from indexing.indexing import build_inverted_index_basic, save_inverted_index, load_basic_inverted_index, build_frequency_inverted_index


parser = argparse.ArgumentParser(prog='DuckDuckQwant')
parser.add_argument('--version', action='version', version='%(prog)s 0.1')
parser.add_argument('--query', '-q', help="your query OR the path to your query file. \
Example of query : 'how to replace google'. Example of path : \
'Queries/dev_queries/query.1'. Flag --file must be added in order for the \
argument to be considered as a path.")
parser.add_argument('--engine', '-e', default="vect",help="choose your search engine.\
 It must be in this list : 'bool', 'vect', 'wordtovec'. Default is 'vect'",
                    choices=['bool', 'vect', 'wordtovec'])
parser.add_argument("--file-path", nargs="?", default=False, const=True, help="Add \
this flag if you are using a file as an input for your queries.")
parser.add_argument("--index", choices=['basic', 'freq', 'pos'],
help="recreates the index with specified type of index among 'basic', 'freq',  'pos'")
parser.add_argument("--limit", "-l", type=int, default=20, help="Specify the \
number of results display. Default is 20")

args = parser.parse_args()

# Serialization paths
c_imap_path = "TestSerialization/test1.imap"
c_invind_path = "TestSerialization/test1.ii"
c_stats_path = "TestSerialization/test1.stats"

# Collection, queries and out
c_collection_path = "Data"
c_filter_folder_out_file = "0"
c_query_path = "Queries/dev_queries/query.1"
c_out_file = "Queries/dev_output/1.out"

# INDEXING AND SERIALIZATION
try:
    if args.index =="basic":
        inverted_index, id_map, _ = build_inverted_index_basic(c_collection_path)
        id_map.save_to_file(c_imap_path)
        save_inverted_index(inverted_index, c_invind_path)

    elif args.index == "freq":
        inverted_index, id_map, collection_stats = build_frequency_inverted_index(c_collection_path)
        id_map.save_to_file(c_imap_path)
        save_inverted_index(inverted_index, c_invind_path)
        collection_stats.save_to_file(c_stats_path)
except Exception as e:
    print(e)
print("Starting serializing...")


if args.engine == "vect":

    # Weighting schemes
    c_weighting_scheme_document = "okapi_bm_25"
    c_weighting_scheme_query = "frequency"

    results = test_vectorial_model(c_imap_path, c_invind_path, c_stats_path, c_collection_path, args.query,
                         c_out_file, c_filter_folder_out_file, c_weighting_scheme_document, c_weighting_scheme_query, args.file_path)
    for i in range(args.limit):
        print(results[i][0], results[i][1])
if args.engine == "bool":
    test_boolean_model(c_imap_path, c_invind_path, c_collection_path, args.query, c_out_file, c_filter_folder_out_file, args.file_path)
