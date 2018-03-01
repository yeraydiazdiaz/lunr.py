import pytest

from lunr.query import Query


class TestQueryClause:
    ALL_FIELDS = ['title', 'body']

    def setup_method(self, method):
        self.query = Query(self.ALL_FIELDS)

    def test_clause_defaults(self):
        self.query.clause(term='foo')
        self.clause = self.query.clauses[0]

        assert self.clause.fields == self.ALL_FIELDS
        assert self.clause.boost == 1
        assert self.clause.use_pipeline is True

    def test_clause_specified(self):
        self.query.clause(
            term='foo',
            boost=10,
            fields=['title'],
            use_pipeline=False
        )
        self.clause = self.query.clauses[0]

        assert self.clause.fields == ['title']
        assert self.clause.boost == 10
        assert self.clause.use_pipeline is False

    @pytest.mark.parametrize(
        'wildcard, expected_term', [
            (Query.WILDCARD_NONE, 'foo'),
            (Query.WILDCARD_LEADING, '*foo'),
            (Query.WILDCARD_TRAILING, 'foo*'),
            (Query.WILDCARD_LEADING | Query.WILDCARD_TRAILING, '*foo*'),
        ])
    def test_clause_wildcard(self, wildcard, expected_term):
        self.query.clause(term='foo', wildcard=wildcard)
        self.clause = self.query.clauses[0]

        assert self.clause.term == expected_term

    def test_clause_wildcard_existing(self):
        self.query.clause(
            term='*foo*',
            wildcard=Query.WILDCARD_LEADING | Query.WILDCARD_TRAILING
        )
        self.clause = self.query.clauses[0]

        assert self.clause.term == '*foo*'
