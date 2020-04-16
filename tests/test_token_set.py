import pytest

from lunr.token_set import TokenSet
from lunr.exceptions import BaseLunrException


class TestTokenSetStr:
    def test_str_includes_node_finality(self):
        non_final = TokenSet()
        final = TokenSet()
        other_final = TokenSet()

        final.final = True
        other_final.final = True

        assert str(non_final) != str(final)
        assert str(other_final) == str(final)

    def test_str_includes_all_edges(self):
        zero_edges = TokenSet()
        one_edge = TokenSet()
        two_edges = TokenSet()

        one_edge.edges["a"] = 1
        two_edges.edges["a"] = 1
        two_edges.edges["b"] = 1

        assert str(zero_edges) != str(one_edge)
        assert str(two_edges) != str(one_edge)
        assert str(two_edges) != str(zero_edges)

    def test_str_includes_edge_id(self):
        child_a = TokenSet()
        child_b = TokenSet()
        parent_a = TokenSet()
        parent_b = TokenSet()
        parent_c = TokenSet()

        parent_a.edges["a"] = child_a
        parent_b.edges["a"] = child_b
        parent_c.edges["a"] = child_b

        assert str(parent_b) == str(parent_c)
        assert str(parent_a) != str(parent_c)
        assert str(parent_a) != str(parent_b)


class TestTokenSetFromString:
    def test_from_string_without_wildcard(self):
        TokenSet._next_id = 1
        x = TokenSet.from_string("a")

        assert str(x) == "0a2"
        assert x.edges["a"].final

    def test_from_string_with_trailing_wildcard(self):
        x = TokenSet.from_string("a*")
        wild = x.edges["a"].edges["*"]

        assert wild == wild.edges["*"]
        assert wild.final


class TestTokenSetFromList:
    def test_from_list_with_unsorted_list(self):
        with pytest.raises(BaseLunrException):
            TokenSet.from_list(["z", "a"])

    def test_from_list_with_sorted_list(self):
        token_set = TokenSet.from_list(["a", "z"])
        assert ["a", "z"] == sorted(token_set.to_list())

    def test_from_list_is_minimal(self):
        token_set = TokenSet.from_list(["ac", "dc"])
        ac_node = token_set.edges["a"].edges["c"]
        dc_node = token_set.edges["d"].edges["c"]

        assert ac_node == dc_node


class TestTokenSetToList:
    def test_to_list_includes_all_words(self):
        words = ["bat", "cat"]
        token_set = TokenSet.from_list(words)

        assert set(words) == set(token_set.to_list())

    def test_to_list_includes_single_words(self):
        word = "bat"
        token_set = TokenSet.from_string(word)

        assert {word} == set(token_set.to_list())


class TestTokenSetIntersect:
    def test_no_intersection(self):
        x = TokenSet.from_string("cat")
        y = TokenSet.from_string("bar")
        z = x.intersect(y)

        assert len(z.to_list()) == 0

    def test_simple_intersection(self):
        x = TokenSet.from_string("cat")
        y = TokenSet.from_string("cat")
        z = x.intersect(y)

        assert {"cat"} == set(z.to_list())

    def test_trailing_wildcard_intersection(self):
        x = TokenSet.from_string("cat")
        y = TokenSet.from_string("c*")
        z = x.intersect(y)

        assert {"cat"} == set(z.to_list())

    def test_trailing_wildcard_no_intersection(self):
        x = TokenSet.from_string("cat")
        y = TokenSet.from_string("b*")
        z = x.intersect(y)

        assert len(z.to_list()) == 0

    def test_leading_wildcard_intersection(self):
        x = TokenSet.from_string("cat")
        y = TokenSet.from_string("*t")
        z = x.intersect(y)

        assert {"cat"} == set(z.to_list())

    def test_leading_wildcard_no_intersection(self):
        x = TokenSet.from_string("cat")
        y = TokenSet.from_string("*r")
        z = x.intersect(y)

        assert len(z.to_list()) == 0

    def test_contained_wildcard_intersection(self):
        x = TokenSet.from_string("foo")
        y = TokenSet.from_string("f*o")
        z = x.intersect(y)

        assert {"foo"} == set(z.to_list())

    def test_contained_wildcard_no_intersection(self):
        x = TokenSet.from_string("foo")
        y = TokenSet.from_string("b*r")
        z = x.intersect(y)

        assert len(z.to_list()) == 0

    def test_wildcard_zero_or_more_characters(self):
        x = TokenSet.from_string("foo")
        y = TokenSet.from_string("foo*")
        z = x.intersect(y)

        assert {"foo"} == set(z.to_list())

    def test_with_fuzzy_string_substitution(self):
        x1 = TokenSet.from_string("bar")
        x2 = TokenSet.from_string("cur")
        x3 = TokenSet.from_string("cat")
        x4 = TokenSet.from_string("car")
        x5 = TokenSet.from_string("foo")
        y = TokenSet.from_fuzzy_string("car", 1)

        assert x1.intersect(y).to_list() == ["bar"]
        assert x2.intersect(y).to_list() == ["cur"]
        assert x3.intersect(y).to_list() == ["cat"]
        assert x4.intersect(y).to_list() == ["car"]
        assert x5.intersect(y).to_list() == []

    def test_with_fuzzy_string_deletion(self):
        x1 = TokenSet.from_string("ar")
        x2 = TokenSet.from_string("br")
        x3 = TokenSet.from_string("ba")
        x4 = TokenSet.from_string("bar")
        x5 = TokenSet.from_string("foo")
        y = TokenSet.from_fuzzy_string("bar", 1)

        assert x1.intersect(y).to_list() == ["ar"]
        assert x2.intersect(y).to_list() == ["br"]
        assert x3.intersect(y).to_list() == ["ba"]
        assert x4.intersect(y).to_list() == ["bar"]
        assert x5.intersect(y).to_list() == []

    def test_with_fuzzy_string_insertion(self):
        x1 = TokenSet.from_string("bbar")
        x2 = TokenSet.from_string("baar")
        x3 = TokenSet.from_string("barr")
        x4 = TokenSet.from_string("bar")
        x5 = TokenSet.from_string("ba")
        x6 = TokenSet.from_string("foo")
        x7 = TokenSet.from_string("bara")
        y = TokenSet.from_fuzzy_string("bar", 1)

        assert x1.intersect(y).to_list() == ["bbar"]
        assert x2.intersect(y).to_list() == ["baar"]
        assert x3.intersect(y).to_list() == ["barr"]
        assert x4.intersect(y).to_list() == ["bar"]
        assert x5.intersect(y).to_list() == ["ba"]
        assert x6.intersect(y).to_list() == []
        assert x7.intersect(y).to_list() == ["bara"]

    def test_with_fuzzy_string_transpose(self):
        x1 = TokenSet.from_string("abr")
        x2 = TokenSet.from_string("bra")
        x3 = TokenSet.from_string("foo")
        y = TokenSet.from_fuzzy_string("bar", 1)

        assert x1.intersect(y).to_list() == ["abr"]
        assert x2.intersect(y).to_list() == ["bra"]
        assert x3.intersect(y).to_list() == []

    def test_fuzzy_string_insertion(self):
        x = TokenSet.from_string("abcxx")
        y = TokenSet.from_fuzzy_string("abc", 2)

        assert x.intersect(y).to_list() == ["abcxx"]

    def test_fuzzy_string_substitution(self):
        x = TokenSet.from_string("axx")
        y = TokenSet.from_fuzzy_string("abc", 2)

        assert x.intersect(y).to_list() == ["axx"]

    def test_fuzzy_string_deletion(self):
        x = TokenSet.from_string("a")
        y = TokenSet.from_fuzzy_string("abc", 2)

        assert x.intersect(y).to_list() == ["a"]

    def test_fuzzy_string_transpose(self):
        x = TokenSet.from_string("bca")
        y = TokenSet.from_fuzzy_string("abc", 2)

        assert x.intersect(y).to_list() == ["bca"]

    def test_leading_wildcard_backtracking_intersection(self):
        x = TokenSet.from_string("aaacbab")
        y = TokenSet.from_string("*ab")

        assert x.intersect(y).to_list() == ["aaacbab"]

    def test_leading_wildcard_backtracking_no_intersection(self):
        x = TokenSet.from_string("aaacbab")
        y = TokenSet.from_string("*abc")

        assert x.intersect(y).to_list() == []

    def test_contained_wildcard_backtracking_intersection(self):
        x = TokenSet.from_string("ababc")
        y = TokenSet.from_string("a*bc")

        assert x.intersect(y).to_list() == ["ababc"]

    def test_contained_wildcard_backtracking_no_intersection(self):
        x = TokenSet.from_string("ababc")
        y = TokenSet.from_string("a*ac")

        assert x.intersect(y).to_list() == []

    @pytest.mark.timeout(2)
    def test_catastrophic_backtracking_with_leading_characters(self):
        x = TokenSet.from_string("f" * 100)
        y = TokenSet.from_string("*f")

        assert len(x.intersect(y).to_list()) == 1

    def test_leading_trailing_wildcard_backtracking_intersection(self):
        x = TokenSet.from_string("acbaabab")
        y = TokenSet.from_string("*ab*")

        assert x.intersect(y).to_list() == ["acbaabab"]

    def test_leading_atrailing_wildcard_backtracking_intersection(self):
        x = TokenSet.from_string("acbaabab")
        y = TokenSet.from_string("a*ba*b")

        assert x.intersect(y).to_list() == ["acbaabab"]
