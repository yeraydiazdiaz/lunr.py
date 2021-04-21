from lunr import lunr, get_default_builder
from lunr.pipeline import Pipeline
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


def test_add_token_metadata():
    builder = get_default_builder()

    def token_length(token, i, tokens):
        token.metadata["token_length"] = len(str(token))
        return token

    Pipeline.register_function(token_length)
    builder.pipeline.add(token_length)
    builder.metadata_whitelist.append("token_length")

    idx = lunr("id", ("title", "body"), documents, builder=builder)

    [result, _, _] = idx.search("green")
    assert result["match_data"].metadata["green"]["title"]["token_length"] == [5]
    assert result["match_data"].metadata["green"]["body"]["token_length"] == [5, 5]
