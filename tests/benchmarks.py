from tests.utils import read_mkdocs_data

from lunr import lunr


def index_mkdocs_data(data):
    lunr(
        ref='location',
        fields=('title', 'text'),
        documents=data['docs']
    )


def test_index_mkdocs(benchmark):
    data = read_mkdocs_data()
    benchmark(index_mkdocs_data, data)
