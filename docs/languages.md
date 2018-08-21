# Language support

An optional and experimental support for other languages via the [Natural Language Toolkit](http://www.nltk.org/) stemmers. To install Lunr with this feature use `pip install lunr[languages]`.

Assuming you have a set of documents in one of the supported languages:

- arabic
- danish
- dutch
- english
- finnish
- french
- german
- hungarian
- italian
- norwegian
- portuguese
- romanian
- russian
- spanish
- swedish

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

> New in 0.5.0: `lunr` now accepts more than one language

Simply define specify one or more [ISO-639-1 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) for the language(s) of you documents in the `languages` parameter to the `lunr` function.

!!! Note
    In previous versions of Lunr the parameter's name is `language` and accepted a single string.

You may pass a single string to `languages`:

```python
>>> from lunr import lunr
>>> idx = lunr('id', ['title', 'text'], documents, languages='es')
>>> idx.search('inventando')
[{'ref': 'a', 'score': 0.130, 'match_data': <MatchData "invent">},
{'ref': 'b', 'score': 0.089, 'match_data': <MatchData "invent">}]
```

!!! Note
    In order to construct stemmers, trimmers and stop word filters Lunr imports corpus data from NLTK which fetches it from Github and caches it in your home directory under `nltk_data` by default. You may see some logging indicating such activity during the creation of the index.

Or a list of languages:

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

## Notes on language support

- Please note that using multiple languages means the terms will be stemmed twice according to the definitions on each language. This can yield unexpected results.
- Compatibility with Lunr.js is ensured for languages that supported by both platforms, however results might differ slightly.
    + Languages not supported by NLTK but by lunr.js:
        * Thai
        * Japanese
        * Turkish
    + Languages upported by NLTK but not lunr.js:
        * Arabic
