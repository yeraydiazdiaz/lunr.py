"""
lunr.Builder

"""

from .pipeline import Pipeline


class Builder:
    """Performs indexing on a set of documents and
    returns instances of lunr.Index ready for querying.

    """

    def __init__(self, *args, **kwargs):
        self.pipeline = Pipeline()
        self.search_pipeline = Pipeline()
