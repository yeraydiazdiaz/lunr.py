[![Build Status](https://travis-ci.org/yeraydiazdiaz/lunr.py.svg?branch=master)](https://travis-ci.org/yeraydiazdiaz/lunr.py)
[![codecov](https://codecov.io/gh/yeraydiazdiaz/lunr.py/branch/master/graph/badge.svg)](https://codecov.io/gh/yeraydiazdiaz/lunr.py)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/lunr.svg)](https://pypi.org/project/lunr/)
[![PyPI](https://img.shields.io/pypi/v/lunr.svg)](https://pypi.org/project/lunr/)
[![Read the Docs](https://img.shields.io/readthedocs/lunr.svg)](http://lunr.readthedocs.io/en/latest/)
[![Downloads](http://pepy.tech/badge/lunr)](http://pepy.tech/project/lunr)

# Lunr.py

A Python implementation of [Lunr.js](https://lunrjs.com) by [Oliver Nightingale](https://github.com/olivernn).

> A bit like Solr, but much smaller and not as bright.

This Python version of Lunr.js aims to bring the simple and powerful full text search capabilities into Python guaranteeing results as close as the original implementation as possible.

- [Documentation](http://lunr.readthedocs.io/en/latest/)

## What does this even do?

Lunr is a simple full text search solution for situations where deploying a full scale solution like Elasticsearch isn't possible, viable or you're simply prototyping.

Lunr parses a set of documents and creates an inverted index for quick full text searches.

The typical use case is to integrate Lunr in a web application, an example would be the [MkDocs documentation library](http://www.mkdocs.org/). In order to do this, you'd integrate [Lunr.js](https://lunrjs.com) in the Javascript code of your application, which will need to fetch and parse a JSON of your documents and create the index at startup of your application. Depending on the size of your document set this can take some time and potentially block the browser's main thread.

Lunr.py provides a backend solution, allowing you to parse the documents ahead of time and create a Lunr.js compatible index you can pass have the browser version read, minimizing start up time of your application.

Of course you could also use Lunr.py to power full text search in desktop applications or backend services to search on your documents mimicking Elasticsearch.

## Installation

Simply `pip install lunr` for the english only, best compatibility with Lunr.js version.

An optional and experimental support for other languages via the [Natural Language Toolkit](http://www.nltk.org/) stemmers is also available via `pip install lunr[languages]`. Please refer to the [documentation page on languages](https://lunr.readthedocs.io/en/latest/languages/) for more information.


## Current state

Each version of lunr.py [targets a specific version of lunr.js](https://github.com/yeraydiazdiaz/lunr.py/blob/master/lunr/__init__.py#L12) and produces the same results as it both in Python 2.7 and 3 for [non-trivial corpus of documents](https://github.com/yeraydiazdiaz/lunr.py/blob/master/tests/acceptance_tests/fixtures/mkdocs_index.json).

Lunr.py also serializes `Index` instances respecting the [`lunr-schema`](https://github.com/olivernn/lunr-schema) which are consumable by Lunr.js and viceversa.

The API is in alpha stage and likely to change.

## Usage

You'll need a list of dicts representing the documents you want to search on. These documents must have a unique field which will serve as a reference and a series of fields you'd like to search on.

Lunr provides a convenience `lunr` function to quickly index this set of documents:

```python
>>> from lunr import lunr
>>>
>>> documents = [{
...     'id': 'a',
...     'title': 'Mr. Green kills Colonel Mustard',
...     'body': 'Mr. Green killed Colonel Mustard in the study with the candlestick.',
... }, {
...     'id': 'b',
...     'title': 'Plumb waters plant',
...     'body': 'Professor Plumb has a green plant in his study',
... }]
>>> idx = lunr(
...     ref='id', fields=('title', 'body'), documents=documents
... )
>>> idx.search('kill')
[{'ref': 'a', 'score': 0.6931722372559913, 'match_data': <MatchData "kill">}]
>>> idx.search('study')
[{'ref': 'b', 'score': 0.23576799568081389, 'match_data': <MatchData "studi">}, {'ref': 'a', 'score': 0.2236629211724517, 'match_data': <MatchData "studi">}]
```

Please refer to the [documentation](http://lunr.readthedocs.io/en/latest/) for more usage examples.
