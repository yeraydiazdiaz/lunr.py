import json

from lunr import lunr
from lunr.index import Index


class TestSerialization:
    def setup_method(self, method):
        documents = [
            {
                "id": "a",
                "title": "Mr. Green kills Colonel Mustard",
                "body": """Mr. Green killed Colonel Mustard in the study with the
candlestick. Mr. Green is not a very nice fellow.""",
                "word_count": 19,
            },
            {
                "id": "b",
                "title": "Plumb waters plant",
                "body": "Professor Plumb has a green plant in his study",
                "word_count": 9,
            },
            {
                "id": "c",
                "title": "Scarlett helps Professor",
                "body": """Miss Scarlett watered Professor Plumbs green plant
while he was away from his office last week.""",
                "word_count": 16,
            },
        ]

        self.idx = lunr(ref="id", fields=("title", "body"), documents=documents)

    def test_serialization(self):
        serialized_index = json.dumps(self.idx.serialize())
        loaded_index = Index.load(json.loads(serialized_index))

        assert self.idx.search("green") == loaded_index.search("green")
