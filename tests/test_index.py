import pytest

from lunr.exceptions import BaseLunrException


class TestIndex:

    def test_create_query_default_fields(self, index):
        query = index.create_query()
        assert query.all_fields == index.fields

    def test_create_query_subset_of_fields(self, index):
        query = index.create_query([index.fields[0]])
        assert query.all_fields == [index.fields[0]]

    def test_create_query_non_contained_fields(self, index):
        with pytest.raises(BaseLunrException):
            index.create_query(['foo'])
