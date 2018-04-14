import json
import os
import subprocess

import pytest


DEFAULT_TOLERANCE = 1e-2


def assert_field_vectors_equal(a, b, tol=DEFAULT_TOLERANCE):
    assert a[0] == b[0]
    for x, y in zip(a[1], b[1]):
        assert x == pytest.approx(y, rel=tol)


def assert_vectors_equal(a, b, tol=DEFAULT_TOLERANCE):
    for x, y in zip(a, b):
        assert x == pytest.approx(y, rel=tol)


def read_mkdocs_data():
    fixture_path = os.path.join(
        os.path.dirname(__file__),
        'acceptance_tests', 'fixtures', 'search_index.json')
    with open(fixture_path) as f:
        return json.loads(f.read())


def run_node_script(filename, *args):
    js_path = os.path.join(
        os.path.dirname(__file__), 'acceptance_tests', filename)
    js_output = subprocess.check_output(['node', js_path] + list(args))
    return js_output.decode().strip()
