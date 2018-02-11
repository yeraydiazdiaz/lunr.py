from math import sqrt

from lunr.vector import Vector


def _vector(*args):
    vector = Vector()
    for i, arg in enumerate(args):
        vector.insert(i, arg)
    return vector


class TestVectorPositionForIndex:

    vector = Vector([1, 'a', 2, 'b', 4, 'c', 7, 'd', 11, 'e'])

    def test_position_for_index_at_the_beggining(self):
        assert self.vector.position_for_index(0) == 0

    def test_position_for_index_at_the_end(self):
        assert self.vector.position_for_index(20) == 10

    def test_position_for_index_consecutive(self):
        assert self.vector.position_for_index(3) == 4

    def test_position_for_index_non_consecutive_gap_after(self):
        assert self.vector.position_for_index(5) == 6

    def test_position_for_index_non_consecutive_gap_before(self):
        assert self.vector.position_for_index(6) == 6

    def test_position_for_index_non_consecutive_gap_before_and_after(self):
        assert self.vector.position_for_index(9) == 8

    def test_position_for_index_duplicate_at_the_beggining(self):
        assert self.vector.position_for_index(1) == 0

    def test_position_for_index_duplicate_at_the_end(self):
        assert self.vector.position_for_index(11) == 8

    def test_position_for_index_duplicate_consecutive(self):
        assert self.vector.position_for_index(4) == 4


def test_magnitude_calculates_magnitude():
    vector = _vector(4, 5, 6)
    assert sqrt(77) == vector.magnitude
