from __future__ import unicode_literals

from builtins import open

import json
import os
import re
import subprocess

import pytest

from lunr import lunr
from tests.utils import assert_field_vectors_equal, DEFAULT_TOLERANCE


PATTERN = r'([^\ ]+) "([^\"]+)" \[([\d\.]*)\]'


def _create_mkdocs_index():
    fixture_path = os.path.join(
        os.path.dirname(__file__), 'fixtures', 'search_index.json')
    with open(fixture_path) as f:
        data = json.loads(f.read())

    return lunr(
        ref='location',
        fields=('title', 'text'),
        documents=data['docs']
    )


def _run_node_script(filename):
    js_path = os.path.join(os.path.dirname(__file__), filename)
    js_output = subprocess.check_output(['node', js_path])
    return js_output.decode().strip()


def test_mkdocs_produces_same_results():
    js_results = _run_node_script('test_mkdocs_results.js').split('\n')
    index = _create_mkdocs_index()
    results = index.search('plugins')
    assert len(results) == len(js_results)

    for js_result, result in zip(js_results, results):
        location, title, score = re.match(PATTERN, js_result).groups()
        assert result['ref'] == location
        assert result['score'] == pytest.approx(
            float(score), rel=DEFAULT_TOLERANCE)


def test_serialized_json_matches():
    json_path = _run_node_script('test_mkdocs_serialization.js')
    with open(json_path) as fd:
        js_serialized_index = fd.read()
        js_index = json.loads(js_serialized_index)

    index = _create_mkdocs_index()
    serialized_index = index.serialize()

    assert sorted(serialized_index.keys()) == sorted(js_index.keys())
    assert serialized_index['fields'] == js_index['fields']
    assert len(
        serialized_index['fieldVectors']) == len(js_index['fieldVectors'])
    # TODO: contents of field vectors do not match, though results are the same
    # TODO: missing `invertedIndex`
