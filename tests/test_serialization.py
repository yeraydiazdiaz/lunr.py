import json

from lunr import lunr, get_default_builder
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


class TestSerializationWithTrimmer:
    def test_serialization_with_trimmer(self):
        builder = get_default_builder(trimmer_in_search=True)
        idx = lunr(
            ref="id",
            fields=["title", "body"],
            documents=[
                {
                    "id": "1",
                    "title": "To be or not to be?",
                    "body": "That is the question!",
                }
            ],
            builder=builder,
        )
        serialized_index = json.dumps(idx.serialize())
        loaded_index = Index.load(json.loads(serialized_index))

        assert idx.search("What is the question?") == loaded_index.search(
            "What is the question?"
        )

    def test_multi_serialization_with_trimmer(self):
        builder = get_default_builder(["es", "it"], trimmer_in_search=True)
        idx = lunr(
            ref="id",
            fields=["title", "text"],
            documents=[
                {
                    "id": "a",
                    "text": (
                        "Este es un ejemplo inventado de lo que sería un documento en el "
                        "idioma que se más se habla en España."
                    ),
                    "title": "Ejemplo de documento en español",
                },
            ],
            builder=builder,
        )
        serialized_index = json.dumps(idx.serialize())
        loaded_index = Index.load(json.loads(serialized_index))
        assert idx.search("inventado") == loaded_index.search(
            "inventado"
        )
        assert idx.search("inventado?") == loaded_index.search(
            "inventado?"
        )
        assert idx.search("inventado!") == loaded_index.search(
            "inventado!"
        )
