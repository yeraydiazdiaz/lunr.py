from lunr.field_ref import FieldRef
from lunr.match_data import MatchData
from lunr.vector import Vector
from lunr.token_set import TokenSet
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
        # TODO: depends on QueryParser
        pass

    def query(self, query_builder):
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
        matching_fields = {}
        query_vectors = {}
        term_field_cache = {}

        # TODO: QueryBuilders construct Query objects?
        query_builder(query)

        for i, clause in enumerate(query.clauses):
            # Unless the pipeline has been disabled for this term, which is
            # the case for terms with wildcards, we need to pass the clause
            # term through the search pipeline. A pipeline returns an array
            # of processed terms. Pipeline functions may expand the passed
            # term, which means we may end up performing multiple index lookups
            # for a single query term.
            if clause.use_pipeline:
                terms = self.pipeline.run_string(clause['term'])
            else:
                terms = [clause['term']]

            for term in terms:
                # Each term returned from the pipeline needs to use the same
                # query clause object, e.g. the same boost and or edit distance
                # The simplest way to do this is to re-use the clause object
                # but mutate its term property.
                clause['term'] = term

                # From the term in the clause we create a token set which will
                # then be used to intersect the indexes token set to get a list
                # of terms to lookup in the inverted index
                term_token_set = TokenSet.from_clause(clause)
                expanded_terms = self.token_set.intersect(
                    term_token_set).to_list()

                for expanded_term in expanded_terms:
                    posting = self.inverted_index[expanded_term]
                    term_index = posting['_index']

                    for field in clause['fields']:
                        # For each field that this query term is scoped by
                        # (by default all fields are in scope) we need to get
                        # all the document refs that have this term in that
                        # field.
                        #
                        # The posting is the entry in the invertedIndex for the
                        # matching term from above.
                        field_posting = posting[field]
                        matching_document_refs = field_posting.keys()
                        term_field = expanded_term + '/' + field

                        # To support field level boosts a query vector is
                        # created per field. This vector is populated using the
                        # termIndex found for the term and a unit value with
                        # the appropriate boost applied.
                        #
                        # If the query vector for this field does not exist yet
                        # it needs to be created.
                        if field not in query_vectors:
                            query_vectors[field] = Vector()

                        # Using upsert because there could already be an entry
                        # in the vector for the term we are working with.
                        # In that case we just add the scores together.
                        query_vectors[field].upsert(
                            term_index,
                            1 * clause['boost'],
                            lambda a, b: a + b
                        )

                        # If we've already seen this term, field combo then
                        # we've already collected the matching documents and
                        # metadata, no need to go through all that again
                        if term_field_cache[term_field]:
                            continue

                        for matching_document_ref in matching_document_refs:
                            # All metadata for this term/field/document triple
                            # are then extracted and collected into an instance
                            # of lunr.MatchData ready to be returned in the
                            # query results
                            matching_field_ref = FieldRef(
                                matching_document_ref, field)
                            metadata = field_posting[matching_document_ref]

                            try:
                                field_match = matching_fields[
                                    matching_field_ref]
                            except KeyError:
                                field_match = MatchData(
                                    expanded_term, field, metadata)
                                matching_fields[
                                    matching_field_ref] = field_match

                        term_field_cache[term_field] = True

        matching_field_refs = matching_fields.keys()
        results = []
        matches = {}

        for matching_field_ref in matching_field_refs:
            # Currently we have document fields that match the query, but we
            # need to return documents. The matchData and scores are combined
            # from multiple fields belonging to the same document.
            #
            # Scores are calculated by field, using the query vectors created
            # above, and combined into a final document score using addition.
            field_ref = FieldRef.from_string(matching_document_ref)
            doc_ref = field_ref.doc_ref
            field_vector = self.field_vectors[field_ref]
            score = query_vectors[field_ref.field_name].similarity(
                field_vector)

            try:
                doc_match = matches[doc_ref]
                doc_match += score
                doc_match.match_data.combine(matching_fields[field_ref])
            except KeyError:
                match = {
                    'ref': doc_ref,
                    'score': score,
                    'match_data': matching_fields[field_ref]
                }
                matches[doc_ref] = match
                results.push(match)

        return sorted(results, key=lambda a, b: b.score - a.score)
