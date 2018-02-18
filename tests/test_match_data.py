from lunr.match_data import MatchData


class TestMatchData:

    def setup_method(self, method):
        self.match = MatchData('foo', 'title', {'position': [1]})
        self.match.combine(
            MatchData('bar', 'title', {'position': [2]}))
        self.match.combine(
            MatchData('baz', 'body', {'position': [3]}))
        self.match.combine(
            MatchData('baz', 'body', {'position': [4]}))

    def test_combine_terms(self):
        assert list(self.match.metadata.keys()) == ['foo', 'bar', 'baz']

    def test_combine_metadata(self):
        assert self.match.metadata['foo']['title']['position'] == [1]
        assert self.match.metadata['bar']['title']['position'] == [2]
        assert self.match.metadata['baz']['body']['position'] == [3, 4]

    def test_combine_does_not_mutate_source_data(self):
        metadata = {'foo': [1]}
        match_data1 = MatchData('foo', 'title', metadata)
        match_data2 = MatchData('foo', 'title', metadata)

        match_data1.combine(match_data2)

        assert metadata['foo'] == [1]
