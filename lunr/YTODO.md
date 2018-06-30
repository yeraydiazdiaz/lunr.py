# Lunr.py

## Overview notes

- FieldRefs are combinations of document reference and field names `title/id`
- Builder:
    + `field_lengths`: `FieldRef -> number of terms`. The number of tokens for a field in a doc.
    + `field_term_frequencies`: FieldRef -> { term:  }
    + `inverted_index`: `Token -> { field_name -> { doc -> metadata } }`. Maps tokens with data per field to each doc, optionally with metadata if the token includes it.

## Non-code

- Star Wars themed examples/docs

## Releasing

- `rm -fr dist/`
- `python setup.py sdist`
- `python setup.py bdist_wheel --universal`
- https://test.pypi.org/project/lunr:
    + `twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
- https://pypi.org/project/lunr
    + `twine upload dist/*`
- Test:
    + `cd`
    + `mkdir tmp`
    + `virtualenv .env`
    + `pip install lunr` (check version)

## Language support

Lunr.js uses a separate packages with stemmer, stopword and trimmer functions that are added to the pipeline via a `this.use(lunr.es)` call in the main `lunr` function callback.

```javascript
var lunr = require("lunr")
require("lunr-languages/lunr.stemmer.support")(lunr)
require("lunr-languages/lunr.fr")(lunr)
var idx = lunr(function () {
  this.use(lunr.fr)
  this.ref('id')
  this.field('text')

  this.add({
    id: 1,
    text: "Ceci n'est pas une pipe"
  })
})
```

Multilanguage is possible using `lunr.multi` and `this.use(lunr.multiLanguage('en', 'es')`.

```javascript
var lunr = require("lunr")
require("lunr-languages/lunr.stemmer.support")(lunr)
require('lunr-languages/lunr.multi')(lunr)
require("lunr-languages/lunr.de")(lunr)

var idx = lunr(function () {
  this.use(lunr.multiLanguage('en', 'de'))
})
```

NLTK has stemmers for many languages, they seem to include stopwords and possibly trimmers? http://www.nltk.org/howto/stem.html


### lunr 2.3.0

- language support results differ from JS
    + the first entry is correct and the score is roughly right
    + the rest of the entries are in the wrong order, opened an issue since the top entry in 2.2.1 is now last
    + specifically the entry with "imperio" on the title and twice on the body scores almost as much as the ones with the term only in the body once
    + `lunr-languages` takes other stemming, trimming and stop-words libraries and adapts it for Lunr.
        * `lunr.<lang>.stemmer` includes the stemmer for the language
    + after tracing both versions seems changes on `Vector.similarity` that stopped taking the magnitude of the other vector into account create all the difference. Seems v2.3.0 yields more meaningful results, I simply changed the query in the acceptance tests