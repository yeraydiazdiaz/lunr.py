import json
import os

from lunr.token import Token
from lunr.stemmer import stemmer
from lunr.pipeline import Pipeline


class TestStemmer:
    def test_reduces_words_to_their_stem(self):
        path = os.path.join(
            os.path.dirname(__file__), "fixtures", "stemming_vocab.json"
        )
        with open(path) as f:
            data = json.loads(f.read())

        for word, expected in data.items():
            token = Token(word)
            result = str(stemmer(token))

            assert result == expected

    def test_is_a_registered_pipeline_function(self):
        assert stemmer.label == "stemmer"
        assert Pipeline.registered_functions["stemmer"] == stemmer
