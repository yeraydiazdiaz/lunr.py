import re

import pytest

from lunr.tokenizer import Tokenizer


class TestTokenizer:
    def test_splitting_into_tokens(self):
        tokenizer = Tokenizer("foo bar baz")
        tokens = [str(token) for token in tokenizer]

        assert tokens == ["foo", "bar", "baz"]

    def test_run_downcases_tokens(self):
        tokenizer = Tokenizer("foo BAR BAZ")
        tokens = [str(token) for token in tokenizer]

        assert tokens == ["foo", "bar", "baz"]

    def test_array_of_strings(self):
        tokenizer = Tokenizer(["foo", "bar", "baz"])
        tokens = [str(token) for token in tokenizer]

        assert tokens == ["foo", "bar", "baz"]

    def test_none_is_converted_to_empty_string(self):
        tokenizer = Tokenizer(["foo", None, "baz"])
        tokens = [str(token) for token in tokenizer]

        assert tokens == ["foo", "", "baz"]

    def test_multiple_whitespace_is_stripped(self):
        tokenizer = Tokenizer("   foo    bar   baz  ")
        tokens = [str(token) for token in tokenizer]

        assert tokens == ["foo", "bar", "baz"]

    def test_handling_null_like_arguments(self):
        assert len(Tokenizer(None)) == 0

    def test_converting_a_number_to_tokens(self):
        tokens = [str(token) for token in Tokenizer(41)]
        assert tokens == ["41"]

    def test_converting_a_boolean_to_tokens(self):
        tokens = [str(token) for token in Tokenizer(False)]
        assert tokens == ["false"]

    def test_converting_an_object_to_tokens(self):
        class Subject:
            def __str__(self):
                return "custom object"

        tokens = [str(token) for token in Tokenizer(Subject())]
        assert tokens == ["custom", "object"]

    def test_splits_strings_with_hyphens(self):
        tokens = [str(token) for token in Tokenizer("foo-bar")]
        assert tokens == ["foo", "bar"]

    def test_splits_strings_with_hyphens_and_spaces(self):
        tokens = [str(token) for token in Tokenizer("foo - bar")]
        assert tokens == ["foo", "bar"]

    def test_tracking_the_token_index(self):
        tokens = Tokenizer("foo bar")
        assert tokens[0].metadata["index"] == 0
        assert tokens[1].metadata["index"] == 1

    def test_tracking_the_token_position(self):
        tokens = Tokenizer("foo bar")
        assert tokens[0].metadata["position"] == [0, 3]
        assert tokens[1].metadata["position"] == [4, 3]

    def test_providing_additional_metadata(self):
        tokens = Tokenizer("foo bar", {"hurp": "durp"})
        assert tokens[0].metadata["hurp"] == "durp"
        assert tokens[1].metadata["hurp"] == "durp"

    @pytest.mark.parametrize("separator", [re.compile(r"[_\-]+"), lambda c: c in "_-"])
    def test_providing_separator(self, separator):
        tokens = [str(token) for token in Tokenizer("foo_bar-baz", separator=separator)]
        assert tokens == ["foo", "bar", "baz"]

    def test_tracking_token_position_with_left_hand_whitespace(self):
        tokens = Tokenizer(" foo bar")
        assert tokens[0].metadata["position"] == [1, 3]
        assert tokens[1].metadata["position"] == [5, 3]

    def test_tracking_token_position_with_right_hand_whitespace(self):
        tokens = Tokenizer("foo bar ")
        assert tokens[0].metadata["position"] == [0, 3]
        assert tokens[1].metadata["position"] == [4, 3]
