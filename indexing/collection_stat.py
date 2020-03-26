from typing import Dict

from common.helpers import serialize_object, deserialize_object
from indexing.document_stat import DocumentStatistics


class CollectionStatistics:
    """ This class represents the statistics for a whole collection. It holds the number of documents in the collection
    and a dictionary with the statistics of every document (the keys are the document ids)."""

    def __init__(self):
        self.__nbr_documents = 0
        self.__documents_stats: Dict[id, DocumentStatistics] = {}

    def get_document_statistics(self, document_id: int) -> DocumentStatistics:
        return self.__documents_stats[document_id]

    def add_document_statistics(self, document_id: int, document_stats: DocumentStatistics) -> None:
        if document_id not in self.__documents_stats:
            self.__nbr_documents += 1
        self.__documents_stats[document_id] = document_stats

    @property
    def nbr_documents(self) -> int:
        return self.__nbr_documents

    def save_to_file(self, absolute_path: str) -> None:
        """ Serialize the object and save it at the given absolute path"""
        serialize_object(self, absolute_path)

    @staticmethod
    def load_collection_statistics_file(absolute_path: str) -> "CollectionStatistics":
        """Deserialize the CollectionStatistics object located at the given absolute path"""
        return deserialize_object(absolute_path)
