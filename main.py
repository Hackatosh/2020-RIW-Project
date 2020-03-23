from indexing.idmap import IdMap
from indexing.indexing import build_inverted_index_basic, save_inverted_index_pickle, load_inverted_index_pickle
import time

imap_path = "test_serialization/test1.imap"
invind_path = "test_serialization/test1.ii"

print("Starting indexing...")
begin_time = time.time()

#inverted_index, idmap = build_inverted_index_basic("Queries")
#idmap.save_to_file(imap_path)
#save_inverted_index_pickle(inverted_index, invind_path)

id_map = IdMap.load_id_map_file(imap_path)
inverted_index = load_inverted_index_pickle(invind_path)

print(inverted_index)

end_time = time.time()
print(f"Temps d'execution {end_time-begin_time}")
