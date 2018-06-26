# Building indices

We briefly skimmed over creating indices in Lunr in the [searching](./usage.md) section, let's go into more detail around what we need to build a Lunr index.

## The `lunr` function

The main entry point to Lunr is the `lunr` function. It provides a simple way to create an index, define fields we're interested in and start indexing a corpus of documents.

We do that simply by providing:

- A `ref` string specifying the field in the documents that should be used as a key for each document.
- A `fields` list, which defines the fields in the documents that should be added to the index.
- A `documents` list, including a set of dictionaries representing the documents we want to index.

And that's it. The `lunr` function will create an index, configure it, add the documents and return the `lunr.Index` for you to start searching.

## Build time boosts

> New in version 0.4.0

Lunr also provides some very useful functionality for boosting at index building time. There are two types of boosts you can include: field boosts and document boosts.

### Field boosts

Field boosts let Lunr know that, when searching, we care more about some fields than others, a typical example is adding a boost on the *title* of our documents so when searching for a term, if it is found in the title, the document will score higher.

To include a field boost we use the `fields` argument of the `lunr` function, instead of passing a list of strings as usual, we pass a list of dictionaries with two keys:

- `field_name` whose value will be the name of the field in the documents we want to index.
- `boost` an integer to be multiplied to the score when a match is found on this field.

For example:

```python
>>> from lunr import lunr
>>> documents = [{
...:         'id': 'a',
...:         'title': 'Mr. Green kills Colonel Mustard',
...:         'body': """Mr. Green killed Colonel Mustard in the study with the
...: candlestick. Mr. Green is not a very nice fellow."""
...:     }, {
...:         'id': 'b',
...:         'title': 'Plumb waters plant',
...:         'body': 'Professor Plumb has a green and a yellow plant in his study',
...:     }, {
...:         'id': 'c',
...:         'title': 'Scarlett helps Professor',
...:         'body': """Miss Scarlett watered Professor Plumbs green plant
...: while he was away on his murdering holiday.""",
...:     }]
>>> idx = lunr(
...:    ref='id',
...:    fields=[dict(field_name='title', boost=10), 'body'],
...:    documents=documents
...: )
```

Note how we're passing a dictionary only for `title`, `body` will have a neutral value for `boost`.


```python
>>> idx.search('plumb')
[{'match_data': <MatchData "plumb">, 'ref': 'b', 'score': 1.599},
 {'match_data': <MatchData "plumb">, 'ref': 'c', 'score': 0.13}]
```

Note how the score for document `b` is much higher thanks to our field boost.

### Document boosts

Document boosts let Lunr know that some documents are more important than others, for example we would like an FAQ page to show up higher in searches.

In Lunr we do this via the `documents` argument to the `lunr` function, instead of passing a list of dictionaries we pass a 2-tuple (or list) with the document dictionary as a first item and another dictionary as a second item. This second dictionary must have a single `boost` key with an integer to be applied to any matches on this particular document.

```python
documents = [
    {
        'id': 'a',
        'title': 'Mr. Green kills Colonel Mustard',
        'body': """Mr. Green killed Colonel Mustard in the study with the
candlestick. Mr. Green is not a very nice fellow."""
    }, {
            'id': 'b',
            'title': 'Plumb waters plant',
            'body': 'Professor Plumb has a green and a yellow plant in his study',
    }, (
        {
            'id': 'c',
            'title': 'Scarlett helps Professor',
            'body': """Miss Scarlett watered Professor Plumbs green plant
    while he was away on his murdering holiday.""",
        }, {
            'boost': 10
        }
    )]
```

Note how the third member of a list is a tuple, now if we pass these documents to the `lunr` function and perform a search:

```python
>>> idx = lunr(ref='id', fields=('title', 'body'), documents=documents)
>>> idx.search('plumb')
[{'match_data': <MatchData "plumb">, 'ref': 'c', 'score': 1.297},
 {'match_data': <MatchData "plumb">, 'ref': 'b', 'score': 0.3}]
```

The score for `c` is now higher than `b` even though there are less matches, thanks to our document boost.

## Field extractors

Up until now we've been working with fairly simple documents, but what if you have large nested documents and only want to index parts of them?

For this Lunr provides *field extractors*, which are simply callables that Lunr can use to fetch the field in the document you want to index. If you do not provide it, as we've been doing, Lunr assumes there's a key matching the field name, i.e. `title` or `body`.

To pass a field extractor to Lunr we, once again, use the `fields` argument to the `lunr` function. Similarly to what we did to define field boosts we pass a list of dictionaries, but this time we add an `extractor` key whose value is a  callable with a single argument, the document being processed. Lunr will call the extractor when fetching the indexed field and will use its result in our index.

Imagine our documents have a slightly different form where the reference is at the top level but our fields are nested under a `content` key:

```python
documents = [{
    'id': 'a',
    'content': {
        'title': 'Mr. Green kills Colonel Mustard',
        'body': """Mr. Green killed Colonel Mustard in the study with the
candlestick. Mr. Green is not a very nice fellow."""
    }
}, {
    'id': 'b',
    'content': {
        'title': 'Plumb waters plant',
        'body': 'Professor Plumb has a green and a yellow plant in his study',
    }
}, {
    'id': 'c',
    'content': {
        'title': 'Scarlett helps Professor',
        'body': """Miss Scarlett watered Professor Plumbs green plant
    while he was away on his murdering holiday.""",
    }
}]
```

To work around this we simply need to add field extractors, which are simply callables that take a document as an argument and return the content of the field, in this case a simple `lambda` will do:

```python
>>> idx = lunr(
...     ref='id',
...     fields=[
...         dict(field_name='title', extractor=lambda d: d['content']['title']),
...         dict(field_name='body', extractor=lambda d: d['content']['body'])
...     ],
...     documents=documents)
```

We can now search the index as usual:

```python
>>> idx.search('plumb')
[{'ref': 'b', 'score': 0.3, 'match_data': <MatchData "plumb">}
 {'ref': 'c', 'score': 0.13, 'match_data': <MatchData "plumb">}]
```
