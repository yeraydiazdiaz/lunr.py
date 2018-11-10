import pytest

from lunr.query import Query, QueryPresence
from lunr.token import Token
from lunr.tokenizer import Tokenizer


class BaseQuerySuite:
    ALL_FIELDS = ["title", "body"]

    def setup_method(self, method):
        self.query = Query(self.ALL_FIELDS)


class TestQueryTerm(BaseQuerySuite):
    def test_single_string_term_adds_single_clause(self):
        self.query.clause(term="foo")

        assert len(self.query.clauses) == 1
        assert self.query.clauses[0].term == "foo"
        assert repr(self.query) == '<Query fields="title,body" clauses="foo">'
        assert repr(self.query.clauses[0]) == '<Clause term="foo">'

    def test_single_token_term_adds_single_clause(self):
        self.query.term(Token("foo"))

        assert len(self.query.clauses) == 1
        assert self.query.clauses[0].term == "foo"

    def test_multiple_string_terms_adds_multiple_clauses(self):
        self.query.term(["foo", "bar"])

        assert len(self.query.clauses) == 2
        assert self.query.clauses[0].term == "foo"
        assert self.query.clauses[1].term == "bar"
        assert repr(self.query) == ('<Query fields="title,body" clauses="foo,bar">')

    def test_multiple_token_terms_adds_multiple_clauses(self):
        self.query.term(Tokenizer("foo bar"))

        assert len(self.query.clauses) == 2
        assert self.query.clauses[0].term == "foo"
        assert self.query.clauses[1].term == "bar"

    def test_multiple_string_terms_with_options(self):
        self.query.term(["foo", "bar"], use_pipeline=False)

        assert len(self.query.clauses) == 2
        assert self.query.clauses[0].term == "foo"
        assert self.query.clauses[1].term == "bar"


class TestQueryClause(BaseQuerySuite):
    def test_clause_defaults(self):
        self.query.clause(term="foo")
        self.clause = self.query.clauses[0]

        assert self.clause.fields == self.ALL_FIELDS
        assert self.clause.boost == 1
        assert self.clause.use_pipeline is True

    def test_clause_specified(self):
        self.query.clause(term="foo", boost=10, fields=["title"], use_pipeline=False)
        self.clause = self.query.clauses[0]

        assert self.clause.fields == ["title"]
        assert self.clause.boost == 10
        assert self.clause.use_pipeline is False

    @pytest.mark.parametrize(
        "wildcard, expected_term",
        [
            (Query.WILDCARD_NONE, "foo"),
            (Query.WILDCARD_LEADING, "*foo"),
            (Query.WILDCARD_TRAILING, "foo*"),
            (Query.WILDCARD_LEADING | Query.WILDCARD_TRAILING, "*foo*"),
        ],
    )
    def test_clause_wildcard(self, wildcard, expected_term):
        self.query.clause(term="foo", wildcard=wildcard)
        self.clause = self.query.clauses[0]

        assert self.clause.term == expected_term

    def test_clause_wildcard_existing(self):
        self.query.clause(
            term="*foo*", wildcard=Query.WILDCARD_LEADING | Query.WILDCARD_TRAILING
        )
        self.clause = self.query.clauses[0]

        assert self.clause.term == "*foo*"


class TestQueryIsNegated(BaseQuerySuite):
    def test_all_prohibited(self):
        self.query.term("foo", presence=QueryPresence.PROHIBITED)
        self.query.term("bar", presence=QueryPresence.PROHIBITED)

        assert self.query.is_negated() is True

    def test_some_prohibited(self):
        self.query.term("foo", presence=QueryPresence.PROHIBITED)
        self.query.term("bar", presence=QueryPresence.REQUIRED)

        assert self.query.is_negated() is False

    def test_nome_prohibited(self):
        self.query.term("foo", presence=QueryPresence.OPTIONAL)
        self.query.term("bar", presence=QueryPresence.REQUIRED)

        assert self.query.is_negated() is False
