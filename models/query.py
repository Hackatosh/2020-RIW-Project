from typing import Any


class Query:
    """This class is used to store a query sequence."""

    def __init__(self, raw_query: str):
        """Constructs a query. The query must be pre-processed (filtered + tokenized)"""
        self.query_words = raw_query.split(" ")

    def __iter__(self):
        for w in self.query_words:
            yield w

    def __eq__(self, other: Any):
        if not isinstance(other, Query):
            # don't attempt to compare against unrelated types
            return False
        return self.query_words == other.query_words

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return " ".join(self.query_words)

    __repr__ = __str__

    @staticmethod
    def build_from_file(path: str) -> "Query":
        """Build a Query object by parsing the text file located at the given path"""
        with open(path, 'r') as f:
            line = f.readline()
            line = line.rstrip()  # Trailing endline can cause bugs. WARNING : You can't see them with a print !
            return Query(line)
