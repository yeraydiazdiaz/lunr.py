from lunr import lunr, get_default_builder
from lunr.stemmer import stemmer
from lunr.trimmer import trimmer
from lunr.stop_word_filter import stop_word_filter

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


def test_get_default_builder():
    builder = get_default_builder()
    assert builder.pipeline._stack == [trimmer, stop_word_filter, stemmer]
    assert builder.search_pipeline._stack == [stemmer]


def test_drop_pipeline_function():
    builder = get_default_builder()
    builder.pipeline.remove(stemmer)

    idx = lunr("id", ("title", "body"), documents, builder=builder)

    assert idx.search("kill") == []  # no match because "killed" was not stemmed
