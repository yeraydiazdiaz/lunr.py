from __future__ import unicode_literals


class Clause(dict):
    """A single clause in a `lunr.Query` contains a term and details on
    how to match that term against a `lunr.Index`.

    TODO: use an actual class
    """
    def __init__(
            self, boost=1, wildcard=0):
        super(Clause, self).__init__()
        # self['fields'] = fields
        # self['edit_distance'] = edit_distance
        # self['use_pipeline'] = use_pipeline
        self['boost'] = boost
        self['wildcard'] = wildcard


class Query:
    """A `lunr.Query` provides a programmatic way of defining queries to be
    performed against a `lunr.Index`.

    Prefer constructing a `lunr.Query` using `the lunr.Index.query` method
    so the query object is pre-initialized with the right index fields.
    """

    # Constants for indicating what kind of automatic wildcard insertion will
    # be used when constructing a query clause.
    # This allows wildcards to be added to the beginning and end of a term
    # without having to manually do any string concatenation.
    # The wildcard constants can be bitwise combined to select both leading and
    # trailing wildcards.
    WILDCARD = '*'
    # TODO: enum?
    WILDCARD_NONE = 0
    WILDCARD_LEADING = 1
    WILDCARD_TRAILING = 2

    def __init__(self, all_fields):
        self.clauses = []
        self.all_fields = all_fields

    def clause(self, clause):
        """Adds a `lunr.Clause` to this query.

        Unless the clause contains the fields to be matched all fields will be
        matched. In addition a default boost of 1 is applied to the clause.
        """
        if 'fields' not in clause:
            clause['fields'] = self.all_fields

        if 'boost' not in clause:
            clause['boost'] = 1

        if 'use_pipeline' not in clause:
            clause['use_pipeline'] = True

        if 'wildcard' not in clause:
            clause['wildcard'] = self.WILDCARD_NONE

        if ((clause['wildcard'] & Query.WILDCARD_LEADING) and
                (clause['term'][0] != Query.WILDCARD)):
            clause['term'] = Query.WILDCARD + clause['term']

        if ((clause['wildcard'] & Query.WILDCARD_TRAILING) and
                (clause['term'][-1] != Query.WILDCARD)):
            clause['term'] = clause['term'] + Query.WILDCARD

        self.clauses.append(clause)
        return self

    def term(self, term, options=None):
        """Adds a term to the current query, under the covers this will create
        a `lunr.Clause` to the list of clauses that make up this query.
        """
        clause = options or {}
        clause['term'] = term
        self.clause(clause)
        return self
