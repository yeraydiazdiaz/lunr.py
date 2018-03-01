[![Build Status](https://travis-ci.org/yeraydiazdiaz/lunr.py.svg?branch=master)](https://travis-ci.org/yeraydiazdiaz/lunr.py)
[![codecov](https://codecov.io/gh/yeraydiazdiaz/lunr.py/branch/master/graph/badge.svg)](https://codecov.io/gh/yeraydiazdiaz/lunr.py)

# Lunr.py

A Python implementation of [Lunr.js](https://lunrjs.com) by [Oliver Nightingale](https://github.com/olivernn).

> A bit like Solr, but much smaller and not as bright.

This Python version of Lunr.js aims to bring the simple and powerful full text search capabilities into Python guaranteeing results as close as the original implementation as possible.

## Current state:

Lunr.py produces the same results as Lunr.js both in Python 2.7 and 3 for [non-trivial corpus of documents](https://github.com/yeraydiazdiaz/lunr.py/blob/master/tests/acceptance_tests/fixtures/search_index.json).

The API is in alpha stage and likely to change.

## Usage:

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