# Lunr.py 🌖

A Python implementation of [Lunr.js](https://lunrjs.com) by [Oliver Nightingale](https://github.com/olivernn).

> A bit like Solr, but much smaller and not as bright.

This Python version of Lunr.js aims to bring the simple and powerful full text search capabilities into Python guaranteeing results as close as the original implementation as possible.

## What does this even do?

Lunr is a simple full text search solution for situations where deploying a full scale solution like Elasticsearch isn't possible, viable or you're simply prototyping.

Lunr parses a set of documents and creates an inverted index for quick full text searches.

The typical use case is to integrate Lunr in a web application, an example would be the [MkDocs documentation library](http://www.mkdocs.org/). In order to do this, you'd integrate [Lunr.js](https://lunrjs.com) in the Javascript code of your application, which will need to fetch and parse a JSON of your documents and create the index at startup of your application. Depending on the size of your document set this can take some time and potentially block the browser's main thread.

Lunr.py provides a backend solution, allowing you to parse the documents ahead of time and create a Lunr.js compatible index you can pass have the browser version read, minimizing start up time of your application.

Of course you could also use Lunr.py to power full text search in desktop applications or backend services to search on your documents mimicking Elasticsearch.

## Current state

Each version of lunr.py [targets a specific version of lunr.js](https://github.com/yeraydiazdiaz/lunr.py/blob/master/lunr/__init__.py#L12) and produces the same results as it both in Python 2.7 and 3 for [non-trivial corpus of documents](https://github.com/yeraydiazdiaz/lunr.py/blob/master/tests/acceptance_tests/fixtures/mkdocs_index.json).

Lunr.py also serializes `Index` instances respecting the [`lunr-schema`](https://github.com/olivernn/lunr-schema) which are consumable by Lunr.js and viceversa.

The API is in alpha stage and likely to change.
