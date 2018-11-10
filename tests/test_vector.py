from math import sqrt

import pytest

from lunr.vector import Vector
from lunr.exceptions import BaseLunrException


def _vector_from_args(*args):
    vector = Vector()
    for i, arg in enumerate(args):
        vector.insert(i, arg)
    return vector


def test_vector_repr():
    vector = _vector_from_args(1, 3, -5)
    assert repr(vector) == "<Vector magnitude={}>".format(vector.magnitude)


class TestVectorPositionForIndex:

    vector = Vector([1, "a", 2, "b", 4, "c", 7, "d", 11, "e"])

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
    vector = _vector_from_args(4, 5, 6)
    assert sqrt(77) == vector.magnitude


def test_dot_calculates_dot_product_of_two_vectors():
    v1 = _vector_from_args(1, 3, -5)
    v2 = _vector_from_args(4, -2, -1)

    assert v1.dot(v2) == 3


class TestSimilarity:
    def test_similarity_calculates_the_similarity_between_two_vectors(self):
        v1 = _vector_from_args(1, 3, -5)
        v2 = _vector_from_args(4, -2, -1)

        assert v1.similarity(v2) == pytest.approx(0.5, 0.1)

    def test_empty_vector(self):
        v_empty = Vector()
        v1 = _vector_from_args(1)

        assert v1.similarity(v_empty) == 0
        assert v_empty.similarity(v1) == 0

    def test_non_overlapping_vector(self):
        v1 = Vector([1, 1])
        v2 = Vector([2, 1])

        assert v1.similarity(v2) == 0
        assert v2.similarity(v1) == 0


class TestVectorInsert:
    def test_insert_invalidates_magnitude_cache(self):
        vector = _vector_from_args(4, 5, 6)
        assert sqrt(77) == vector.magnitude

        vector.insert(3, 7)

        assert sqrt(126) == vector.magnitude

    def test_insert_keeps_items_in_index_specified_order(self):
        vector = Vector()

        vector.insert(2, 4)
        vector.insert(1, 5)
        vector.insert(0, 6)

        assert vector.to_list() == [6, 5, 4]

    def test_insert_fails_when_duplicate_entry(self):
        vector = _vector_from_args(4, 5, 6)
        with pytest.raises(BaseLunrException):
            vector.insert(0, 44)


class TestVectorUpsert:
    def test_upsert_invalidates_magnitude_cache(self):
        vector = _vector_from_args(4, 5, 6)
        assert vector.magnitude == sqrt(77)

        vector.upsert(3, 7)

        assert vector.magnitude == sqrt(126)

    def test_upsert_keeps_items_in_index_specified_order(self):
        vector = Vector()

        vector.upsert(2, 4)
        vector.upsert(1, 5)
        vector.upsert(0, 6)

        assert vector.to_list() == [6, 5, 4]

    def test_upsert_calls_fn_for_value_on_duplicate(self):
        vector = _vector_from_args(4, 5, 6)

        vector.upsert(0, 4, lambda current, passed: current + passed)

        assert vector.to_list() == [8, 5, 6]

    def test_upsert_defaults_to_passed_value_on_duplicate(self):
        vector = _vector_from_args(4, 5, 6)

        vector.upsert(0, 3)

        assert vector.to_list() == [3, 5, 6]
