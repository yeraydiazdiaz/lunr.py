from lunr.utils import CompleteSet


class TestCompleteSet:
    def test_always_contains_other_element(self):
        assert "foo" in CompleteSet()

    def test_intersection_returns_other(self):
        cs = CompleteSet({"bar"})
        assert cs.intersection({"foo"}) == {"foo"}

    def test_union_returns_self(self):
        cs = CompleteSet({"bar"})
        assert cs.union({"foo"}) == {"bar"}
