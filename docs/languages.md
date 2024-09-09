# Language support

Lunr includes optional and experimental support for languages other than English via the [Natural Language Toolkit](http://www.nltk.org/). To install Lunr with this feature use `pip install lunr[languages]`.

The currently supported languages are:

- Arabic
- Danish
- Dutch
- English
- Finnish
- French
- German
- Hungarian
- Italian
- Norwegian
- Portuguese
- Romanian
- Russian
- Spanish
- Swedish

```python
>>> documents = [
...   {
...     "id": "a",
...     "text": (
...         "Este es un ejemplo inventado de lo que sería un documento en el "
...         "idioma que se más se habla en España."),
...     "title": "Ejemplo de documento en español"
...   },
...   {
...     "id": "b",
...     "text": (
...         "Según un estudio que me acabo de inventar porque soy un experto en"
...         "idiomas que se hablan en España."),
...     "title": "Español es el tercer idioma más hablado del mundo"
...   },
... ]
```

> New in 0.5.1: the `lunr` function now accepts more than one language

Simply define specify one or more [ISO-639-1 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) for the language(s) of your documents in the `languages` parameter to the `lunr` function.

!!! Note
    In versions of Lunr prior to 0.5.0 the parameter's name is `language` and accepted a single string.

If you have a single language you can pass the language code in `languages`:

```python
>>> from lunr import lunr
>>> idx = lunr('id', ['title', 'text'], documents, languages='es')
>>> idx.search('inventando')
[{'ref': 'a', 'score': 0.130, 'match_data': <MatchData "invent">},
{'ref': 'b', 'score': 0.089, 'match_data': <MatchData "invent">}]
```

!!! Note
    In order to construct stemmers, trimmers and stop word filters Lunr imports corpus data from NLTK which fetches data from Github and caches it in your home directory under `nltk_data` by default. You may see some logging indicating such activity during the creation of the index.

If you have documents in multiple language pass a list of language codes:

```python
>>> documents.append({
     "id": "c",
     "text": "Let's say you also have documents written in English",
     "title": "A document in English"
 })
>>> idx = lunr('id', ['title', 'text'], documents, languages=['es', 'en'])
>>> idx.search('english')
[{'ref': 'c', 'score': 1.106, 'match_data': <MatchData "english">}]
```

## Folding to ASCII

It is often useful to allow for transliterated or unaccented
characters when indexing and searching.  This is not implemented in
the language support but can be done by adding a pipeline stage which
"folds" the tokens to ASCII.  There are
[various](https://pypi.org/project/text-unidecode/)
[libraries](https://pypi.org/project/Unidecode/) to do this in Python
as well as in [JavaScript](https://www.npmjs.com/package/unidecode).

On the Python side, for example, to fold accents in French text using
`text-unidecode` or `unidecode` (depending on your licensing
preferences):

```python
import json
from lunr import lunr, get_default_builder
from lunr.pipeline import Pipeline
from text_unidecode import unidecode

def unifold(token, _idx=None, _tokens=None):
    def wrap_unidecode(text, _metadata):
        return unidecode(text)
    return token.update(wrap_unidecode)

Pipeline.register_function(unifold, "unifold")
builder = get_default_builder("fr")
builder.pipeline.add(unifold)
builder.search_pipeline.add(unifold)
index = lunr(
    ref="id",
    fields=["titre", "texte"],
    documents=[
        {"id": "1314-2023-DEM", "titre": "Règlement de démolition", "texte": "Texte"}
    ],
    languages="fr",
    builder=builder,
)
print(index.search("reglement de demolition"))
# [{'ref': '1314-2023-DEM', 'score': 0.4072935059634513, 'match_data': <MatchData "demolit,regl">}]
print(index.search("règlement de démolition"))
# [{'ref': '1314-2023-DEM', 'score': 0.4072935059634513, 'match_data': <MatchData "demolit,regl">}]
with open("index.json", "wt") as outfh:
    json.dump(index.serialize(), outfh)
```

Note that it is important to do folding on both the indexing and
search pipelines to ensure that users who have the right keyboard and
can remember which accents go where will still get the expected
results.

On the JavaScript side [the
API](https://lunrjs.com/docs/lunr.Pipeline.html) is of course quite
similar:

```js
const lunr = require("lunr");
const fs = require("fs");
const unidecode = require("unidecode");
require("lunr-languages/lunr.stemmer.support.js")(lunr);
require("lunr-languages/lunr.fr.js")(lunr);

lunr.Pipeline.registerFunction(token => token.update(unidecode), "unifold")
const index = lunr.Index.load(JSON.parse(fs.readFileSync("index.json", "utf8")));
console.log(JSON.stringify(index.search("reglement de demolition")));
# [{"ref":"1314-2023-DEM","score":0.4072935059634513,"matchData":{"metadata":{"regl":{"titre":{}},"demolit":{"titre":{}}}}}]
console.log(JSON.stringify(index.search("règlement de démolition")));
# [{"ref":"1314-2023-DEM","score":0.4072935059634513,"matchData":{"metadata":{"regl":{"titre":{}},"demolit":{"titre":{}}}}}]
```

There is also
[lunr-folding](https://www.npmjs.com/package/lunr-folding) for
JavaScript, but its folding is not the same as `unidecode` and it may
not be fully compatible with language support, so it is recommended to
use the above method.

## Notes on language support

- Using multiple languages means the terms will be stemmed once per language. This can yield unexpected results.
- Compatibility with Lunr.js is ensured for languages that supported by both platforms, however results might differ slightly.
    + Languages supported by Lunr.js but not by Lunr.py:
        * Thai
        * Japanese
        * Turkish
    + Languages supported by Lunr.py but not Lunr.js:
        * Arabic
- The usage of the language feature is subject to [NTLK corpus licensing clauses](https://github.com/nltk/nltk#redistributing)
