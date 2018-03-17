[![Build Status](https://travis-ci.org/yeraydiazdiaz/lunr.py.svg?branch=master)](https://travis-ci.org/yeraydiazdiaz/lunr.py)
[![codecov](https://codecov.io/gh/yeraydiazdiaz/lunr.py/branch/master/graph/badge.svg)](https://codecov.io/gh/yeraydiazdiaz/lunr.py)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/lunr.svg)](https://pypi.org/project/lunr/)
[![PyPI](https://img.shields.io/pypi/v/lunr.svg)](https://pypi.org/project/lunr/)

# Lunr.py

A Python implementation of [Lunr.js](https://lunrjs.com) by [Oliver Nightingale](https://github.com/olivernn).

> A bit like Solr, but much smaller and not as bright.

This Python version of Lunr.js aims to bring the simple and powerful full text search capabilities into Python guaranteeing results as close as the original implementation as possible.

## Current state:

Each version of lunr.py [targets a specific version of lunr.js](https://github.com/yeraydiazdiaz/lunr.py/blob/master/lunr/__init__.py#L12) and produces the same results as it both in Python 2.7 and 3 for [non-trivial corpus of documents](https://github.com/yeraydiazdiaz/lunr.py/blob/master/tests/acceptance_tests/fixtures/search_index.json).

Lunr.py also serializes `Index` instances respecting the [`lunr-schema`](https://github.com/olivernn/lunr-schema) which are consumable by Lunr.js and viceversa.

The API is in alpha stage and likely to change.

## Usage:

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
