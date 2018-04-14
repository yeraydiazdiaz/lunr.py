from __future__ import unicode_literals

import pytest

from lunr import lunr
from lunr.stemmer_languages import LANGUAGE_SUPPORT
from lunr.pipeline import Pipeline

documents = [
  {
    "id": "a",
    "text": (
        "Este es un ejemplo inventado de lo que sería un documento en el "
        "idioma que se más se habla en España."),
    "title": "Ejemplo de documento en español"
  },
  {
    "id": "b",
    "text": (
        "Según un estudio que me acabo de inventar porque soy un experto en"
        "idiomas que se hablan en España."),
    "title": "Español es el tercer idioma más hablado del mundo"
  },
]


def test_lunr_function_raises_if_unsupported_language():
    with pytest.raises(RuntimeError):
        lunr('id', ['title', 'text'], documents, 'foo')


def test_lunr_function_registers_nltk_stemmer():
    assert LANGUAGE_SUPPORT is True
    lunr('id', ['title', 'text'], documents, 'en')
    assert 'stemmer_en' in Pipeline.registered_functions


def test_search_stems_search_terms():
    idx = lunr('id', ['title', 'text'], documents, 'es')
    results = idx.search('inventando')  # stemmed to "invent"
    assert len(results) == 2
