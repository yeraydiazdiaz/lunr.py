from lunr import lunr


class BaseTestSearch:

    def setup_method(self, method):
        documents = [{
            'id': 'a',
            'title': 'Mr. Green kills Colonel Mustard',
            'body': """Mr. Green killed Colonel Mustard in the study with the
candlestick. Mr. Green is not a very nice fellow.""",
            'word_count': 19
        }, {
            'id': 'b',
            'title': 'Plumb waters plant',
            'body': 'Professor Plumb has a green plant in his study',
            'word_count': 9
        }, {
            'id': 'c',
            'title': 'Scarlett helps Professor',
            'body': """Miss Scarlett watered Professor Plumbs green plant
while he was away from his office last week.""",
            'word_count': 16
        }]
        self.idx = lunr(
            ref='id',
            fields=('title', 'body'),
            documents=documents
        )


class TestSingleTermSearch(BaseTestSearch):

    def test_one_match(self):
        results = self.idx.search('scarlett')
        assert len(results) == 1
        assert results[0]['ref'] == 'c'
        assert list(
            results[0]['match_data'].metadata.keys()) == ['scarlett']

    def test_no_match(self):
        results = self.idx.search('foo')
        assert len(results) == 0

    def test_multiple_matches_sorts_by_relevance(self):
        results = self.idx.search('plant')
        assert len(results) == 2
        assert results[0]['ref'] == 'b'
        assert results[1]['ref'] == 'c'

    def test_pipeline_processing_enabled(self):
        results = self.idx.query(lambda q: q.clause({
            'term': 'study',  # stemmed to studi
            'use_pipeline': True
        }))

        assert len(results) == 2
        assert results[0]['ref'] == 'b'
        assert results[1]['ref'] == 'a'

    def test_pipeline_processing_disabled(self):
        results = self.idx.query(lambda q: q.clause({
            'term': 'study',  # stemmed to studi
            'use_pipeline': False
        }))

        assert len(results) == 0
