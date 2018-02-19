from lunr.query import Query


class Index:
    """An index contains the built index of all documents and provides a query
    interface to the index.

    Usually instances of lunr.Index will not be created using this
    constructor, instead lunr.Builder should be used to construct new
    indexes, or lunr.Index.load should be used to load previously built and
    serialized indexes.
    """

    def __init__(self, attrs):
        self.inverted_index = attrs['inverted_index']
        self.field_vectors = attrs['field_vectors']
        self.token_set = attrs['token_set']
        self.fields = attrs['fields']
        self.pipeline = attrs['pipeline']

    def search(self, query_string):
        pass

    def query(self, fn):
        """Performs a query against the index using the yielded lunr.Query
        object.

        If performing programmatic queries against the index, this method is
        preferred over `lunr.Index.search` so as to avoid the additional query
        parsing overhead.

        A query object is yielded to the supplied function which should be used
        to express the query to be run against the index.

        Note that although this function takes a callback parameter it is _not_
        an asynchronous operation, the callback is just yielded a query object
        to be customized.
        """
        # for each query clause
        # * process terms
        # * expand terms from token set
        # * find matching documents and metadata
        # * get document vectors
        # * score documents
        query = Query(self.fields)
        # matching_fields = {}
        # query_vectors = {}
        # term_field_cache = {}

        fn(query, query)
