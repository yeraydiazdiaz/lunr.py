import json
import os
import re
import subprocess

import pytest

PATTERN = r'([^\ ]+) "([^\"]+)" \[([\d\.]*)\]'
DEFAULT_TOLERANCE = 1e-2


def assert_field_vectors_equal(a, b, tol=DEFAULT_TOLERANCE):
    assert a[0] == b[0]
    for x, y in zip(a[1], b[1]):
        assert x == pytest.approx(y, rel=tol)


def assert_vectors_equal(a, b, tol=DEFAULT_TOLERANCE):
    for x, y in zip(a, b):
        assert x == pytest.approx(y, rel=tol)


def assert_results_match(results, js_results, tol=DEFAULT_TOLERANCE):
    assert len(results) == len(js_results) != 0
    for js_result, result in zip(js_results, results):
        id_, title, score = re.match(PATTERN, js_result).groups()
        assert result["ref"] == id_
        assert result["score"] == pytest.approx(float(score), rel=tol)


def read_json_fixture(filename):
    fixture_path = os.path.join(
        os.path.dirname(__file__), "acceptance_tests", "fixtures", filename
    )
    with open(fixture_path) as f:
        return json.loads(f.read())


def run_node_script(filename, *args):
    js_path = os.path.join(
        os.path.dirname(__file__), "acceptance_tests", "javascript", filename
    )
    js_output = subprocess.check_output(["node", js_path] + list(args))
    return js_output.decode("utf-8").strip()
