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
Use `python` or `python3` depending on your python setup.
The following will display all possible options, add `-h` to get a more detailed help.

```shell
python main.py
```

With default options (vectorial model with pre calculated weighting scheme docs and query) you can run a query like follows

```shell
python main.py -q "how to replace google"
```

or if using a file, with the `--is-file-path` option.
```shell
python main.py -q path/to/file/with/query --is-file-path
```
You can change the model used to run the query with the `-e` flag.
```shell
python main.py -q 'how to replace google' -e bool
```
Also you can limit the number of results displayed. Default is 20
```shell
python main.py -q "how to replace google" -l 10
```
Learn more about the options ith `python main.py -h`

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
