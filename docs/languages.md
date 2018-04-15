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

Simply define specify the [ISO-639-1 code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) for the language of you documents as a parameter to the `lunr` function:

```python
>>> from lunr import lunr
>>> idx = lunr('id', ['title', 'text'], documents, language='es')
>>> idx.search('inventando')
[{'ref': 'a', 'score': 0.1300928764641503, 'match_data': <MatchData "invent">},
{'ref': 'b', 'score': 0.08967151299297255, 'match_data': <MatchData "invent">}]
```

Please note compatibility with Lunr.js might be affected when using this feature.