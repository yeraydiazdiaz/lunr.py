import pytest

from lunr.trimmer import trimmer
from lunr.token import Token
from lunr.pipeline import Pipeline


class TestTrimmer:
    def test_latin_characters(self):
        token = Token("hello")
        assert str(trimmer(token)) == str(token)

    @pytest.mark.parametrize(
        "description, string, expected",
        [
            ("full stop", "hello.", "hello"),
            ("inner apostrophe", "it's", "it's"),
            ("trailing apostrophe", "james'", "james"),
            ("exclamation mark", "stop!", "stop"),
            ("comma", "first,", "first"),
            ("brackets", "[tag]", "tag"),
        ],
    )
    def test_punctuation(self, description, string, expected):
        token = Token(string)
        trimmed = str(trimmer(token))

        assert trimmed == expected

    def test_is_a_registered_pipeline_function(self):
        assert trimmer.label == "trimmer"
        assert Pipeline.registered_functions["trimmer"] == trimmer
