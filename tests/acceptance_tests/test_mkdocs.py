from __future__ import unicode_literals

from builtins import open

import json
import tempfile

from lunr import lunr
from lunr.index import Index
from tests.utils import (
    read_json_fixture, run_node_script, assert_results_match)


def test_mkdocs_produces_same_results():
    js_results = run_node_script('test_mkdocs_results.js').split('\n')
    data = read_json_fixture('mkdocs_index.json')
    index = lunr(
        ref='id',
        fields=('title', 'text'),
        documents=data['docs']
    )
    results = index.search('plugins')
    assert_results_match(results, js_results)


def test_js_serialized_index_can_be_loaded_and_produces_same_results():
    json_path = run_node_script('test_mkdocs_serialization.js')
    with open(json_path) as fd:
        js_serialized_index = fd.read()

    index = Index.load(js_serialized_index)
    results = index.search('plugins')
    js_results = run_node_script('test_mkdocs_results.js').split('\n')
    assert_results_match(results, js_results)


def test_serialized_index_can_be_loaded_in_js_and_produces_same_results():
    data = read_json_fixture('mkdocs_index.json')
    index = lunr(
        ref='id',
        fields=('title', 'text'),
        documents=data['docs']
    )
    results = index.search('plugins')
    serialized_index = index.serialize()

    with tempfile.NamedTemporaryFile(delete=False) as fp:
        fp.write(json.dumps(serialized_index).encode())

    js_results = run_node_script(
        'test_mkdocs_load_serialized_index.js', fp.name).split('\n')
    assert_results_match(results, js_results)
