from __future__ import unicode_literals

from builtins import open
import six

import json
import os
import re
import subprocess

import pytest

from lunr import lunr

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


def test_mkdocs_produces_same_results():
    js_path = os.path.join(os.path.dirname(__file__), 'test_mkdocs.js')
    js_output = subprocess.check_output(['node', js_path])
    js_results = js_output.decode().strip().split('\n')

    index = _create_mkdocs_index()
    results = index.search('plugins')
    assert len(results) == len(js_results)
    if six.PY2:
        # TODO: in Python 2.7 scores below 0.14 are returned in different order
        results = results[:10]

    for js_result, result in zip(js_results, results):
        location, title, score = re.match(PATTERN, js_result).groups()
        assert result['ref'] == location
        assert pytest.approx(result['score'], float(score))
