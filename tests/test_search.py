import pytest

from lunr import lunr
from lunr.query import Query, QueryPresence
from lunr.exceptions import QueryParseError


class TestSingleTermSearch:
    def test_one_match(self, index):
        results = index.search("scarlett")
        assert len(results) == 1
        assert results[0]["ref"] == "c"
        assert set(results[0]["match_data"].metadata.keys()) == {"scarlett"}

    def test_no_match(self, index):
        results = index.search("foo")
        assert len(results) == 0

    def test_multiple_matches_sorts_by_relevance(self, index):
        results = index.search("plant")
        assert len(results) == 2
        assert results[0]["ref"] == "b"
        assert results[1]["ref"] == "c"

    def test_pipeline_processing_enabled(self, index):
        query = Query(index.fields)
        query.clause(term="study", use_pipeline=True)  # stemmed to studi
        results = index.query(query)

        assert len(results) == 2
        assert results[0]["ref"] == "b"
        assert results[1]["ref"] == "a"

    def test_pipeline_processing_disabled(self, index):
        query = Query(index.fields)
        query.clause(term="study", use_pipeline=False)  # stemmed to studi
        results = index.query(query)

        assert len(results) == 0

    def test_multiple_terms_all_terms_match(self, index):
        results = index.search("fellow candlestick")

        assert len(results) == 1
        assert results[0]["ref"] == "a"
        metadata = results[0]["match_data"].metadata
        assert set(metadata.keys()) == {"fellow", "candlestick"}
        assert set(metadata["fellow"].keys()) == {"body"}
        assert set(metadata["candlestick"].keys()) == {"body"}

    def test_one_term_matches(self, index):
        results = index.search("week foo")

        assert len(results) == 1
        assert results[0]["ref"] == "c"
        metadata = results[0]["match_data"].metadata
        assert set(metadata.keys()) == {"week"}

    def test_duplicate_query_terms(self, index):
        index.search("fellow candlestick foo bar green plant fellow")

    def test_documents_with_all_terms_score_higher(self, index):
        results = index.search("candlestick green")

        assert len(results) == 3

        assert {r["ref"] for r in results} == {"a", "b", "c"}
        assert set(results[0]["match_data"].metadata.keys()) == {"candlestick", "green"}
        assert set(results[1]["match_data"].metadata.keys()) == {"green"}
        assert set(results[2]["match_data"].metadata.keys()) == {"green"}

    def test_no_terms_match(self, index):
        results = index.search("foo bar")

        assert len(results) == 0

    def test_corpus_terms_are_stemmed(self, index):
        results = index.search("water")

        assert len(results) == 2
        assert {r["ref"] for r in results} == {"b", "c"}

    def test_field_scoped_terms(self, index):
        results = index.search("title:plant")

        assert len(results) == 1
        assert results[0]["ref"] == "b"
        assert set(results[0]["match_data"].metadata.keys()) == {"plant"}

    def test_field_scoped_no_matching_terms(self, index):
        results = index.search("title:candlestick")

        assert len(results) == 0


class TestSearchWildcardTrailing:
    def test_matching_no_matches(self, index):
        results = index.search("fo*")

        assert len(results) == 0

    def test_matching_one_match(self, index):
        results = index.search("candle*")

        assert len(results) == 1
        assert results[0]["ref"] == "a"
        assert set(results[0]["match_data"].metadata.keys()) == {"candlestick"}

    def test_matching_multiple_terms_match(self, index):
        results = index.search("pl*")

        assert len(results) == 2

        assert {r["ref"] for r in results} == {"b", "c"}
        assert set(results[0]["match_data"].metadata.keys()) == {"plumb", "plant"}
        assert set(results[1]["match_data"].metadata.keys()) == {"plumb", "plant"}


class TestSearchWildcardLeading:
    def test_matching_no_matches(self, index):
        results = index.search("*oo")

        assert len(results) == 0

    def test_matching_multiple_terms_match(self, index):
        results = index.search("*ant")

        assert len(results) == 2
        assert {r["ref"] for r in results} == {"b", "c"}
        assert set(results[0]["match_data"].metadata.keys()) == {"plant"}
        assert set(results[1]["match_data"].metadata.keys()) == {"plant"}


class TestSearchWildcardContained:
    def test_matching_no_matches(self, index):
        results = index.search("f*o")
        assert len(results) == 0

    def test_matching_multiple_terms_match(self, index):
        results = index.search("pl*nt")

        assert len(results) == 2
        assert {r["ref"] for r in results} == {"b", "c"}
        assert set(results[0]["match_data"].metadata.keys()) == {"plant"}
        assert set(results[1]["match_data"].metadata.keys()) == {"plant"}


class TestEditDistance:
    def test_edit_distance_no_results(self, index):
        results = index.search("foo~1")
        assert len(results) == 0

    def test_edit_distance_two_results(self, index):
        results = index.search("plont~1")

        assert len(results) == 2
        assert {r["ref"] for r in results} == {"b", "c"}
        assert set(results[0]["match_data"].metadata.keys()) == {"plant"}
        assert set(results[1]["match_data"].metadata.keys()) == {"plant"}


class TestSearchByField:
    def test_search_by_field_unknown_field(self, index):
        with pytest.raises(QueryParseError):
            index.search("unknown-field:plant")

    def test_search_by_field_no_results(self, index):
        results = index.search("title:candlestick")
        assert len(results) == 0

    def test_search_by_field_results(self, index):
        results = index.search("title:plant")

        assert len(results) == 1
        assert results[0]["ref"] == "b"
        assert set(results[0]["match_data"].metadata.keys()) == {"plant"}


class TestTermBoosts:
    def test_term_boosts_no_results(self, index):
        results = index.search("foo^10")
        assert len(results) == 0

    def test_term_boosts_results(self, index):
        results = index.search("scarlett candlestick^5")

        assert len(results) == 2
        assert {r["ref"] for r in results} == {"a", "c"}
        assert set(results[0]["match_data"].metadata.keys()) == {"candlestick"}
        assert set(results[1]["match_data"].metadata.keys()) == {"scarlett"}


class TestTypeaheadStyleSearch:
    def test_typeahead_no_results(self, index):
        query = Query(index.fields)
        query.clause("xyz", boost=100, use_pipeline=True)
        query.clause(
            "xyz", boost=10, use_pipeline=False, wildcard=Query.WILDCARD_TRAILING
        )
        query.clause("xyz", boost=1, edit_distance=1)

        results = index.query(query)
        assert len(results) == 0

    def test_typeahead_results(self, index):
        query = Query(index.fields)
        query.clause("pl", boost=100, use_pipeline=True)
        query.clause(
            "pl", boost=10, use_pipeline=False, wildcard=Query.WILDCARD_TRAILING
        )
        query.clause("pl", boost=1, edit_distance=1)

        results = index.query(query)

        assert len(results) == 2
        assert {r["ref"] for r in results} == {"b", "c"}
        assert set(results[0]["match_data"].metadata.keys()) == {"plumb", "plant"}
        assert set(results[1]["match_data"].metadata.keys()) == {"plumb", "plant"}


class TestTermPresence:
    @pytest.mark.parametrize("query_or_search", ["query", "search"])
    def test_prohibited_match_excludes_prohibited_result(self, index, query_or_search):
        if query_or_search == "query":
            query = Query(index.fields)
            query.term("candlestick", presence=QueryPresence.PROHIBITED)
            query.term("green", presence=QueryPresence.OPTIONAL)
            results = index.query(query)
        else:
            results = index.search("-candlestick green")

        assert len(results) == 2
        assert {r["ref"] for r in results} == {"b", "c"}
        assert set(results[0]["match_data"].metadata.keys()) == {"green"}
        assert set(results[1]["match_data"].metadata.keys()) == {"green"}

    @pytest.mark.parametrize("query_or_search", ["query", "search"])
    def test_only_prohibited_match_yields_no_results(self, index, query_or_search):
        if query_or_search == "query":
            query = Query(index.fields)
            query.term("green", presence=QueryPresence.PROHIBITED)
            results = index.query(query)
        else:
            results = index.search("-green")

        assert len(results) == 0

    @pytest.mark.parametrize("query_or_search", ["query", "search"])
    def test_negated_query_no_match(self, index, query_or_search):
        if query_or_search == "query":
            query = Query(index.fields)
            query.term("qwertyuiop", presence=QueryPresence.PROHIBITED)
            results = index.query(query)
        else:
            results = index.search("-qwertyuiop")

        assert len(results) == 3

    @pytest.mark.parametrize("query_or_search", ["query", "search"])
    def test_negated_query_some_match(self, index, query_or_search):
        if query_or_search == "query":
            query = Query(index.fields)
            query.term("plant", presence=QueryPresence.PROHIBITED)
            results = index.query(query)
        else:
            results = index.search("-plant")

        assert len(results) == 1
        assert results[0]["score"] == 0

    @pytest.mark.parametrize("query_or_search", ["query", "search"])
    def test_field_match(self, index, query_or_search):
        if query_or_search == "query":
            query = Query(index.fields)
            query.term("plant", presence=QueryPresence.PROHIBITED, fields=["title"])
            query.term("plumb", presence=QueryPresence.OPTIONAL)
            results = index.query(query)
        else:
            results = index.search("-title:plant plumb")

        assert len(results) == 1
        assert set(results[0]["match_data"].metadata.keys()) == {"plumb"}

    @pytest.mark.parametrize("query_or_search", ["query", "search"])
    def test_required_match(self, index, query_or_search):
        if query_or_search == "query":
            query = Query(index.fields)
            query.term("candlestick", presence=QueryPresence.REQUIRED)
            query.term("green", presence=QueryPresence.OPTIONAL)
            results = index.query(query)
        else:
            results = index.search("+candlestick green")

        assert len(results) == 1
        assert set(results[0]["match_data"].metadata.keys()) == {"candlestick", "green"}

    @pytest.mark.parametrize("query_or_search", ["query", "search"])
    def test_two_required_matches_yields_no_results(self, index, query_or_search):
        if query_or_search == "query":
            query = Query(index.fields)
            query.term("mustard", presence=QueryPresence.REQUIRED)
            query.term("plant", presence=QueryPresence.REQUIRED)
            results = index.query(query)
        else:
            results = index.search("+mustard +plant")

        assert len(results) == 0

    @pytest.mark.parametrize("query_or_search", ["query", "search"])
    def test_required_term_not_matching_yields_no_results(self, index, query_or_search):
        if query_or_search == "query":
            query = Query(index.fields)
            query.term("qwertyuiop", presence=QueryPresence.REQUIRED)
            query.term("green", presence=QueryPresence.OPTIONAL)
            results = index.query(query)
        else:
            results = index.search("+qwertyuiop green")

        assert len(results) == 0

    @pytest.mark.parametrize("query_or_search", ["query", "search"])
    def test_required_term_on_field_matches(self, index, query_or_search):
        if query_or_search == "query":
            query = Query(index.fields)
            query.term("plant", presence=QueryPresence.REQUIRED, fields=["title"])
            query.term("green", presence=QueryPresence.OPTIONAL)
            results = index.query(query)
        else:
            results = index.search("+title:plant green")

        assert len(results) == 1
        assert set(results[0]["match_data"].metadata.keys()) == {"plant", "green"}
        assert results[0]["ref"] == "b"

    @pytest.mark.parametrize("query_or_search", ["query", "search"])
    def test_required_terms_on_field_and_non_field_match(self, index, query_or_search):
        if query_or_search == "query":
            query = Query(index.fields)
            query.term("plant", presence=QueryPresence.REQUIRED, fields=["title"])
            query.term("green", presence=QueryPresence.REQUIRED)
            results = index.query(query)
        else:
            results = index.search("+title:plant +green")

        assert len(results) == 1
        assert set(results[0]["match_data"].metadata.keys()) == {"plant", "green"}
        assert results[0]["ref"] == "b"

    @pytest.mark.parametrize("query_or_search", ["query", "search"])
    def test_required_terms_on_different_fields_match(self, index, query_or_search):
        if query_or_search == "query":
            query = Query(index.fields)
            query.term("plant", presence=QueryPresence.REQUIRED, fields=["title"])
            query.term("study", presence=QueryPresence.REQUIRED, fields=["body"])
            results = index.query(query)
        else:
            results = index.search("+title:plant +body:study")

        assert len(results) == 1
        assert set(results[0]["match_data"].metadata.keys()) == {"studi", "plant"}
        assert results[0]["ref"] == "b"

    @pytest.mark.parametrize("query_or_search", ["query", "search"])
    def test_combined_required_optional_and_prohibited_match(
        self, index, query_or_search
    ):
        if query_or_search == "query":
            query = Query(index.fields)
            query.term("plant", presence=QueryPresence.REQUIRED)
            query.term("green", presence=QueryPresence.OPTIONAL)
            query.term("office", presence=QueryPresence.PROHIBITED)
            results = index.query(query)
        else:
            results = index.search("+plant green -office")

        assert len(results) == 1
        assert set(results[0]["match_data"].metadata.keys()) == {"green", "plant"}
        assert results[0]["ref"] == "b"


class TestBuildTimeFieldBoost:
    @pytest.mark.parametrize("query_or_search", ["query", "search"])
    def test_no_query_boosts_build_boost_ranks_higher(self, documents, query_or_search):
        idx = lunr(
            ref="id",
            fields=["title", {"field_name": "body", "boost": 10}],
            documents=documents,
        )

        if query_or_search == "search":
            results = idx.search("professor")
        else:
            query = Query(idx.fields)
            query.term("professor")
            results = idx.query(query)

        assert results[0]["ref"] == "b"


class TestBuildTimeDocumentBoost:
    @pytest.mark.parametrize("query_or_search", ["query", "search"])
    def test_no_query_boosts_document_boost_ranks_higher(
        self, documents, query_or_search
    ):
        documents_with_boost = [
            (document, {"boost": 10 if document["id"] == "c" else 1})
            for document in documents
        ]
        idx = lunr(ref="id", fields=("title", "body"), documents=documents_with_boost)

        if query_or_search == "search":
            results = idx.search("plumb")
        else:
            query = Query(idx.fields)
            query.term("plumb")
            results = idx.query(query)

        assert results[0]["ref"] == "c"
