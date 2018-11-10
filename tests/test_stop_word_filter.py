from lunr.stop_word_filter import stop_word_filter, generate_stop_word_filter
from lunr.pipeline import Pipeline

STOP_WORDS = ["the", "and", "but", "than", "when"]


class TestStopWordFilter:
    def test_filters_stop_words(self):
        for word in STOP_WORDS:
            assert stop_word_filter(word) is None

    def test_ignores_non_stop_words(self):
        non_stop_words = ["interesting", "words", "pass", "through"]
        for word in non_stop_words:
            assert stop_word_filter(word) == word

    def test_is_a_registered_pipeline_function(self):
        assert stop_word_filter.label == "stopWordFilter"
        assert Pipeline.registered_functions["stopWordFilter"] == stop_word_filter


class TestGenerateStopWordFilter:
    def test_creates_correct_stop_words_filter(self):
        new_stop_word_filter = generate_stop_word_filter(STOP_WORDS)
        for word in STOP_WORDS:
            assert new_stop_word_filter(word) is None

    def test_registers_new_stop_words_filter(self):
        new_stop_word_filter = generate_stop_word_filter(STOP_WORDS)
        assert new_stop_word_filter.label == "stopWordFilter"
        assert Pipeline.registered_functions["stopWordFilter"] == new_stop_word_filter

    def test_passing_a_language_adds_to_registered_label(self):
        new_stop_word_filter = generate_stop_word_filter(STOP_WORDS, "es")
        assert new_stop_word_filter.label == "stopWordFilter-es"
        assert (
            Pipeline.registered_functions["stopWordFilter-es"] == new_stop_word_filter
        )
