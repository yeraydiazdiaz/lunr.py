from __future__ import unicode_literals

from lunr.builder import Builder
from lunr.trimmer import trimmer
from lunr.stop_word_filter import stop_word_filter
from lunr.stemmer import stemmer
from lunr.stemmer_languages import LANGUAGE_SUPPORT, SUPPORTED_LANGUAGES
from lunr.pipeline import Pipeline


def _get_nltk_builder(language):
    language_stemmer = Pipeline.registered_functions[
        'stemmer-{}'.format(language)]

    builder = Builder()
    builder.pipeline.add(trimmer, language_stemmer)
    builder.search_pipeline.add(language_stemmer)

    return builder


def lunr(ref, fields, documents, language=None):
    """A convenience function to configure and construct a lunr.Index.

    Args:
        ref (str): The key in the documents to be used a the reference.
        fields (list): A list of strings defining fields in the documents to
            index. Optionally a list of dictionaries with three keys:
            `field_name` defining the document's field, `boost` an integer
            defining a boost to be applied to the field, and `extractor`
            a callable taking the document as a single argument and returning
            a string located in the document in a particular way.
        documents (list): The list of dictonaries representing the documents
            to index. Optionally a 2-tuple of dicts, the first one being
            the document and the second the associated attributes to it.
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
        if isinstance(field, dict):
            builder.field(**field)
        else:
            builder.field(field)

    for document in documents:
        if isinstance(document, (tuple, list)):
            builder.add(document[0], attributes=document[1])
        else:
            builder.add(document)

    return builder.build()
