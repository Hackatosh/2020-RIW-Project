from collections import Counter
from typing import List


class DocumentStatistics:
    """ This class represents the statistics for one document of the collection"""

    def __init__(self, parsed_document: List[str]):
        """Build the object given a parsed document, which is a list of the tokenized terms of the document"""
        counter = Counter()
        length_doc = 0
        for term in parsed_document:
            length_doc += 1
            counter.update([term])
        self.__max_freq = counter.most_common(1)[0][1] # most_common(1) eturns a list of 1 element
        self.__nb_unique_terms = len(counter.items())
        tf_moy = sum(counter.values())
        self.__avg_freq = tf_moy / len(counter.items())
        self.__length_doc = length_doc

    @property
    def max_freq(self) -> float:
        return self.__max_freq

    @property
    def nb_unique_terms(self) -> int:
        return self.__nb_unique_terms

    @property
    def avg_freq(self) -> float:
        return self.__avg_freq

    @property
    def length_doc(self) -> int:
        return self.__length_doc
