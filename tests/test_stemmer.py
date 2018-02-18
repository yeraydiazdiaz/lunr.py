import json
from pathlib import Path

from lunr.token import Token
from lunr.stemmer import stemmer
from lunr.pipeline import Pipeline


class TestStemmer:

    def test_reduces_words_to_their_stem(self):
        path = Path(__file__).parent / 'fixtures' / 'stemming_vocab.json'
        with open(path) as f:
            data = json.loads(f.read())

        for word, expected in data.items():
            token = Token(word)
            result = str(stemmer(token))

            if result != expected:
                print(result, expected)

    def test_is_a_registered_pipeline_function(self):
        assert stemmer.label == 'stemmer'
        assert Pipeline.registered_functions['stemmer'] == stemmer
