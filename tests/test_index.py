from mock import MagicMock

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

    def test_query_no_arguments_warns_and_returns_no_results(
            self, monkeypatch, index):
        from lunr.index import logger
        mock_logger = MagicMock()
        monkeypatch.setattr(logger, 'warning', mock_logger)
        results = index.query()
        assert results == []
        mock_logger.assert_called_once()

    def test_query_callback_argument_is_query_with_fields(self, index):
        def callback(query):
            assert query.all_fields == index.fields

        index.query(callback=callback)

    def test_query_callback_can_configure_query(self, index):
        def callback(query):
            query.clause('study')

        results = index.query(callback=callback)
        assert len(results) == 2
        assert results[0]['ref'] == 'b'
        assert results[1]['ref'] == 'a'

    def test_serialization(self, index):
        serialized_index = index.serialize()
        assert serialized_index['version'] == __TARGET_JS_VERSION__
        assert serialized_index['fields'] == index.fields
        for ref, vector in serialized_index['fieldVectors']:
            assert ref in index.field_vectors
            assert_vectors_equal(vector, index.field_vectors[ref])
