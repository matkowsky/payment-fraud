"""Test for tools/prior_work_search. Run from paper/working: python3 tools/test_prior_work_search.py"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'prior_work_search'))
import strings as st


def test_strings_are_current_and_within_limits():
    js, md = st.build()
    assert (st.HERE / 'strings.json').read_text(encoding='utf-8') == js
    assert (st.HERE / 'STRINGS.md').read_text(encoding='utf-8') == md
    d = json.loads(js)
    assert len(d['runs']) == 22 and len(d['cited_by']) == 8
    assert all('*' not in r['string'] for r in d['runs'] if r['database'] == 'IEEE Xplore')


if __name__ == '__main__':
    test_strings_are_current_and_within_limits()
    print('1 test passed')
