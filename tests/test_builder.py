import pytest

from lunr.builder import Builder
from lunr.token_set import TokenSet
from lunr.index import Index
from lunr.vector import Vector


def _assert_deep_keys(dict_, keys):
    d = dict_
    for key in keys.split("."):
        d_keys_as_str = [str(k) for k in d]
        assert key in d_keys_as_str
        d = d[key]


class TestBuilderBuild:
    def setup_method(self, method):
        self.builder = Builder()
        doc = {"id": "id", "title": "test", "body": "missing"}

        self.builder.ref("id")
        self.builder.field("title")
        self.builder.add(doc)
        self.index = self.builder.build()

    def test_adds_tokens_to_inverted_index(self):
        _assert_deep_keys(self.builder.inverted_index, "test.title.id")

    def test_builds_vector_space_of_the_document_fields(self):
        assert "title/id" in self.builder.field_vectors
        assert isinstance(self.builder.field_vectors["title/id"], Vector)

    def test_skips_fields_not_defined_for_indexing(self):
        assert "missing" not in self.builder.inverted_index

    def test_builds_a_token_set_for_the_corpus(self):
        needle = TokenSet.from_string("test")
        assert "test" in self.builder.token_set.intersect(needle).to_list()

    def test_calculates_document_count(self):
        assert self.builder.average_field_length["title"] == 1

    def test_index_is_returned(self):
        assert isinstance(self.index, Index)


class TestBuilderAdd:
    def test_builder_casts_docrefs_to_strings(self):
        self.builder = Builder()
        self.builder.ref("id")
        self.builder.field("title")

        self.builder.add(dict(id=123, title="test", body="missing"))

        _assert_deep_keys(self.builder.inverted_index, "test.title.123")

    def test_builder_metadata_whitelist_includes_metadata_in_index(self):
        self.builder = Builder()
        self.builder.ref("id")
        self.builder.field("title")
        self.builder.metadata_whitelist = ["position"]

        self.builder.add(dict(id="a", title="test", body="missing"))
        self.builder.add(dict(id="b", title="another test", body="missing"))

        assert self.builder.inverted_index["test"]["title"]["a"] == {
            "position": [[0, 4]]
        }
        assert self.builder.inverted_index["test"]["title"]["b"] == {
            "position": [[8, 4]]
        }

    def test_builder_field_raises_if_contains_slash(self):
        self.builder = Builder()

        with pytest.raises(ValueError):
            self.builder.field("foo/bar")

    def test_builder_extracts_nested_properties_from_document(self):
        self.builder = Builder()
        self.builder.field("name", extractor=lambda d: d["person"]["name"])

        self.builder.add({"id": "id", "person": {"name": "bob"}})

        assert self.builder.inverted_index["bob"]["name"]["id"] == {}

    def test_builder_field_term_frequency_and_length(self):
        self.builder = Builder()
        self.builder.ref("id")
        self.builder.field("title")

        self.builder.add(dict(id="a", title="test a testing test", body="missing"))

        assert self.builder.field_term_frequencies == {
            "title/a": {"test": 2, "a": 1, "testing": 1}
        }
        assert self.builder.field_lengths == {"title/a": 4}


class TestBuilderUse:
    def setup_method(self, method):
        self.builder = Builder()

    def test_calls_plugin_function(self):
        def plugin(*args):
            assert True

        self.builder.use(plugin)

    def test_plugin_is_called_with_builder_as_first_argument(self):
        def plugin(builder):
            assert builder is self.builder

        self.builder.use(plugin)

    def test_forwards_arguments_to_the_plugin(self):
        def plugin(builder, *args, **kwargs):
            assert args == (1, 2, 3)
            assert kwargs == {"foo": "bar"}

        self.builder.use(plugin, 1, 2, 3, foo="bar")


class TestBuilderK1:
    def test_k1_default_value(self):
        builder = Builder()
        assert builder._k1 == 1.2

    def test_k1_can_be_set(self):
        builder = Builder()
        builder.k1(1.6)
        assert builder._k1 == 1.6


class TestBuilderB:
    def test_b_default_value(self):
        builder = Builder()
        assert builder._b == 0.75

    def test_b_within_range(self):
        builder = Builder()
        builder.b(0.5)
        assert builder._b == 0.5

    def test_b_less_than_zero(self):
        builder = Builder()
        builder.b(-1)
        assert builder._b == 0

    def test_b_higher_than_one(self):
        builder = Builder()
        builder.b(1.5)
        assert builder._b == 1


class TestBuilerRef:
    def test_default_reference(self):
        builder = Builder()
        assert builder._ref == "id"

    def test_defining_a_reference_field(self):
        builder = Builder()
        builder.ref("foo")
        assert builder._ref == "foo"


class TestBuilderField:
    def test_define_fields_to_index(self):
        builder = Builder()
        builder.field("foo")
        assert len(builder._fields) == 1
        assert builder._fields["foo"].name == "foo"
        assert builder._fields["foo"].boost == 1
        assert builder._fields["foo"].extractor is None
        assert repr(builder._fields["foo"]) == '<Field "foo" boost="1">'
        assert hash(builder._fields["foo"]) == hash("foo")
