from gensim.models import Word2Vec, KeyedVectors
from common.helpers import generate_file_paths, parse_document
import time
import tqdm
import numpy as np


def train_word2vec_model_from_collection(collection_directory: str) -> Word2Vec:

    """Train a word2vec model on the given collection"""

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


def restrict_w2v(w2v, restricted_word_set):
    
    """Restrict a word2vec model to the restricted_word_set"""
    
    new_vectors = []
    new_vocab = {}
    new_index2entity = []

    for i in tqdm.trange(len(w2v.vocab)):
        word = w2v.index2entity[i]
        vec = w2v.vectors[i]
        vocab = w2v.vocab[word]
        if word in restricted_word_set:
            vocab.index = len(new_index2entity)
            new_index2entity.append(word)
            new_vocab[word] = vocab
            new_vectors.append(vec)

    w2v.vocab = new_vocab
    w2v.vectors = np.array(new_vectors)
    w2v.index2entity = new_index2entity
    w2v.index2word = new_index2entity


def clip_google_word2vec_model(collection_directory: str, path_to_google_model: str) -> Word2Vec:

    """Clip the Google word2vec model (far too heavy) so it fits just our collection"""

    file_paths = generate_file_paths(collection_directory)
    vocabulary = set()
    for (absolute_path, relative_path) in tqdm.tqdm(file_paths):
        parsed_document = parse_document(absolute_path)
        for word in parsed_document:
            if not(word in vocabulary):
                vocabulary.add(word)

    model = KeyedVectors.load_word2vec_format(path_to_google_model, binary=True)
    restrict_w2v(model, vocabulary)
    model.init_sims()
    return model


def save_word2vec_model(model: Word2Vec, absolute_path: str) -> None:

    """Save the vectors of a word2vec model (take twice less space than the entire model)"""

    model.wv.save(absolute_path)


if __name__ == '__main__':
    collection_directory = '../Data'
    path_to_google_model = 'GoogleNews-vectors-negative300.bin'
    path_to_model = 'word2vec_google.kv'
    model = clip_google_word2vec_model(collection_directory, path_to_google_model)
    #save_word2vec_model(model, path_to_model)
