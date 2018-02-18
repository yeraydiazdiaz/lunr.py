from lunr.stop_word_filter import stop_word_filter
from lunr.pipeline import Pipeline


class TestStopWordFilter:

    def test_filters_stop_words(self):
        stop_words = ['the', 'and', 'but', 'than', 'when']
        for word in stop_words:
            assert stop_word_filter(word) is None

    def test_ignores_non_stop_words(self):
        non_stop_words = ['interesting', 'words', 'pass', 'through']
        for word in non_stop_words:
            assert stop_word_filter(word) == word

    def test_is_a_registered_pipeline_function(self):
        assert stop_word_filter.label == 'stop_word_filter'
        assert Pipeline.registered_functions[
            'stop_word_filter'] == stop_word_filter
