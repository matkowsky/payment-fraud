#!/usr/bin/env python3
"""Agent test of the practitioner study's cases. Protocol: README.md in this folder. Standard library only.

Run from paper/working:

    python3 tools/agent_test/agent_test.py sheet [--check]
    python3 tools/agent_test/agent_test.py prompt RUN_ID
    python3 tools/agent_test/agent_test.py run --vendor openai --phase pilot --out DIR     # needs OPENAI_API_KEY
    python3 tools/agent_test/agent_test.py run --vendor anthropic --phase pilot --out DIR  # needs ANTHROPIC_API_KEY
    python3 tools/agent_test/agent_test.py score --phase pilot --replies DIR ... --key KEY.md --out DIR

`sheet` writes RUN_SHEET.csv; with --check it only compares. `run` sends the phase's sessions for one vendor,
saves each raw reply as RUN_ID.json in DIR/PHASE/, skips sessions already saved and stops at the cost cap.
`score` reads the saved replies and writes results.json and results.md. --key is the phase's answer key,
checked against its hash: the pilot key for the pilot, the practitioner study's key for the main phase.
"""
import argparse
import csv
import hashlib
import io
import json
import math
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
INSTRUMENT = HERE.parent / 'practitioner_study' / 'INSTRUMENT.md'
FILLER = HERE / 'FILLER.md'
PILOT = HERE / 'PILOT_CASE.md'
SHEET = HERE / 'RUN_SHEET.csv'

SEED = 20261117
CONDITIONS = ('case_only', 'records', 'filler')
# model -> (vendor, letter used in run ids)
MODELS = {'gpt-6.1-sol': ('openai', 'S'), 'gpt-6.1-terra': ('openai', 'T'), 'gpt-6-luna': ('openai', 'L'),
          'claude-opus-5-5': ('anthropic', 'O'), 'claude-sonnet-5-5': ('anthropic', 'N'),
          'claude-haiku-5-5': ('anthropic', 'H')}
VENDORS = {'openai': {'url': 'https://api.openai.com/v1/responses', 'key': 'OPENAI_API_KEY'},
           'anthropic': {'url': 'https://api.anthropic.com/v1/messages', 'key': 'ANTHROPIC_API_KEY'}}
SESSIONS_PER_CONDITION = {'pilot': 10, 'main': 30}
# Dollars per million tokens (input, output). OpenAI: its pricing page, read 16 November 2026.
# Anthropic: its pricing page, read 17 November 2026 (Haiku: prompts up to 100,000 tokens).
PRICES = {'gpt-6.1-sol': (2.0, 10.0), 'gpt-6.1-terra': (1.0, 5.0), 'gpt-6-luna': (0.10, 0.50),
          'claude-opus-5-5': (4.0, 20.0), 'claude-sonnet-5-5': (2.0, 10.0), 'claude-haiku-5-5': (0.10, 0.50)}
CAP_DOLLARS = 15.0  # for each vendor
MAX_OUTPUT_TOKENS = 6000
# The pilot key is kept private until the practitioner study's form closes (README, PILOT_CASE.md).
PILOT_KEY_SHA256 = 'b709ee4a4336c0a9ba961a42a185586d955dfc4b77e59d564053acf3e8b29c0b'

RECORDS_LEAD = 'These records are also available. Each record is shown as the system stores it.'
HEAD = ('{lead}\n'
        'For each question, choose one of the listed answers, word for word.\n'
        'You may reason before you answer. Then end your reply with one line in exactly this form, '
        'with each answer in place of <answer>:\n\n{template}\n')
TAIL = '\nEnd your reply with the RESULT line described at the top, starting with: RESULT {run_id} |\n'
QUESTION = re.compile(r'^([A-Z]\d)\. (.+\?) (.+)$')
RESULT_LINE = re.compile(r'^[\W_]*RESULT\s+(\S+)\s*\|(.*)$', re.M)
RUN_FILE = re.compile(r'^[PM][STLONH]-\d{3}\.json$')


# ---------- material ----------

def _section(text, start, end=None):
    i = text.index(start)
    j = text.index(end, i + len(start)) if end else len(text)
    return text[i + len(start):j]


def _bullets(block):
    return [ln for ln in block.splitlines() if ln.startswith('- ')]


def _case(block):
    """A case block from '### Case X: title' up to the next case: title, body lines, questions."""
    lines = block.strip('\n').splitlines()
    title = lines[0].lstrip('#').strip()
    body, questions = [], []
    for ln in lines[1:]:
        m = QUESTION.match(ln)
        if m:
            questions.append({'code': m.group(1), 'line': ln, 'choices': [c.strip() for c in m.group(3).split(' / ')]})
        elif not questions:
            body.append(ln)
    while body and not body[-1].strip():
        body.pop()
    while body and not body[0].strip():
        body.pop(0)
    return {'title': title, 'body': body, 'questions': questions}


def load_main():
    text = INSTRUMENT.read_text(encoding='utf-8')
    part2 = _section(text, '## Part 2', '## Part 3')
    part3 = _section(text, '## Part 3', '## Part 4')
    lead = [ln for ln in part2.splitlines()[1:] if ln.strip()][0]
    filler = FILLER.read_text(encoding='utf-8')
    cases = []
    for letter, nxt in (('A', '### Case B'), ('B', None)):
        c = _case(f'### Case {letter}' + _section(part2, f'### Case {letter}', nxt))
        c['records'] = _bullets(_section(part3, f'### Case {letter}: added records', '### Case B' if letter == 'A' else None))
        c['filler'] = _bullets(_section(filler, f'## Case {letter}', '## Case B' if letter == 'A' else None))
        cases.append(c)
    return lead, cases


def load_pilot():
    text = PILOT.read_text(encoding='utf-8')
    c = _case(_section(text, '## Case\n', '## Records'))
    c['records'] = _bullets(_section(text, '## Records', '## Filler'))
    c['filler'] = _bullets(_section(text, '## Filler', '## Key'))
    lead, _ = load_main()
    return lead, [c]


def material(phase):
    return load_pilot() if phase == 'pilot' else load_main()


def questions(phase):
    return [q for c in material(phase)[1] for q in c['questions']]


# ---------- prompts and run sheet ----------

def build_prompt(phase, condition, run_id):
    lead, cases = material(phase)
    template = f'RESULT {run_id} | ' + ' | '.join(f"{q['code']}: <answer>" for c in cases for q in c['questions'])
    out = [HEAD.format(lead=lead, template=template)]
    for c in cases:
        out += ['', c['title'], ''] + c['body']
        added = {'records': c['records'], 'filler': c['filler']}.get(condition)
        if added:
            out += ['', RECORDS_LEAD, ''] + added
        for q in c['questions']:
            out += ['', q['line']]
    out.append(TAIL.format(run_id=run_id))
    return '\n'.join(out)


def build_sheet():
    rows = []
    for phase in ('pilot', 'main'):
        for model, (_, letter) in MODELS.items():
            n = SESSIONS_PER_CONDITION[phase]
            conds = [c for c in CONDITIONS for _ in range(n)]
            random.Random(f'{SEED}:{phase}:{model}').shuffle(conds)
            for i, cond in enumerate(conds, 1):
                run_id = f"{'P' if phase == 'pilot' else 'M'}{letter}-{i:03d}"
                prompt = build_prompt(phase, cond, run_id)
                rows.append({'run_id': run_id, 'phase': phase, 'model': model, 'condition': cond, 'order': i,
                             'prompt_sha256': hashlib.sha256(prompt.encode('utf-8')).hexdigest()})
    return rows


def sheet_text(rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0]), lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def read_sheet():
    with SHEET.open(encoding='utf-8', newline='') as f:
        return {r['run_id']: r for r in csv.DictReader(f)}


# ---------- replies ----------

def canon(s):
    return re.sub(r'[\s,.;:"\'*`]+', ' ', str(s).casefold()).strip()


def parse_result(text, run_id, qs):
    """(answers by item, None) or (None, the problem). The last RESULT line in the reply counts."""
    hits = RESULT_LINE.findall(str(text or '').replace('**', '').replace('`', ''))
    if not hits:
        return None, 'no RESULT line'
    rid, rest = hits[-1]
    rid = rid.strip('<>[]*')
    if rid != run_id:
        return None, f'the RESULT line names run {rid}, not {run_id}'
    choices = {q['code']: {canon(c): c for c in q['choices']} for q in qs}
    answers = {}
    for part in rest.split('|'):
        if not part.strip():
            continue
        m = re.match(r'\s*([A-Z]\d)\s*[:=]\s*(.*?)\s*$', part)
        if not m or m.group(1) not in choices:
            return None, f'unreadable part: {part.strip()[:40]}'
        code, ans = m.groups()
        if code in answers:
            return None, f'{code} is answered twice'
        if canon(ans) not in choices[code]:
            return None, f'{code}: "{ans[:40]}" is not one of the choices'
        answers[code] = choices[code][canon(ans)]
    missing = [q['code'] for q in qs if q['code'] not in answers]
    if missing:
        return None, 'no answer for ' + ', '.join(missing)
    return answers, None


def response_text(resp):
    """The reply's text: OpenAI's Responses format (output messages) or Anthropic's Messages format (content)."""
    parts = []
    for item in resp.get('output') or []:
        if item.get('type') == 'message':
            parts += [c.get('text', '') for c in item.get('content') or [] if c.get('type') == 'output_text']
    parts += [c.get('text', '') for c in resp.get('content') or [] if c.get('type') == 'text']
    return '\n'.join(parts)


def policy_stop(resp):
    """The API's reason when its own safety system stopped the reply, else None."""
    if resp.get('stop_reason') == 'refusal':  # Anthropic
        category = (resp.get('stop_details') or {}).get('category')
        return 'refusal' + (f': {category}' if category else '')
    if resp.get('status') == 'incomplete' and (resp.get('incomplete_details') or {}).get('reason') == 'content_filter':
        return 'content_filter'  # OpenAI
    return None


def read_replies(paths):
    """run_id -> {'text', 'model_shown', 'source', 'stop', 'resent'} from the RUN_ID.json files `run` saves."""
    out = {}
    files = []
    for p in map(Path, paths):
        files += sorted(f for f in p.rglob('*') if RUN_FILE.match(f.name)) if p.is_dir() else [p]
    for f in files:
        rec = json.loads(f.read_text(encoding='utf-8'))
        rid = rec['run_id']
        if rid in out:
            raise ValueError(f"run {rid} has two replies ({out[rid]['source']}, {f})")
        out[rid] = {'text': response_text(rec['response']), 'model_shown': rec['response'].get('model'), 'source': str(f),
                    'stop': policy_stop(rec['response']), 'resent': 'stopped_reply' in rec}
    return out


# ---------- scoring ----------

def parse_key_table(text, items):
    key = {}
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) >= 4 and cells[0] in items:
            key[cells[0]] = {'supported': canon(cells[1]), 'error': canon(cells[2]), 'requirement': cells[3]}
    m = re.search(r'"Cannot tell" is also supported for ([A-Z0-9, and]+);', text)
    also = set(re.findall(r'[A-Z]\d', m.group(1))) if m else set()
    if set(key) != set(items):
        raise ValueError(f'the key lacks items {sorted(set(items) - set(key))}')
    return key, also


def main_key(path):
    sys.path.insert(0, str(HERE.parent / 'practitioner_study'))
    import score_responses as sr
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != sr.KEY_SHA256:
        raise SystemExit('answer key does not match the hash recorded before the first response')
    key, also = sr.parse_key(raw.decode('utf-8'))
    return {i: {**v, 'supported': canon(v['supported']), 'error': canon(v['error'])} for i, v in key.items()}, also


def pilot_key(path):
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != PILOT_KEY_SHA256:
        raise SystemExit('pilot key does not match the hash recorded before the pilot')
    return parse_key_table(raw.decode('utf-8'), [q['code'] for q in questions('pilot')])


def _binom_cdf(k, n, p):
    if p <= 0:
        return 1.0
    if p >= 1:
        return 0.0 if k < n else 1.0
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k + 1))


def clopper_pearson(k, n, alpha=0.05):
    """Exact two-sided interval for k successes in n trials, by bisection on the binomial tail."""
    if n == 0:
        return None
    def solve(f):
        lo, hi = 0.0, 1.0
        for _ in range(100):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if f(mid) else (lo, mid)
        return (lo + hi) / 2
    lower = 0.0 if k == 0 else solve(lambda p: 1 - _binom_cdf(k - 1, n, p) < alpha / 2)
    upper = 1.0 if k == n else solve(lambda p: _binom_cdf(k, n, p) > alpha / 2)
    return [round(lower, 4), round(upper, 4)]


def score(phase, sheet, replies, key, also):
    qs = questions(phase)
    items = [q['code'] for q in qs]
    planned = [r for r in sheet.values() if r['phase'] == phase]
    stray = sorted(set(replies) - {r['run_id'] for r in planned})
    if stray:
        raise ValueError(f'replies for runs not in this phase of the sheet: {stray}')
    res = {'phase': phase, 'models': {}}
    for model in MODELS:
        rows = [r for r in planned if r['model'] == model]
        m = res['models'][model] = {'planned': len(rows), 'run': 0, 'model_shown': {}, 'no_answer': {},
                                    'stopped': {}, 'conditions': {}}
        for cond in CONDITIONS:
            sessions = []
            for r in (r for r in rows if r['condition'] == cond):
                rep = replies.get(r['run_id'])
                if rep is None:
                    continue
                m['run'] += 1
                shown = rep.get('model_shown') or '(not recorded)'
                m['model_shown'][shown] = m['model_shown'].get(shown, 0) + 1
                ans, why = parse_result(rep['text'], r['run_id'], qs)
                if rep.get('resent') or rep.get('stop'):
                    m['stopped'][r['run_id']] = (('resent; stopped again' if rep.get('stop') else 'resent; answered')
                                                 if rep.get('resent') else f"{rep['stop']}; not resent")
                if ans is None:
                    m['no_answer'][r['run_id']] = f"stopped by the API ({rep['stop']})" if rep.get('stop') else why
                sessions.append(ans)
            n = len(sessions)
            per_item = {}
            for i in items:
                k = key[i]
                given = [canon(a[i]) for a in sessions if a]
                err = sum(a == k['error'] for a in given)
                sup = sum(a == k['supported'] or (cond != 'records' and i in also and a == 'cannot tell') for a in given)
                per_item[i] = {'requirement': k['requirement'], 'sessions': n, 'errors': err, 'supported': sup,
                               'no_answer': n - len(given), 'error_interval': clopper_pearson(err, n),
                               'answers': dict(Counter(given))}
            by_req = {}
            for i, v in per_item.items():
                req = 'Control' if v['requirement'] == 'Control' else v['requirement'].split()[0]
                agg = by_req.setdefault(req, Counter())
                for f in ('errors', 'supported', 'no_answer'):
                    agg[f] += v[f]
                agg['item_answers'] += v['sessions']
            m['conditions'][cond] = {'sessions': n, 'items': per_item, 'by_requirement': {k: dict(v) for k, v in by_req.items()}}
    if phase == 'pilot':
        # The one pre-set branch (README, "Pilot"): counted errors on P1 and P2, case only, all models pooled.
        e = n = 0
        for m in res['models'].values():
            c = m['conditions']['case_only']
            for i in ('P1', 'P2'):
                e += c['items'][i]['errors']
                n += c['items'][i]['sessions'] - c['items'][i]['no_answer']
        res['branch'] = {'case_only_requirement_answers': n, 'counted_errors': e,
                         'main_run': 'free-text conclusions' if n and e <= 0.2 * n else ('as fixed' if n else 'not decided')}
    return res


def to_markdown(res):
    names = {'case_only': 'case only', 'records': 'with records', 'filler': 'with filler'}
    out = [f"# Agent test results, {res['phase']}", '']
    if 'branch' in res:
        b = res['branch']
        out += [f"Pilot branch: {b['counted_errors']} counted errors in {b['case_only_requirement_answers']} case-only "
                f"answers to P1 and P2. Main run: {b['main_run']}.", '']
    for model, m in res['models'].items():
        out += [f'## {model}', '', f"Sessions run: {m['run']} of {m['planned']}. Model shown: "
                + (', '.join(f'{k} ({v})' for k, v in m['model_shown'].items()) or 'none') + '.', '']
        if m.get('stopped'):
            out += ["Stopped by the API's safety system: " + '; '.join(f'{k} ({v})' for k, v in m['stopped'].items()) + '.', '']
        if m['no_answer']:
            out += ['No valid RESULT line: ' + '; '.join(f'{k} ({v})' for k, v in m['no_answer'].items()) + '.', '']
        out += ['| Item | Requirement | ' + ' | '.join(f'Errors, {names[c]} (95% CI)' for c in CONDITIONS) + ' |',
                '|---|---|' + '---|' * len(CONDITIONS)]
        first = m['conditions'][CONDITIONS[0]]['items']
        for i, v in first.items():
            cells = []
            for c in CONDITIONS:
                x = m['conditions'][c]['items'][i]
                ci = x['error_interval']
                cells.append(f"{x['errors']} of {x['sessions']}" + (f' ({ci[0]:.2f} to {ci[1]:.2f})' if ci else ''))
            out.append(f"| {i} | {v['requirement']} | " + ' | '.join(cells) + ' |')
        out += ['', '| Requirement | ' + ' | '.join(f'Errors, {names[c]}' for c in CONDITIONS) + ' |',
                '|---|' + '---|' * len(CONDITIONS)]
        for req in sorted(m['conditions'][CONDITIONS[0]]['by_requirement']):
            cells = [f"{m['conditions'][c]['by_requirement'][req]['errors']} of "
                     f"{m['conditions'][c]['by_requirement'][req]['item_answers']}" for c in CONDITIONS]
            out.append(f'| {req} | ' + ' | '.join(cells) + ' |')
        out.append('')
    return '\n'.join(out) + '\n'


# ---------- APIs ----------

def cost(model, usage):
    pin, pout = PRICES[model]
    return (usage.get('input_tokens', 0) * pin + usage.get('output_tokens', 0) * pout) / 1e6


def spent(root, vendor):
    total = 0.0
    for f in Path(root).rglob('*.json'):
        if not RUN_FILE.match(f.name):
            continue
        rec = json.loads(f.read_text(encoding='utf-8'))
        model = rec.get('model_requested')
        if model in MODELS and MODELS[model][0] == vendor:
            total += cost(model, rec['response'].get('usage') or {})
            if rec.get('stopped_reply'):
                total += cost(model, rec['stopped_reply']['response'].get('usage') or {})
    return total


def worst_next(model, prompt):
    pin, pout = PRICES[model]
    return (len(prompt.encode('utf-8')) / 2 * pin + MAX_OUTPUT_TOKENS * pout) / 1e6


def request(vendor, model, prompt, api_key):
    if vendor == 'openai':
        body = {'model': model, 'input': prompt, 'max_output_tokens': MAX_OUTPUT_TOKENS, 'store': False}
        headers = {'Authorization': f'Bearer {api_key}'}
    else:
        body = {'model': model, 'max_tokens': MAX_OUTPUT_TOKENS, 'messages': [{'role': 'user', 'content': prompt}]}
        headers = {'x-api-key': api_key, 'anthropic-version': '2023-06-01'}
    headers['Content-Type'] = 'application/json'
    return urllib.request.Request(VENDORS[vendor]['url'], data=json.dumps(body).encode('utf-8'), headers=headers)


def call_api(vendor, model, prompt, api_key, tries=4):
    for t in range(tries):
        try:
            with urllib.request.urlopen(request(vendor, model, prompt, api_key), timeout=900) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503, 504, 529) or t == tries - 1:
                raise SystemExit(f'{vendor} refused the request for {model}: HTTP {e.code} {e.read()[:300]!r}')
        except (urllib.error.URLError, TimeoutError) as e:
            if t == tries - 1:
                raise SystemExit(f'no reply from {vendor} after {tries} tries: {e}')
        time.sleep(10 * 2 ** t)


def run_api(vendor, phase, out_root, api_key, models=None):
    sheet = [r for r in read_sheet().values() if r['phase'] == phase and MODELS[r['model']][0] == vendor
             and (not models or r['model'] in models)]
    sheet.sort(key=lambda r: (int(r['order']), list(MODELS).index(r['model'])))  # models take turns
    folder = Path(out_root) / phase
    folder.mkdir(parents=True, exist_ok=True)
    done = 0
    for r in sheet:
        path = folder / f"{r['run_id']}.json"
        if path.exists():
            continue
        prompt = build_prompt(phase, r['condition'], r['run_id'])
        if hashlib.sha256(prompt.encode('utf-8')).hexdigest() != r['prompt_sha256']:
            raise SystemExit(f"prompt for {r['run_id']} differs from RUN_SHEET.csv; the material has changed")
        so_far = spent(out_root, vendor)
        if so_far + worst_next(r['model'], prompt) > CAP_DOLLARS:
            print(f'stopped at the cap: about {so_far:.2f} dollars spent with {vendor}; {r["run_id"]} not sent')
            return
        sent = datetime.now(timezone.utc).isoformat(timespec='seconds')
        resp = call_api(vendor, r['model'], prompt, api_key)
        rec = {'run_id': r['run_id'], 'model_requested': r['model'], 'prompt_sha256': r['prompt_sha256'],
               'sent_at': sent, 'received_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
               'response': resp}
        stop = policy_stop(resp)
        if stop and phase == 'main':
            # README, "Pilot": a reply the API's safety system stops is resent once, to the same model.
            if so_far + cost(r['model'], resp.get('usage') or {}) + worst_next(r['model'], prompt) > CAP_DOLLARS:
                print(f"{r['run_id']} stopped by the API ({stop}); not resent: the cap")
            else:
                rec['stopped_reply'] = {'sent_at': rec['sent_at'], 'received_at': rec['received_at'], 'stop': stop,
                                        'response': resp}
                rec['sent_at'] = datetime.now(timezone.utc).isoformat(timespec='seconds')
                rec['response'] = resp = call_api(vendor, r['model'], prompt, api_key)
                rec['received_at'] = datetime.now(timezone.utc).isoformat(timespec='seconds')
        path.write_text(json.dumps(rec, indent=1) + '\n', encoding='utf-8')
        done += 1
        status = resp.get('status') or resp.get('stop_reason')
        print(f"{r['run_id']} {r['model']} {status} {cost(r['model'], resp.get('usage') or {}):.4f} dollars")
    print(f'done: {done} sent; about {spent(out_root, vendor):.2f} dollars spent with {vendor} in all')


# ---------- command line ----------

def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('sheet')
    s.add_argument('--check', action='store_true')
    s = sub.add_parser('prompt')
    s.add_argument('run_id')
    s = sub.add_parser('run')
    s.add_argument('--vendor', choices=list(VENDORS), required=True)
    s.add_argument('--phase', choices=('pilot', 'main'), required=True)
    s.add_argument('--out', required=True)
    s.add_argument('--model', action='append', choices=list(MODELS))
    s = sub.add_parser('score')
    s.add_argument('--phase', choices=('pilot', 'main'), required=True)
    s.add_argument('--replies', nargs='+', required=True)
    s.add_argument('--key', required=True)
    s.add_argument('--out', required=True)
    a = ap.parse_args(argv)
    if a.cmd == 'sheet':
        text = sheet_text(build_sheet())
        if a.check:
            if SHEET.read_text(encoding='utf-8') != text:
                raise SystemExit('RUN_SHEET.csv differs from the material; the material has changed')
            print('RUN_SHEET.csv matches the material')
        else:
            SHEET.write_text(text, encoding='utf-8')
    elif a.cmd == 'prompt':
        r = read_sheet()[a.run_id]
        print(build_prompt(r['phase'], r['condition'], a.run_id))
    elif a.cmd == 'run':
        api_key = os.environ.get(VENDORS[a.vendor]['key'])
        if not api_key:
            raise SystemExit(f"set {VENDORS[a.vendor]['key']} first")
        run_api(a.vendor, a.phase, a.out, api_key, a.model)
    elif a.cmd == 'score':
        key, also = main_key(a.key) if a.phase == 'main' else pilot_key(a.key)
        res = score(a.phase, read_sheet(), read_replies(a.replies), key, also)
        out = Path(a.out)
        out.mkdir(parents=True, exist_ok=True)
        (out / 'results.json').write_text(json.dumps(res, indent=1) + '\n', encoding='utf-8')
        (out / 'results.md').write_text(to_markdown(res), encoding='utf-8')
        print(json.dumps({m: v['run'] for m, v in res['models'].items()}))


if __name__ == '__main__':
    main()
