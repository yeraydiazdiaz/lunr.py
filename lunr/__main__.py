"""
Lunr.js boilerplate is quite unpythonic

"""

from .builder import Builder


def lunr(ref, fields, documents):
    """A convenience function to configure and construct a lunr.Index."""
    # TODO: JS version adds a pipeline with trimmer, stopWordFilter and stemmer
    # and a search_pipeline with a stemmer, maybe pass them in the constructor?
    builder = Builder()

    builder.ref(ref)
    for field in fields:
        builder.field(field)

    for document in documents:
        builder.add(document)

    return builder.build()
