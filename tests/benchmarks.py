from tests.utils import read_json_fixture

from lunr import lunr


def index_mkdocs_data(data):
    lunr(
        ref='id',
        fields=('title', 'text'),
        documents=data['docs']
    )


def test_index_mkdocs(benchmark):
    data = read_json_fixture('mkdocs_index.json')
    benchmark(index_mkdocs_data, data)
