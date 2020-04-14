# Information Retrieval Project 2020

Welcome to the repository of our Information Retrieval project !

The project was initiated as an academic project at [CentraleSupélec](https://www.centralesupelec.fr/)
during the Information Retrieval and Web Search course.

## Getting Started

### Prerequisites
Before being able to run this project, you need to fulfill the following
requirements:

* [Python 3.8](https://www.python.org/)

The project also uses the Python packages `numpy` and `gensim`.

### Use the Search Engine
You can use the Search Engine using a Command Line Interface.

The following command will display all possible options : 

```shell
python3 main.py
```

You can also add the flag `-h` to get detailed help and learn more about the options :

```shell
python3 main.py -h
```

To use the search engine with the default options (vectorial model with the Okapi BM 25 weighting scheme for the documents and a frequency weighting for the query), you can run a query like follows :

```shell
python3 main.py -q "how to replace google"
```

or if using a text file containing the query, with the `--is-file-path` option :

```shell
python3 main.py -q path/to/file/with/query --is-file-path
```

You can change the model used to run the query with the `-e` flag :

```shell
python3 main.py -q "how to replace google" -e bool
```

Also you can limit the number of results displayed with the `-l` flag (default value is 20) :

```shell
python3 main.py -q "how to replace google" -l 10
```

Finally, you could run a complex query like this (Word2Vec Model) :

```shell
python3 main.py -q "how to replace google" -l 50 -e wordtovec --w2v-model indexing/word2vec_google.kv
```
 

## The Stanford C276 collection

The collection used for this project is the public collection made available for the course
"CS 276 / LING 286: Information Retrieval and Web Search" from Stanford University.
It is a collection of web pages from the Stanford University website.
The webpages in the collection are not raw HTML : they are already tokenized, which makes it easier to work with them.

The collection can be downloaded at the following address : http://web.stanford.edu/class/cs276/pa/pa1-data.zip.

## Built With
The whole project is written in [Python 3](https://www.python.org/).

## Contributing
This project does not accept public contributions.

## Authors
* [Hackatosh](https://github.com/Hackatosh)
* [damianib](https://github.com/damianib)
* [Raklyon](https://github.com/Raklyon)

## License
This project is licensed under the MIT License—see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments
* Thanks to CentraleSupélec.
