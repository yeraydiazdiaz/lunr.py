from __future__ import unicode_literals

from itertools import chain

from past.builtins import basestring

from lunr.builder import Builder
from lunr.trimmer import trimmer, generate_trimmer
from lunr.stop_word_filter import stop_word_filter, generate_stop_word_filter
from lunr.stemmer import stemmer
from lunr.stemmer_languages import LANGUAGE_SUPPORT, SUPPORTED_LANGUAGES
from lunr.pipeline import Pipeline


def _get_stopwords_and_word_characters(language):
    # TODO: add the stopword filter using stopwords for languages
    # Move to languages module?
    import nltk
    nltk.download('stopwords')

    verbose_language = SUPPORTED_LANGUAGES[language]
    stopwords = nltk.corpus.stopwords.words(verbose_language)
    # TODO: search for a more exhaustive list of word characters
    word_characters = {c for word in stopwords for c in word}

    return stopwords, word_characters


def _get_nltk_builder(languages):
    """Returns a builder with stemmers for all languages added to it.

    Args:
        languages (list): A list of supported languages.
    """
    stemmers = []
    stopwords_filters = []
    word_characters = {}

    for language in languages:
        if language == 'en':
            # use Lunr's defaults
            stemmers.append(stemmer)
            stopwords_filters.append(stop_word_filter)
            word_characters.update({'\W'})
        else:
            stopwords, word_characters = (
                _get_stopwords_and_word_characters(language))
            stemmers.append(
                Pipeline.registered_functions['stemmer-{}'.format(language)])
            stopwords_filters.append(generate_stop_word_filter(stopwords))
            word_characters.update(word_characters)

    builder = Builder()
    multi_trimmer = generate_trimmer(''.join(sorted(word_characters)))
    Pipeline.register_function(
        multi_trimmer, 'lunr-multi-trimmer-{}'.format('-'.join(languages)))
    builder.pipeline.reset()

    for fn in chain([multi_trimmer], stopwords_filters, stemmers):
        builder.pipeline.add(fn)
    for fn in stemmers:
        builder.search_pipeline.add(fn)

    return builder


def lunr(ref, fields, documents, languages=None):
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
        languages (str or list, optional): The languages to use if using
            NLTK language support, ignored if NLTK is not available.

    Returns:
        Index: The populated Index ready to search against.
    """
    if languages is not None and LANGUAGE_SUPPORT:
        if isinstance(languages, basestring):
            languages = [languages]

        unsupported_languages = set(languages) - set(SUPPORTED_LANGUAGES)
        if unsupported_languages:
            raise RuntimeError(
                'The specified languages {} are not supported, '
                'please choose one of {}'.format(
                    ', '.join(unsupported_languages),
                    ', '.join(SUPPORTED_LANGUAGES.keys())))
        builder = _get_nltk_builder(languages)
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
