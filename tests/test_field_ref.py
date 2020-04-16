import pytest

from lunr.field_ref import FieldRef
from lunr.exceptions import BaseLunrException


class TestFieldRef:
    def test_str_combines_document_ref_and_field_name(self):
        field_name = "title"
        document_ref = 123
        field_ref = FieldRef(document_ref, field_name)

        assert str(field_ref) == "title/123"
        assert repr(field_ref) == '<FieldRef field="title" ref="123">'

    def test_from_string_splits_string_into_parts(self):
        field_ref = FieldRef.from_string("title/123")

        assert field_ref.field_name == "title"
        assert field_ref.doc_ref == "123"

    def test_from_string_docref_contains_join_character(self):
        field_ref = FieldRef.from_string("title/http://example.com/123")

        assert field_ref.field_name == "title"
        assert field_ref.doc_ref == "http://example.com/123"

    def test_from_string_does_not_contain_join_character(self):
        string = "docRefOnly"

        with pytest.raises(BaseLunrException):
            FieldRef.from_string(string)
