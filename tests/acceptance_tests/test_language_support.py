from __future__ import unicode_literals

from lunr import lunr
from tests.utils import (
    read_json_fixture, run_node_script, assert_results_match)


def test_languages_match():
    js_results = run_node_script('test_language_support.js').split('\n')
    data = read_json_fixture('lang_es.json')
    index = lunr(
        ref='id',
        fields=('title', 'text'),
        documents=data['docs'],
        language='es',
    )
    results = index.search('invento')
    # TODO: score varies widely
    assert_results_match(results, js_results, tol=1)
