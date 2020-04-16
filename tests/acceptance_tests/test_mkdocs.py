import json
import tempfile

import pytest

from lunr import lunr
from lunr.index import Index
from tests.utils import read_json_fixture, run_node_script, assert_results_match


@pytest.mark.acceptance
def test_mkdocs_produces_same_results():
    query_string = "plugins"
    js_results = run_node_script("mkdocs_query.js", query_string).split("\n")
    data = read_json_fixture("mkdocs_index.json")
    index = lunr(ref="id", fields=("title", "text"), documents=data["docs"])
    results = index.search(query_string)
    assert_results_match(results, js_results)


@pytest.mark.acceptance
def test_js_serialized_index_can_be_loaded_and_produces_same_results():
    json_path = run_node_script("mkdocs_serialization.js")
    with open(json_path) as fd:
        js_serialized_index = fd.read()

    index = Index.load(js_serialized_index)
    query_string = "plugins"
    results = index.search(query_string)
    js_results = run_node_script("mkdocs_query.js", query_string).split("\n")
    assert_results_match(results, js_results)


@pytest.mark.acceptance
def test_serialized_index_can_be_loaded_in_js_and_produces_same_results():
    data = read_json_fixture("mkdocs_index.json")
    index = lunr(ref="id", fields=("title", "text"), documents=data["docs"])
    query_string = "plugins"
    results = index.search(query_string)
    serialized_index = index.serialize()

    with tempfile.NamedTemporaryFile(delete=False) as fp:
        fp.write(json.dumps(serialized_index).encode())

    js_results = run_node_script(
        "mkdocs_load_serialized_index_and_search.js", fp.name, query_string
    ).split("\n")
    assert_results_match(results, js_results)
