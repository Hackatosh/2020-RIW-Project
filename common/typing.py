from typing import Dict, List, Union, Tuple

"""This type represents the most basic inverted index possible : each key is a term present in the collection and 
is associated to the list of the document ids in which the term appears."""
BasicInvertedIndex = Dict[str, List[int]]

"""This type represents a frequency inverted index : each key is a term present in the collection and 
is associated a dictionary holding all the document ids in which the term appears (as keys) and the number of 
appearances (as values)."""
FrequencyInvertedIndex = Dict[str, Dict[int, int]]

"""This type represents a frequency inverted index with position : each key is a term present in the collection and 
is associated a dictionary holding all the document ids in which the term appears (as keys) and a tuple with the number 
of appearances and the list of positions of the term in the document (as values)."""
FrequencyInvertedIndexWithPos = Dict[str, Dict[int, Tuple[int, List[int]]]]

InvertedIndex = Union[BasicInvertedIndex, FrequencyInvertedIndex, FrequencyInvertedIndexWithPos]

"""This type represents the list of results returned by a model without score"""
ResultsWithoutScore = List[str]

"""This type represents the list of results returned by a model with score : it returns a list of tuples, holding the 
name of the document and its score."""
ResultsWithScore = List[Tuple[str, float]]
