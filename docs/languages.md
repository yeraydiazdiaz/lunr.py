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
