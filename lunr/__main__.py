from __future__ import unicode_literals

from functools import partial

from lunr.builder import Builder
from lunr.trimmer import trimmer
from lunr.stop_word_filter import stop_word_filter
from lunr.stemmer import stemmer
from lunr.stemmer_languages import (
    LANGUAGE_SUPPORT, SUPPORTED_LANGUAGES, get_language_stemmer, nltk_stemmer)
from lunr.pipeline import Pipeline


def _get_nltk_builder(language):
    language_stemmer = partial(nltk_stemmer, get_language_stemmer(language))
    Pipeline.register_function(
        language_stemmer, 'stemmer_{}'.format(language))

    builder = Builder()
    builder.pipeline.add(trimmer, language_stemmer)
    builder.search_pipeline.add(language_stemmer)

    return builder


def lunr(ref, fields, documents, language=None):
    """A convenience function to configure and construct a lunr.Index.

    Args:
        ref (str): The key in the documents to be used a the reference.
        fields (list): A list of keys in the documents to index.
        documents (list): The list of dictonaries to index.
        language (str, optional): The language to use if using NLTK language
            support, ignored if NLTK is not available.

    Returns:
        Index: The populated Index ready to search against.
    """
    if language and LANGUAGE_SUPPORT:
        if language not in SUPPORTED_LANGUAGES:
            raise RuntimeError(
                '"{}" is not a supported language, '
                'please choose one of {}'.format(
                    language, ', '.join(SUPPORTED_LANGUAGES.keys())))
        builder = _get_nltk_builder(language)
    else:
        builder = Builder()
        builder.pipeline.add(trimmer, stop_word_filter, stemmer)
        builder.search_pipeline.add(stemmer)

    builder.ref(ref)
    for field in fields:
        builder.field(field)

    for document in documents:
        builder.add(document)

    return builder.build()
