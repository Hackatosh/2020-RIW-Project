from typing import Dict

from indexing.document_stat import DocumentStatistics


class CollectionStatistics:
    """ This class represents the statistics for a whole collection. It holds the number of documents in the collection
    and a dictionary with the statistics of every document (the keys are the document ids)."""

    def __init__(self):
        self.__nbr_documents = 0
        self.__documents_stats: Dict[id, DocumentStatistics] = {}

    def __getitem__(self, key: int) -> DocumentStatistics:
        return self.__documents_stats[key]

    @property
    def nbr_documents(self):
        return self.__nbr_documents

    def add_document_statistics(self, document_id: int, document_stats: DocumentStatistics):
        if document_id not in self.__documents_stats:
            self.__nbr_documents += 1
        self.__documents_stats[document_id] = document_stats
