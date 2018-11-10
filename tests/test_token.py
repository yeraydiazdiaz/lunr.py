from lunr.token import Token


def test_str_repr():
    token = Token("foo")
    assert str(token) == "foo"
    assert repr(token) == '<Token "foo">'


class TestMetadata:
    def test_can_attach_arbitrary_metadata(self):
        token = Token("foo", {"length": 3})
        assert token.metadata["length"] == 3

    def test_can_update_token_value(self):
        token = Token("foo", {"length": 3})
        token.update(lambda s, m: s.upper())

        assert str(token) == "FOO"

    def test_metadata_is_yielded_when_updating(self):
        # TODO: unsure what this test is asserting, a language feature?
        pass


class TestClone:
    def setup_method(self, method):
        self.token = Token("foo", {"bar": True})

    def test_clones_value(self):
        assert str(self.token) == str(self.token.clone())

    def test_clones_metadata(self):
        assert self.token.metadata == self.token.clone().metadata

    def test_clone_and_modify(self):
        clone = self.token.clone(lambda s, m: s.upper())

        assert str(clone) == "FOO"
        self.token.metadata == clone.metadata
