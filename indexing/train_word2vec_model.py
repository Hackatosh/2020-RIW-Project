from gensim.models import Word2Vec
from common.helpers import generate_file_paths, parse_document
import time


def train_word2vec_model(collection_directory: str) -> Word2Vec:

    file_paths = generate_file_paths(collection_directory)
    corpus = []
    for (absolute_path, relative_path) in file_paths:
        parsed_document = parse_document(absolute_path)
        corpus.append(parsed_document)
    print(len(corpus))
    start = time.time()
    model = Word2Vec(corpus, min_count=5, size=100, workers=4, window=5, iter=10)
    print('Training time :', time.time() - start)
    return model


def save_word2vec_model(model: Word2Vec, absolute_path: str) -> None:
    model.wv.save(absolute_path)


if __name__ == '__main__':
    collection_directory = '../Data'
    path_to_model = 'word2vec.kv'
    model = train_word2vec_model(collection_directory)
    save_word2vec_model(model, path_to_model)