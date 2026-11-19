"""Tests for agent_test.py. Run from paper/working: python3 tools/agent_test/test_agent_test.py"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agent_test as at  # noqa: E402


# A made-up key for these tests. It is not the pilot's key, which is private until the form closes.
TEST_KEY = ('| P1 | Yes | No | C2 first |\n| P2 | Yes | No | C2 second |\n| P3 | Yes | No | Control |\n\n'
            '"Cannot tell" is also supported for P2; made up.\n')


def result_line(run_id, answers):
    return f'RESULT {run_id} | ' + ' | '.join(f'{k}: {v}' for k, v in answers.items())


class Material(unittest.TestCase):
    def test_sheet_is_fixed(self):
        self.assertEqual(at.SHEET.read_text(encoding='utf-8'), at.sheet_text(at.build_sheet()))

    def test_sheet_counts(self):
        rows = at.build_sheet()
        self.assertEqual(len(rows), 720)
        self.assertEqual(len({r['run_id'] for r in rows}), 720)
        for phase, n in at.SESSIONS_PER_CONDITION.items():
            for model in at.MODELS:
                for cond in at.CONDITIONS:
                    got = sum(r['phase'] == phase and r['model'] == model and r['condition'] == cond for r in rows)
                    self.assertEqual(got, n, (phase, model, cond))

    def test_main_material(self):
        lead, cases = at.load_main()
        self.assertEqual(lead, 'Answer from what is shown. "Cannot tell" is a valid answer.')
        self.assertEqual([q['code'] for c in cases for q in c['questions']],
                         [f'A{i}' for i in range(1, 6)] + [f'B{i}' for i in range(1, 7)])
        self.assertEqual([len(c['records']) for c in cases], [4, 5])
        self.assertEqual([len(c['filler']) for c in cases], [4, 5])
        a3 = cases[0]['questions'][2]
        self.assertEqual(a3['choices'], ['Yes', 'No, not by itself', 'Cannot tell'])

    def test_pilot_material(self):
        _, cases = at.load_pilot()
        self.assertEqual([q['code'] for q in cases[0]['questions']], ['P1', 'P2', 'P3'])
        self.assertEqual((len(cases[0]['records']), len(cases[0]['filler'])), (2, 2))

    def test_prompts_by_condition(self):
        _, cases = at.load_main()
        text = at.INSTRUMENT.read_text(encoding='utf-8')
        part2 = at._section(text, '## Part 2', '## Part 3')
        p = {c: at.build_prompt('main', c, 'MX-001') for c in at.CONDITIONS}
        for ln in part2.splitlines():
            if ln.startswith('- ') or at.QUESTION.match(ln):
                for c in at.CONDITIONS:
                    self.assertIn(ln, p[c])
        records = [r for c in cases for r in c['records']]
        filler = [r for c in cases for r in c['filler']]
        self.assertNotIn(at.RECORDS_LEAD, p['case_only'])
        self.assertTrue(all(r in p['records'] for r in records))
        self.assertFalse(any(r in p['records'] for r in filler))
        self.assertTrue(all(r in p['filler'] for r in filler))
        self.assertFalse(any(r in p['filler'] for r in records))
        self.assertFalse(any(r in p['case_only'] for r in records + filler))


class Parsing(unittest.TestCase):
    qs = at.questions('pilot')

    def test_valid_with_markup_and_reasoning(self):
        text = 'Reasoning here.\n\n**RESULT PS-001 | P1: Cannot tell | P2: no | P3: Yes.**'
        self.assertEqual(at.parse_result(text, 'PS-001', self.qs), ({'P1': 'Cannot tell', 'P2': 'No', 'P3': 'Yes'}, None))

    def test_last_line_counts(self):
        text = 'RESULT PS-001 | P1: Yes | P2: Yes | P3: Yes\nOn reflection:\nRESULT PS-001 | P1: Cannot tell | P2: No | P3: Yes'
        self.assertEqual(at.parse_result(text, 'PS-001', self.qs)[0]['P1'], 'Cannot tell')

    def test_problems(self):
        good = {'P1': 'Yes', 'P2': 'No', 'P3': 'Yes'}
        self.assertEqual(at.parse_result('no line', 'PS-001', self.qs), (None, 'no RESULT line'))
        self.assertIn('names run', at.parse_result(result_line('PS-002', good), 'PS-001', self.qs)[1])
        self.assertIn('no answer for P3', at.parse_result('RESULT PS-001 | P1: Yes | P2: No', 'PS-001', self.qs)[1])
        self.assertIn('not one of the choices', at.parse_result(result_line('PS-001', {**good, 'P2': 'Maybe'}), 'PS-001', self.qs)[1])
        self.assertIn('twice', at.parse_result('RESULT PS-001 | P1: Yes | P1: No | P2: No | P3: Yes', 'PS-001', self.qs)[1])

    def test_comma_choice(self):
        qs = at.questions('main')
        ans = {q['code']: q['choices'][0] for q in qs}
        ans['A3'] = 'No not by itself'
        got, why = at.parse_result(result_line('MS-001', ans), 'MS-001', qs)
        self.assertIsNone(why)
        self.assertEqual(got['A3'], 'No, not by itself')


class Scoring(unittest.TestCase):
    def test_clopper_pearson(self):
        self.assertEqual(at.clopper_pearson(0, 10), [0.0, 0.3085])
        self.assertEqual(at.clopper_pearson(5, 10), [0.1871, 0.8129])
        self.assertEqual(at.clopper_pearson(10, 10), [0.6915, 1.0])
        self.assertIsNone(at.clopper_pearson(0, 0))

    def pilot_replies(self, case_only_p1):
        sheet = at.read_sheet()
        replies = {}
        for rid, r in sheet.items():
            if r['phase'] != 'pilot':
                continue
            ans = {'P1': 'Yes', 'P2': 'Yes', 'P3': 'Yes'}
            if r['condition'] == 'case_only':
                ans['P1'] = case_only_p1
            replies[rid] = {'text': result_line(rid, ans), 'model_shown': r['model'], 'source': 'test'}
        return sheet, replies

    def test_pilot_counts_and_branch(self):
        key, also = at.parse_key_table(TEST_KEY, ['P1', 'P2', 'P3'])
        self.assertEqual(also, {'P2'})
        sheet, replies = self.pilot_replies('No')
        res = at.score('pilot', sheet, replies, key, also)
        sol = res['models']['gpt-6.1-sol']['conditions']
        self.assertEqual(sol['case_only']['items']['P1']['errors'], 10)
        self.assertEqual(sol['records']['items']['P1']['errors'], 0)
        self.assertEqual(sol['case_only']['by_requirement']['C2']['item_answers'], 20)
        self.assertEqual(res['branch']['counted_errors'], 60)          # 6 models x 10 sessions, P1 only
        self.assertEqual(res['branch']['case_only_requirement_answers'], 120)
        self.assertEqual(res['branch']['main_run'], 'as fixed')
        sheet, replies = self.pilot_replies('Yes')
        self.assertEqual(at.score('pilot', sheet, replies, key, also)['branch']['main_run'], 'free-text conclusions')
        self.assertIn('| P1 | C2 first |', at.to_markdown(res))

    def test_no_answer_and_stray(self):
        key, also = at.parse_key_table(TEST_KEY, ['P1', 'P2', 'P3'])
        sheet = at.read_sheet()
        res = at.score('pilot', sheet, {'PL-001': {'text': 'I cannot answer.', 'source': 't'}}, key, also)
        self.assertEqual(res['models']['gpt-6-luna']['no_answer'], {'PL-001': 'no RESULT line'})
        with self.assertRaises(ValueError):
            at.score('pilot', sheet, {'MS-001': {'text': '', 'source': 't'}}, key, also)

    def test_policy_stop(self):
        self.assertEqual(at.policy_stop({'stop_reason': 'refusal', 'stop_details': {'category': 'reasoning_extraction'}}),
                         'refusal: reasoning_extraction')
        self.assertEqual(at.policy_stop({'status': 'incomplete', 'incomplete_details': {'reason': 'content_filter'}}),
                         'content_filter')
        self.assertIsNone(at.policy_stop({'status': 'incomplete', 'incomplete_details': {'reason': 'max_output_tokens'}}))
        self.assertIsNone(at.policy_stop({'stop_reason': 'end_turn'}))
        self.assertIsNone(at.policy_stop({'status': 'completed'}))

    def test_stop_is_reported_apart(self):
        key, also = at.parse_key_table(TEST_KEY, ['P1', 'P2', 'P3'])
        sheet = at.read_sheet()
        replies = {'PN-025': {'text': 'reasoning cut off', 'source': 't', 'stop': 'refusal: x', 'resent': False},
                   'PN-026': {'text': result_line('PN-026', {'P1': 'Yes', 'P2': 'Yes', 'P3': 'Yes'}), 'source': 't',
                              'stop': None, 'resent': True}}
        res = at.score('pilot', sheet, replies, key, also)
        m = res['models']['claude-sonnet-5-5']
        self.assertEqual(m['no_answer'], {'PN-025': 'stopped by the API (refusal: x)'})
        self.assertEqual(m['stopped'], {'PN-025': 'refusal: x; not resent', 'PN-026': 'resent; answered'})
        self.assertIn("Stopped by the API's safety system: PN-025", at.to_markdown(res))

    def test_resend_once_in_main_only(self):
        usage = {'input_tokens': 10, 'output_tokens': 10}
        stopped = {'stop_reason': 'refusal', 'stop_details': {'category': 'x'}, 'content': [], 'usage': usage}
        ok = {'stop_reason': 'end_turn', 'content': [{'type': 'text', 'text': 'fine'}], 'usage': usage}
        calls = []
        real = at.call_api
        at.call_api = lambda *a, **k: calls.append(a) or (stopped if len(calls) == 1 else ok)
        try:
            with tempfile.TemporaryDirectory() as d:
                at.run_api('anthropic', 'main', d, 'k', ['claude-haiku-5-5'])
                n = sum(1 for r in at.read_sheet().values() if r['phase'] == 'main' and r['model'] == 'claude-haiku-5-5')
                self.assertEqual(len(calls), n + 1)
                recs = [json.loads(f.read_text(encoding='utf-8')) for f in (Path(d) / 'main').glob('*.json')]
                resent = [r for r in recs if 'stopped_reply' in r]
                self.assertEqual(len(resent), 1)
                self.assertEqual(resent[0]['stopped_reply']['stop'], 'refusal: x')
                self.assertEqual(resent[0]['response'], ok)
                self.assertAlmostEqual(at.spent(d, 'anthropic'), (n + 1) * at.cost('claude-haiku-5-5', usage))
                self.assertTrue(at.read_replies([d])[resent[0]['run_id']]['resent'])
                calls.clear()
                at.run_api('anthropic', 'pilot', d, 'k', ['claude-haiku-5-5'])  # the pilot is not resent
                self.assertEqual(len(calls), 30)
        finally:
            at.call_api = real

    def test_pilot_key_hash(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / 'key.md'
            f.write_text(TEST_KEY, encoding='utf-8')
            with self.assertRaises(SystemExit):
                at.pilot_key(f)
        self.assertNotIn('| P1 |', at.PILOT.read_text(encoding='utf-8'))  # the key is not in the repository
        self.assertIn(at.PILOT_KEY_SHA256, at.PILOT.read_text(encoding='utf-8'))

    def test_main_key_hash(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / 'key.md'
            f.write_text('| A1 | Yes | No | C1 |\n', encoding='utf-8')
            with self.assertRaises(SystemExit):
                at.main_key(f)

    def test_read_replies(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / 'pilot').mkdir()
            (d / 'pilot' / 'PS-001.json').write_text(json.dumps({'run_id': 'PS-001', 'response': {
                'model': 'gpt-6.1-sol-2026-10-01', 'output': [{'type': 'reasoning'}, {'type': 'message', 'content': [
                    {'type': 'output_text', 'text': 'RESULT PS-001 | P1: Yes | P2: No | P3: Yes'}]}]}}), encoding='utf-8')
            (d / 'pilot' / 'results.json').write_text('{}', encoding='utf-8')
            got = at.read_replies([d])
            self.assertEqual(set(got), {'PS-001'})
            self.assertEqual(got['PS-001']['model_shown'], 'gpt-6.1-sol-2026-10-01')
            self.assertTrue(got['PS-001']['text'].startswith('RESULT'))
            with self.assertRaises(ValueError):
                at.read_replies([d, d / 'pilot' / 'PS-001.json'])


class Apis(unittest.TestCase):
    def test_cost(self):
        self.assertAlmostEqual(at.cost('gpt-6.1-sol', {'input_tokens': 1_000_000, 'output_tokens': 100_000}), 3.0)
        self.assertAlmostEqual(at.cost('claude-opus-5-5', {'input_tokens': 1_000_000, 'output_tokens': 100_000}), 6.0)

    def test_anthropic_text(self):
        resp = {'model': 'claude-haiku-5-5', 'content': [{'type': 'text', 'text': 'RESULT PH-001 | P1: Yes'}]}
        self.assertEqual(at.response_text(resp), 'RESULT PH-001 | P1: Yes')

    def test_requests(self):
        o = at.request('openai', 'gpt-6-luna', 'hi', 'k')
        self.assertEqual(o.full_url, 'https://api.openai.com/v1/responses')
        self.assertEqual(json.loads(o.data)['store'], False)
        a = at.request('anthropic', 'claude-haiku-5-5', 'hi', 'k')
        self.assertEqual(a.full_url, 'https://api.anthropic.com/v1/messages')
        self.assertEqual(json.loads(a.data)['messages'], [{'role': 'user', 'content': 'hi'}])
        self.assertEqual(a.get_header('X-api-key'), 'k')

    def test_cap_is_per_vendor(self):
        calls = []
        real = at.call_api
        at.call_api = lambda *a, **k: calls.append(a) or {'status': 'completed', 'usage': {}}
        try:
            with tempfile.TemporaryDirectory() as d:
                (Path(d) / 'pilot').mkdir()
                (Path(d) / 'pilot' / 'PS-099.json').write_text(json.dumps({
                    'run_id': 'PS-099', 'model_requested': 'gpt-6.1-sol',
                    'response': {'usage': {'input_tokens': 0, 'output_tokens': 1_495_000}}}), encoding='utf-8')
                at.run_api('openai', 'pilot', d, 'k', ['gpt-6.1-sol'])
                self.assertEqual(calls, [])
                at.run_api('openai', 'pilot', d, 'k', ['gpt-6-luna'])
                self.assertEqual(len(calls), 30)
                at.run_api('anthropic', 'pilot', d, 'k', ['claude-haiku-5-5'])
                self.assertEqual(len(calls), 60)
                self.assertTrue(all(c[0] == 'anthropic' for c in calls[30:]))
        finally:
            at.call_api = real


if __name__ == '__main__':
    unittest.main()
