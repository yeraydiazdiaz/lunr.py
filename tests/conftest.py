import pytest

from lunr import lunr


@pytest.fixture
def documents():
    return [
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


@pytest.fixture
def index(documents):
    return lunr(ref="id", fields=("title", "body"), documents=documents)
