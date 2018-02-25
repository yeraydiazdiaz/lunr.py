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

    def test_multiple_terms_all_terms_match(self):
        results = self.idx.search('fellow candlestick')

        assert len(results) == 1
        assert results[0]['ref'] == 'a'
        metadata = results[0]['match_data'].metadata
        assert list(metadata.keys()) == ['fellow', 'candlestick']
        assert list(metadata['fellow'].keys()) == ['body']
        assert list(metadata['candlestick'].keys()) == ['body']

    def test_one_term_matches(self):
        results = self.idx.search('week foo')

        assert len(results) == 1
        assert results[0]['ref'] == 'c'
        metadata = results[0]['match_data'].metadata
        assert list(metadata.keys()) == ['week']

    def test_duplicate_query_terms(self):
        self.idx.search('fellow candlestick foo bar green plant fellow')

    def test_documents_with_all_terms_score_higher(self):
        results = self.idx.search('candlestick green')

        assert len(results) == 3

        assert [r['ref'] for r in results] == ['a', 'b', 'c']
        assert list(
            results[0]['match_data'].metadata.keys()
        ) == ['candlestick', 'green']
        assert list(results[1]['match_data'].metadata.keys()) == ['green']
        assert list(results[2]['match_data'].metadata.keys()) == ['green']

    def test_no_terms_match(self):
        results = self.idx.search('foo bar')

        assert len(results) == 0

    def test_corpus_terms_are_stemmed(self):
        results = self.idx.search('water')

        assert len(results) == 2
        assert [r['ref'] for r in results] == ['b', 'c']

    def test_field_scoped_terms(self):
        results = self.idx.search('title:plant')

        assert len(results) == 1
        assert results[0]['ref'] == 'b'
        assert list(results[0]['match_data'].metadata.keys()) == ['plant']

    def test_field_scoped_no_matching_terms(self):
        results = self.idx.search('title:candlestick')

        assert len(results) == 0

    def test_wildcard_matching_no_matches(self):
        results = self.idx.search('fo*')

        assert len(results) == 0

    def test_wildcard_matching_one_match(self):
        results = self.idx.search('candle*')

        assert len(results) == 1
        assert results[0]['ref'] == 'a'
        assert list(
            results[0]['match_data'].metadata.keys()) == ['candlestick']

    def test_wildcard_matching_multiple_terms_match(self):
        results = self.idx.search('pl*')

        assert len(results) == 2

        assert [r['ref'] for r in results] == ['b', 'c']
        assert list(
            results[0]['match_data'].metadata.keys()
        ) == ['plumb', 'plant']
        assert list(
            results[1]['match_data'].metadata.keys()
        ) == ['plumb', 'plant']