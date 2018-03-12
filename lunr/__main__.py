from __future__ import unicode_literals

from lunr.builder import Builder
from lunr.trimmer import trimmer
from lunr.stop_word_filter import stop_word_filter
from lunr.stemmer import stemmer


def lunr(ref, fields, documents):
    """A convenience function to configure and construct a lunr.Index.

    Args:
        ref (str): The key in the documents to be used a the reference.
        fields (list): A list of keys in the documents to index.
        documents (list): The list of dictonaries to index.

    Returns:
        Index: The populated Index ready to search against.
    """
    builder = Builder()
    builder.pipeline.add(trimmer, stop_word_filter, stemmer)
    builder.search_pipeline.add(stemmer)

    builder.ref(ref)
    for field in fields:
        builder.field(field)

    for document in documents:
        builder.add(document)

    return builder.build()
