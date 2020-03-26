from typing import Optional, Union
from common.typing import ResultsWithoutScore, ResultsWithScore


def parse_out_file(out_file_path: str, filter_folder: Optional[str] = None) -> ResultsWithoutScore:
    """Given the absolute path to the out file, returns the list of the relevant documents written in this file.
    If you do not want to keep the results corresponding to the whole dataset, you can provide a sub-folder which the
    results should belong to using filter_folder"""
    if filter_folder is not None and not filter_folder.startswith("/"):
        raise ValueError("filter_folder should be a relative path like '0/'")
    if filter_folder is not None and not filter_folder.endswith("/"):
        filter_folder += "/"
    result = []
    with open(out_file_path, 'r') as f:
        line = f.readline()
        while line:
            if filter_folder is None:
                result.append(line)
            if filter_folder is not None and line.startswith(filter_folder):
                result.append(line[len(filter_folder):])
            line = f.readline()
    return result


def calculate_precision_and_recall(results: Union[ResultsWithoutScore,ResultsWithScore],
                                   relevant_docs: ResultsWithoutScore) -> (float, float):
    """ Given the results of a model and the relevant documents, it calculates the precision and recall"""
    if len(results) == 0:
        return 1, 0
    if len(relevant_docs) == 0:
        raise ValueError("No relevant documents provided !")
    if type(results[0]) == tuple:
        results = strip_scores(results) # Convert ResultsWithScore to ResultsWithoutScore
    nbr_relevant_selected = 0
    for result in results:
        if result in relevant_docs:
            nbr_relevant_selected += 1
    precision = nbr_relevant_selected / len(results)
    recall = nbr_relevant_selected / len(relevant_docs)
    return precision, recall


def strip_scores(results: ResultsWithScore) -> ResultsWithoutScore:
    return [result[0] for result in results]