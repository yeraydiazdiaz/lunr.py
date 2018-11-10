import pytest

from lunr.query import Query, QueryPresence
from lunr.query_parser import QueryParser
from lunr.exceptions import QueryParseError


def parse(q):
    query = Query(["title", "body"])
    parser = QueryParser(q, query)

    parser.parse()
    return query.clauses


class TestQueryParser:
    def test_parse_empty_string(self):
        clauses = parse("")
        assert len(clauses) == 0

    def test_parse_single_term(self):
        clauses = parse("foo")
        assert len(clauses) == 1
        clause = clauses[0]
        assert clause.term == "foo"
        assert clause.fields == ["title", "body"]
        assert clause.use_pipeline is True
        assert clause.presence is QueryPresence.OPTIONAL

    def test_parse_single_term_uppercase(self):
        clauses = parse("FOO")
        assert len(clauses) == 1
        clause = clauses[0]
        assert clause.term == "foo"
        assert clause.fields == ["title", "body"]
        assert clause.use_pipeline is True

    def test_parse_single_term_with_wildcard(self):
        clauses = parse("fo*")
        assert len(clauses) == 1
        clause = clauses[0]
        assert clause.term == "fo*"
        assert clause.use_pipeline is False

    def test_multiple_terms(self):
        clauses = parse("foo bar")
        assert len(clauses) == 2
        assert clauses[0].term == "foo"
        assert clauses[1].term == "bar"

    def test_term_with_presence_required_adds_required_clause(self):
        clauses = parse("+foo")
        assert len(clauses) == 1
        assert clauses[0].term == "foo"
        assert clauses[0].boost == 1
        assert clauses[0].fields == ["title", "body"]
        assert clauses[0].presence == QueryPresence.REQUIRED

    def test_term_with_presence_required_adds_prohibited_clause(self):
        clauses = parse("-foo")
        assert len(clauses) == 1
        assert clauses[0].term == "foo"
        assert clauses[0].boost == 1
        assert clauses[0].fields == ["title", "body"]
        assert clauses[0].presence == QueryPresence.PROHIBITED

    def test_term_scoped_by_field_with_presence_required(self):
        clauses = parse("+title:foo")
        assert len(clauses) == 1
        assert clauses[0].term == "foo"
        assert clauses[0].boost == 1
        assert clauses[0].fields == ["title"]
        assert clauses[0].presence == QueryPresence.REQUIRED

    def test_term_scoped_by_field_with_presence_prohibited(self):
        clauses = parse("-title:foo")
        assert len(clauses) == 1
        assert clauses[0].term == "foo"
        assert clauses[0].boost == 1
        assert clauses[0].fields == ["title"]
        assert clauses[0].presence == QueryPresence.PROHIBITED

    def test_multiple_terms_with_presence_creates_two_clauses(self):
        clauses = parse("+foo +bar")
        assert len(clauses) == 2
        assert clauses[0].term == "foo"
        assert clauses[1].term == "bar"
        assert clauses[0].presence == QueryPresence.REQUIRED
        assert clauses[1].presence == QueryPresence.REQUIRED

    def test_unknown_field(self):
        with pytest.raises(QueryParseError):
            parse("unknown:foo")

    def test_field_without_a_term(self):
        with pytest.raises(QueryParseError):
            parse("title:")

    def test_field_twice(self):
        with pytest.raises(QueryParseError):
            parse("title:title:")

    def test_term_with_field(self):
        clauses = parse("title:foo")
        assert len(clauses) == 1
        assert clauses[0].fields == ["title"]

    def test_uppercase_field_with_uppercase_term(self):
        query = Query(["TITLE"])
        parser = QueryParser("TITLE:FOO", query)

        parser.parse()
        clauses = query.clauses

        assert len(clauses) == 1
        assert clauses[0].term == "foo"
        assert clauses[0].fields == ["TITLE"]

    def test_multiple_terms_scoped_to_different_fields(self):
        clauses = parse("title:foo body:bar")

        assert len(clauses) == 2
        assert clauses[0].fields == ["title"]
        assert clauses[1].fields == ["body"]

        assert clauses[0].term == "foo"
        assert clauses[1].term == "bar"

    def test_single_term_with_edit_distance(self):
        clauses = parse("foo~2")

        assert len(clauses) == 1
        assert clauses[0].term == "foo"
        assert clauses[0].fields == ["title", "body"]
        assert clauses[0].edit_distance == 2

    def test_multiple_terms_with_edit_distance(self):
        clauses = parse("foo~2 bar~3")

        assert len(clauses) == 2
        assert clauses[0].fields == ["title", "body"]
        assert clauses[1].fields == ["title", "body"]

        assert clauses[0].term == "foo"
        assert clauses[1].term == "bar"

        assert clauses[0].edit_distance == 2
        assert clauses[1].edit_distance == 3

    def test_single_term_scoped_to_field_with_edit_distance(self):
        clauses = parse("title:foo~2")

        assert len(clauses) == 1
        assert clauses[0].term == "foo"
        assert clauses[0].fields == ["title"]
        assert clauses[0].edit_distance == 2

    def test_non_numeric_edit_distance(self):
        with pytest.raises(QueryParseError):
            parse("foo~a")

    def test_edit_distance_without_a_term(self):
        with pytest.raises(QueryParseError):
            parse("~2")

    def test_single_term_with_boost(self):
        clauses = parse("foo^2")

        assert len(clauses) == 1
        assert clauses[0].term == "foo"
        assert clauses[0].fields == ["title", "body"]
        assert clauses[0].boost == 2

    def test_non_numeric_boost(self):
        with pytest.raises(QueryParseError):
            parse("foo^a")

    def test_boost_without_a_term(self):
        with pytest.raises(QueryParseError):
            parse("^2")

    def test_multiple_terms_with_boost(self):
        clauses = parse("foo^2 bar^3")

        assert len(clauses) == 2
        assert clauses[0].fields == ["title", "body"]
        assert clauses[1].fields == ["title", "body"]

        assert clauses[0].term == "foo"
        assert clauses[1].term == "bar"

        assert clauses[0].boost == 2
        assert clauses[1].boost == 3

    def test_term_scoped_by_field_with_boost(self):
        clauses = parse("title:foo^2")

        assert len(clauses) == 1
        assert clauses[0].term == "foo"
        assert clauses[0].fields == ["title"]
        assert clauses[0].boost == 2

    def test_term_with_boost_and_edit_distance(self):
        clauses = parse("foo^2~3")

        assert len(clauses) == 1
        assert clauses[0].term == "foo"
        assert clauses[0].fields == ["title", "body"]
        assert clauses[0].edit_distance == 3
        assert clauses[0].boost == 2

    def test_edit_distance_followed_by_presence(self):
        clauses = parse("foo~10 +bar")

        assert len(clauses) == 2

        assert clauses[0].fields == ["title", "body"]
        assert clauses[1].fields == ["title", "body"]

        assert clauses[0].term == "foo"
        assert clauses[1].term == "bar"

        assert clauses[0].edit_distance == 10
        assert clauses[1].edit_distance == 0

        assert clauses[0].presence == QueryPresence.OPTIONAL
        assert clauses[1].presence == QueryPresence.REQUIRED

    def test_boost_followed_by_presence(self):
        clauses = parse("foo^10 +bar")

        assert len(clauses) == 2

        assert clauses[0].fields == ["title", "body"]
        assert clauses[1].fields == ["title", "body"]

        assert clauses[0].term == "foo"
        assert clauses[1].term == "bar"

        assert clauses[0].boost == 10
        assert clauses[1].boost == 1

        assert clauses[0].presence == QueryPresence.OPTIONAL
        assert clauses[1].presence == QueryPresence.REQUIRED
