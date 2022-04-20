# Interoperability with Lunr.js

A key goal of Lunr.py is interoperability with Lunr.js: building an index with
Lunr.py and being able to read it using Lunr.js without having to build it
on the client on each visit.

The key step in this process is index serialization, which is possible thanks
to [`lunr-schema`](https://github.com/olivernn/lunr-schema).

The serialization process in Lunr.py consist on calling `Index.serialize`,
here is a complete example with the data from the [introduction](index.md):

```python
>>> import json
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
>>> serialized_idx = idx.serialize()
>>> with open('idx.json', 'w') as fd:
...:    json.dump(serialized_idx, fd)
```

As you can see `serialize` will produce a JSON friendly dict you can write to
disk and read from Lunr.js. The following snippet shows how to read the index
using Node.js:

```javascript
> const fs = require('fs')
> const lunr = require('lunr')
> const serializedIndex = JSON.parse(fs.readFileSync('idx.json'))
> let idx = lunr.Index.load(serializedIndex)
> idx.search('plant')
[
  {
    ref: 'b',
    score: 1.599,
    matchData: { metadata: [Object: null prototype] }
  },
  {
    ref: 'c',
    score: 0.13,
    matchData: { metadata: [Object: null prototype] }
  }
]
```

!!! Note
    The search will only the _references_ of the matching documents.
    It is up to you to keep mapping of the documents in memory to be able show richer
    results which means in a web environment you will need to serve _two_ files,
    one for the index and another the collection of documents.

## Loading a serialized index

You can also do the reverse operation of reading a serialized index produced
by Lunr.py or Lunr.js using the `Index.load` class method:

```python
>>> import json
>>> from lunr.index import Index
>>> with open("idx.json") as fd:
...     serialized_idx = json.loads(fd.read())
...
>>> idx = Index.load(serialized_idx)
>>> idx.search("plant")
[{'ref': 'b', 'score': 1.599, 'match_data': <MatchData "plant">}, {'ref': 'c', 'score': 0.13, 'match_data': <MatchData "plant">}]
```

## Language support

Lunr.js uses the
[`lunr-languages`](https://lunrjs.com/guides/language_support.html) package,
a community driven collection of stemmers and trimmers for many languages.

Porting each of those into Python was not feasible so Lunr.py uses [NTLK](https://www.nltk.org/)
for language support and will configure the serialized index as expected by Lunr.js
to ensure compatibility.

However, this produces differences in scoring when loading indices from Lunr.py
into Lunr.js larger than those observed using the base english implementation,
due to inherent differences in the implementation of said stemmers and trimmers.
