import pytest

DEFAULT_TOLERANCE = 1e-2


def assert_field_vectors_equal(a, b, tol=DEFAULT_TOLERANCE):
    assert a[0] == b[0]
    for x, y in zip(a[1], b[1]):
        assert x == pytest.approx(y, rel=tol)


def assert_vectors_equal(a, b, tol=DEFAULT_TOLERANCE):
    for x, y in zip(a, b):
        assert x == pytest.approx(y, rel=tol)
