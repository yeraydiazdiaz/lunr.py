import pytest

from lunr import __TARGET_JS_VERSION__
from lunr.exceptions import BaseLunrException

from tests.utils import assert_vectors_equal


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

    def test_serialization(self, index):
        serialized_index = index.serialize()
        assert serialized_index['version'] == __TARGET_JS_VERSION__
        assert serialized_index['fields'] == index.fields
        for ref, vector in serialized_index['fieldVectors']:
            assert ref in index.field_vectors
            assert_vectors_equal(vector, index[ref])
