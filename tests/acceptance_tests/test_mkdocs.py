from __future__ import unicode_literals

from builtins import open

import json
import os
import re
import subprocess
import tempfile

import pytest

from lunr import lunr
from lunr.index import Index
from tests.utils import DEFAULT_TOLERANCE


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


def _run_node_script(filename, *args):
    js_path = os.path.join(os.path.dirname(__file__), filename)
    js_output = subprocess.check_output(['node', js_path] + list(args))
    return js_output.decode().strip()


def _assert_results_match(results, js_results):
    assert len(results) == len(js_results)
    for js_result, result in zip(js_results, results):
        location, title, score = re.match(PATTERN, js_result).groups()
        assert result['ref'] == location
        assert result['score'] == pytest.approx(
            float(score), rel=DEFAULT_TOLERANCE)


def test_mkdocs_produces_same_results():
    js_results = _run_node_script('test_mkdocs_results.js').split('\n')
    index = _create_mkdocs_index()
    results = index.search('plugins')
    _assert_results_match(results, js_results)


def test_js_serialized_index_can_be_loaded_and_produces_same_results():
    json_path = _run_node_script('test_mkdocs_serialization.js')
    with open(json_path) as fd:
        js_serialized_index = fd.read()

    index = Index.load(js_serialized_index)
    results = index.search('plugins')
    js_results = _run_node_script('test_mkdocs_results.js').split('\n')
    _assert_results_match(results, js_results)


def test_serialized_index_can_be_loaded_in_js_and_produces_same_results():
    index = _create_mkdocs_index()
    results = index.search('plugins')
    serialized_index = index.serialize()

    with tempfile.NamedTemporaryFile(delete=False) as fp:
        fp.write(json.dumps(serialized_index).encode())

    js_results = _run_node_script(
        'test_mkdocs_load_serialized_index.js', fp.name).split('\n')
    _assert_results_match(results, js_results)
