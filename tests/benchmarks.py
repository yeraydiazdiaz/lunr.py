import os.path

import pytest

from tests.utils import read_json_fixture

from lunr import lunr
from lunr.pipeline import Pipeline


def get_mkdocs_index():
    data = read_json_fixture("mkdocs_index.json")
    return lunr(ref="id", fields=("title", "text"), documents=data["docs"])


class TestSearchBenchmarks:
    @pytest.fixture(scope="session")
    def index(self):
        return get_mkdocs_index()

    def test_search(self, index, benchmark):
        benchmark(index.search, "styling")


class TestPipelineBenchmarks:

    FEW_COUNT = 50
    MANY_COUNT = 1000

    @pytest.fixture(scope="session")
    def many_tokens(self):
        path = os.path.join(os.path.dirname(__file__), "fixtures/words.txt")
        with open(path) as words:
            self.many_tokens = [
                words.readline().strip() for _ in range(self.MANY_COUNT)
            ]
        self.few_tokens = self.many_tokens[: self.FEW_COUNT]
        yield self.many_tokens

    @pytest.fixture(scope="session")
    def few_tokens(self, many_tokens):
        yield self.few_tokens

    @staticmethod
    def token_to_token(token, i, tokens):
        return token

    @staticmethod
    def token_to_token_array(token, i, tokens):
        return [token, token]

    def test_few_token_to_token(self, few_tokens, benchmark):
        token_to_token_pipeline = Pipeline()
        token_to_token_pipeline.add(self.token_to_token)
        benchmark(token_to_token_pipeline.run, few_tokens)

    def test_many_token_to_token(self, many_tokens, benchmark):
        token_to_token_pipeline = Pipeline()
        token_to_token_pipeline.add(self.token_to_token)
        benchmark(token_to_token_pipeline.run, many_tokens)

    def test_few_token_to_token_array(self, few_tokens, benchmark):
        token_to_token_array_pipeline = Pipeline()
        token_to_token_array_pipeline.add(self.token_to_token_array)
        benchmark(token_to_token_array_pipeline.run, few_tokens)

    def test_many_token_to_token_array(self, many_tokens, benchmark):
        token_to_token_array_pipeline = Pipeline()
        token_to_token_array_pipeline.add(self.token_to_token_array)
        benchmark(token_to_token_array_pipeline.run, many_tokens)


if __name__ == "__main__":
    get_mkdocs_index()
