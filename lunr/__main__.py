from __future__ import unicode_literals

from lunr.builder import Builder
from lunr.trimmer import trimmer
from lunr.stop_word_filter import stop_word_filter
from lunr.stemmer import stemmer


def lunr(ref, fields, documents):
    """A convenience function to configure and construct a lunr.Index."""
    builder = Builder()
    builder.pipeline.add(trimmer, stop_word_filter, stemmer)
    builder.search_pipeline.add(stemmer)

    builder.ref(ref)
    for field in fields:
        builder.field(field)

    for document in documents:
        builder.add(document)

    return builder.build()
