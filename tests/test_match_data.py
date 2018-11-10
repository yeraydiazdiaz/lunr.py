from lunr.match_data import MatchData


class TestMatchData:
    def setup_method(self, method):
        self.match = MatchData("foo", "title", {"position": [1]})
        self.match.combine(MatchData("bar", "title", {"position": [2]}))
        self.match.combine(MatchData("baz", "body", {"position": [3]}))
        self.match.combine(MatchData("baz", "body", {"position": [4]}))

    def test_repr(self):
        assert repr(self.match) == '<MatchData "bar,baz,foo">'

    def test_create_empty_match_data(self):
        assert MatchData().metadata == {}

    def test_create_missing_field(self):
        assert MatchData("foo").metadata["foo"] == {}

    def test_create_missing_metadata(self):
        assert MatchData("foo", "title").metadata["foo"]["title"] == {}

    def test_combine_terms(self):
        assert sorted(list(self.match.metadata.keys())) == ["bar", "baz", "foo"]

    def test_combine_metadata(self):
        assert self.match.metadata["foo"]["title"]["position"] == [1]
        assert self.match.metadata["bar"]["title"]["position"] == [2]
        assert self.match.metadata["baz"]["body"]["position"] == [3, 4]

    def test_combine_does_not_mutate_source_data(self):
        metadata = {"foo": [1]}
        match_data1 = MatchData("foo", "title", metadata)
        match_data2 = MatchData("foo", "title", metadata)

        match_data1.combine(match_data2)

        assert metadata["foo"] == [1]

    def test_add_metadata_for_missing_term(self):
        self.match.add("spam", "title", {"position": [5]})

        assert self.match.metadata["spam"]["title"]["position"] == [5]

    def test_add_metadata_for_missing_field(self):
        self.match.add("foo", "body", {"position": [6]})

        assert self.match.metadata["foo"]["body"]["position"] == [6]

    def test_add_metadata_for_existing_term_field_and_metadata_key(self):
        self.match.add("foo", "title", {"position": [7]})

        assert self.match.metadata["foo"]["title"]["position"] == [1, 7]

    def test_add_metadata_for_existing_term_and_field_and_missing_metadata_key(self):
        self.match.add("foo", "title", {"weight": [7]})

        assert self.match.metadata["foo"]["title"] == {"position": [1], "weight": [7]}
