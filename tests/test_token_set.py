import pytest

from lunr.token_set import TokenSet


class TestTokenSet:

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

        one_edge.edges['a'] = 1
        two_edges.edges['a'] = 1
        two_edges.edges['b'] = 1

        assert str(zero_edges) != str(one_edge)
        assert str(two_edges) != str(one_edge)
        assert str(two_edges) != str(zero_edges)

    def test_str_includes_edge_id(self):
        child_a = TokenSet()
        child_b = TokenSet()
        parent_a = TokenSet()
        parent_b = TokenSet()
        parent_c = TokenSet()

        parent_a.edges['a'] = child_a
        parent_b.edges['a'] = child_b
        parent_c.edges['a'] = child_b

        assert str(parent_b) == str(parent_c)
        assert str(parent_a) != str(parent_c)
        assert str(parent_a) != str(parent_b)

    def test_from_string_without_wildcard(self):
        TokenSet._next_id = 1
        x = TokenSet.from_string('a')

        assert str(x) == '0a2'
        assert x.edges['a'].final

    def test_from_string_with_trailing_wildcard(self):
        x = TokenSet.from_string('a*')
        wild = x.edges['a'].edges['*']

        assert wild == wild.edges['*']
        assert wild.final

    def test_from_list_with_unsorted_list(self):
        with pytest.raises(Exception):
            TokenSet.from_list(['z', 'a'])

    def test_from_list_with_sorted_list(self):
        token_set = TokenSet.from_list(['a', 'z'])
        assert ['a', 'z'] == sorted(token_set.to_list())

    def test_to_list_includes_all_words(self):
        words = ['bat', 'cat']
        token_set = TokenSet.from_list(words)

        assert set(words) == set(token_set.to_list())
