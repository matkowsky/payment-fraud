"""Record merged pull requests and synchronize working-draft labels; never publish a release.

Commands, run from the package root:
  sync       rewrite labels, README status and STATUS.md from REVISION_STATUS.json
  check      verify labels, the change record and the manifest (generated files included)
  check --sources
             verify the state file and source labels only; used on pull requests, where
             generated files are not rebuilt
  manifest   refresh MANIFEST_SHA256.txt
  accept     on main after a merge: find the merged pull request from the merge commit,
             verify it and record it, after any earlier merge that is not yet recorded
             (GitHub Actions only)
"""
from pathlib import Path
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request

sys.path.insert(0, str(Path(__file__).resolve().parent))
import changes_since  # noqa: E402

PACKAGE = Path(__file__).resolve().parents[1]
MANIFEST = 'MANIFEST_SHA256.txt'
REPO_URL = 'https://github.com/matkowsky/payment-fraud'
LABELS = {
    'proposed': 'Proposed revision for version {version} · Not accepted or published',
    'accepted': 'Accepted working draft for version {version} · Not published',
}
STATUS_LINE = (r'(?:Proposed revision for version \d+\.\d+ · Not accepted or published'
               r'|Accepted working draft for version \d+\.\d+ · Not published)')
DATE = r'\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}'
CREDIT_LINE = re.compile(r'^[ \t>*_-]*Drafting contribution:[ \t*_]*(\S[^\n]{0,298})$', re.M | re.I)


def read_state(package=PACKAGE):
    state = json.loads((package / 'REVISION_STATUS.json').read_text())
    if state['status'] not in LABELS:
        raise ValueError('Unknown revision status')
    if not re.fullmatch(r'\d+\.\d+', state['version']):
        raise ValueError('Invalid version')
    if 'drafting_credit' in state and (not isinstance(state['drafting_credit'], str)
                                       or not state['drafting_credit'].strip()):
        raise ValueError('A recorded drafting credit cannot be empty')
    accepted = state.get('accepted', [])
    if not isinstance(accepted, list):
        raise ValueError('Accepted merges must be a list')
    for entry in accepted:
        if type(entry.get('pr')) is not int or entry['pr'] <= 1:
            raise ValueError('Accepted merges must name a manuscript PR; review-only PR #1 is excluded')
        if (not re.fullmatch(r'[0-9a-f]{40}', entry.get('merge_commit_sha', ''))
                or not entry.get('merged_at') or not entry.get('merged_by') or not entry.get('credit')):
            raise ValueError('Accepted status requires merge attribution')
    if (state['status'] == 'accepted') != bool(accepted):
        raise ValueError('Status must be accepted exactly when a merge is recorded')
    return state


def credit_for(pr, state):
    """Drafting credit: the merged branch's REVISION_STATUS.json, else the PR description, else a pointer."""
    if state.get('drafting_credit'):
        return state['drafting_credit'].strip()
    match = CREDIT_LINE.search(pr.get('body') or '')
    if match and match.group(1).strip('*_ ').strip():
        return match.group(1).strip('*_ ').strip()
    return 'Recorded in PR #' + str(pr['number']) + '.'


def validate_merge(pr, state, repository, head, ref):
    """Require the actual merged PR and exact checked-out merge commit, then record it."""
    if ref != 'refs/heads/main':
        raise ValueError('Acceptance automation runs only on main')
    if type(pr.get('number')) is not int or pr['number'] <= 1:
        raise ValueError('Review-only PR #1 is never merged or accepted')
    if not pr.get('merged'):
        raise ValueError('Pull request has not been merged')
    if pr.get('base', {}).get('ref') != 'main' or pr['base']['repo']['full_name'] != repository:
        raise ValueError('Merge targets a different repository or branch')
    if pr.get('merge_commit_sha') != head:
        raise ValueError('Checked-out commit is not the pull request merge commit')
    if not pr.get('merged_at') or not (pr.get('merged_by') or {}).get('login'):
        raise ValueError('Merge attribution is missing')
    entry = {
        'pr': pr['number'],
        'title': (pr.get('title') or '').strip()[:200],
        'merge_commit_sha': head,
        'merged_at': pr['merged_at'],
        'merged_by': pr['merged_by']['login'],
        'credit': credit_for(pr, state),
    }
    recorded = {k: v for k, v in state.items() if k != 'drafting_credit'}
    recorded['status'] = 'accepted'
    recorded['accepted'] = [*state.get('accepted', []), entry]
    return recorded


def find_merged_pr(pulls, head):
    """The one pull request merged into main whose merge produced this commit."""
    merged = [p['number'] for p in pulls
              if p.get('merged_at') and p.get('merge_commit_sha') == head
              and p.get('base', {}).get('ref') == 'main']
    if len(merged) != 1:
        raise ValueError('No single merged pull request produced this commit; '
                         'changes to paper/working reach main only by merging a pull request')
    return merged[0]


def cell(text):
    return str(text).replace('|', '\\|').replace('\n', ' ')


def draft_date(state):
    """Date of the latest accepted merge, as printed on the first page; None before any merge."""
    if not state.get('accepted'):
        return None
    when = datetime.fromisoformat(state['accepted'][-1]['merged_at'].replace('Z', '+00:00')).astimezone(timezone.utc)
    return str(when.day) + when.strftime(' %B %Y')


def sync_labels(state, package=PACKAGE):
    label = LABELS[state['status']].format(**state)
    date = draft_date(state)
    edits = {}
    for name in ('manuscript', 'supplement'):
        path = package / 'SOURCE' / (name + '.md')
        if date is None:
            text, count = re.subn(STATUS_LINE, lambda _: label, path.read_text())
        else:
            text, count = re.subn(DATE + ' · ' + STATUS_LINE, lambda _: date + ' · ' + label, path.read_text())
        if count != 1:
            raise ValueError('Expected exactly one dated status line in ' + str(path))
        edits[path] = text
    status = '**Status: ' + ('proposed for review; not accepted or published.' if state['status'] == 'proposed'
                             else 'accepted working draft; not published.') + '**'
    readme = package / 'README.md'
    text, count = re.subn(r'<!-- revision-status -->.*?<!-- /revision-status -->',
                         '<!-- revision-status -->\n' + status + '\n<!-- /revision-status -->',
                         readme.read_text(), flags=re.S)
    if count != 1:
        raise ValueError('README status marker is missing or duplicated')
    edits[readme] = text
    details = ['# Working manuscript status', '', status, '',
               'Read the current [manuscript](MANUSCRIPT.md) ([PDF](MANUSCRIPT.pdf)) and '
               '[supplement](SUPPLEMENT.md) ([PDF](SUPPLEMENT.pdf)), and see '
               '[what changed since version 1.0](' + changes_since.OUTPUT + ').', '']
    if state.get('drafting_credit'):
        details += ['Changes on this branch, not yet merged: ' + state['drafting_credit'], '']
    details += ['## Accepted merges', '']
    if state.get('accepted'):
        details += ['| Pull request | Title | Merged by GitHub account | Merged at | Merge commit | Drafting credit |',
                    '|---|---|---|---|---|---|']
        for e in state['accepted']:
            details.append('| [#' + str(e['pr']) + '](' + REPO_URL + '/pull/' + str(e['pr']) + ') | ' + cell(e['title'])
                           + ' | ' + cell(e['merged_by']) + ' | ' + cell(e['merged_at']) + ' | `' + e['merge_commit_sha']
                           + '` | ' + cell(e['credit']) + ' |')
    else:
        details.append('None yet. Open pull requests that change `paper/working/` are proposals until merged.')
    details += ['',
                'After a pull request that changes `paper/working/` is merged into main, GitHub Actions finds that pull '
                'request from the merge commit, records it above, synchronizes these labels, rebuilds both documents and '
                'the change record, runs the checks and refreshes the package manifest. A merge whose own run did not '
                'finish is recorded by the next run. A failed run leaves the last '
                'committed files intact; the merge record remains the authority for acceptance. A versioned publication is '
                'separate. Checks and reviews are recorded in each pull request. This status does not establish independent '
                'review, empirical validation or publication.', '']
    edits[package / 'STATUS.md'] = '\n'.join(details)
    edits[package / 'REVISION_STATUS.json'] = json.dumps(state, indent=2, ensure_ascii=False) + '\n'
    for path, text in edits.items():
        path.write_text(text)


def package_files(package=PACKAGE):
    return sorted(p for p in package.rglob('*') if p.is_file()
                  and not {'build', '__pycache__', '.git'}.intersection(p.relative_to(package).parts)
                  and p.name != MANIFEST and p.suffix != '.log')


def refresh_manifest(package=PACKAGE):
    (package / MANIFEST).write_text(''.join(
        hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.relative_to(package).as_posix() + '\n'
        for p in package_files(package)))


def check_package(package=PACKAGE, baseline=None, sources_only=False):
    state = read_state(package)
    label = LABELS[state['status']].format(**state)
    for name in ('SOURCE/manuscript.md', 'SOURCE/supplement.md'):
        text = (package / name).read_text()
        if re.findall(STATUS_LINE, text) != [label]:
            raise ValueError('Stale or duplicated document status: ' + name)
        if draft_date(state) and draft_date(state) + ' · ' + label not in text:
            raise ValueError('Working-draft date is not the latest merge date: ' + name)
    if sources_only:
        print('State file and source status labels verified (sources only; generated files are rebuilt after merge)')
        return
    for name in ('MANUSCRIPT.md', 'SUPPLEMENT.md'):
        if label not in (package / name).read_text():
            raise ValueError('Stale document status: ' + name)
    baseline = package.parent / 'v1.0' if baseline is None else baseline
    record = package / changes_since.OUTPUT
    if not record.is_file() or record.read_text(encoding='utf-8') != changes_since.render(package, baseline):
        raise ValueError('Stale change record: run python3 tools/changes_since.py')
    expected = dict(line.split('  ', 1)[::-1] for line in (package / MANIFEST).read_text().splitlines())
    actual = {p.relative_to(package).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in package_files(package)}
    if expected != actual:
        raise ValueError('Manifest mismatch')
    print('Status labels, change record and ' + str(len(actual)) + ' manifest entries verified')


def github_get(path):
    request = urllib.request.Request('https://api.github.com/' + path, headers={
        'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
    })
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def git(*args):
    return subprocess.run(['git', '-C', str(PACKAGE), *args], capture_output=True, text=True)


def current_head():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()


def earlier_unrecorded(head, recorded):
    """Commits on main after the last recorded merge and before head that changed this package, oldest first.

    A run stops when main has advanced, so a merge followed at once by another merge is not recorded by its
    own run. The next run finds it here. Main's own history is followed through first parents.
    """
    if not recorded:
        return []
    found = []
    walk = git('rev-list', '--first-parent', head + '^')
    if walk.returncode:
        raise ValueError('Cannot read the history of main: ' + walk.stderr.strip())
    for sha in walk.stdout.split():
        if sha in recorded:
            return found[::-1]
        changed = git('diff', '--quiet', sha + '^', sha, '--', '.').returncode
        if changed not in (0, 1):
            break  # no parent to compare with: the start of the history, or a shallow checkout
        if changed:
            found.append(sha)
    raise ValueError('No recorded merge is an ancestor of this commit; the history is incomplete')


def introduced_credit(sha):
    """The drafting_credit that this merge added to REVISION_STATUS.json, or None."""
    def credit(commit):
        shown = git('show', commit + ':./REVISION_STATUS.json')
        try:
            return json.loads(shown.stdout).get('drafting_credit') if shown.returncode == 0 else None
        except ValueError:
            return None
    here = credit(sha)
    return here if isinstance(here, str) and here.strip() and here != credit(sha + '^') else None


def accept(package=PACKAGE):
    """Record the pull request whose merge produced the checked-out commit, after any earlier merge that is
    not yet recorded. Returns True if files changed."""
    if os.environ.get('GITHUB_REF') != 'refs/heads/main':
        raise ValueError('Acceptance requires main')
    state = read_state(package)
    head = current_head()
    recorded = {e['merge_commit_sha'] for e in state.get('accepted', [])}
    if head in recorded:
        print('Already synchronized; no changes')
        return False
    repository = os.environ['GITHUB_REPOSITORY']
    if github_get('repos/' + repository + '/branches/main')['commit']['sha'] != head:
        raise ValueError('Main advanced; refusing to overwrite newer work')
    state = {k: v for k, v in state.items() if k != 'drafting_credit'}
    numbers = []
    for sha in [*earlier_unrecorded(head, recorded), head]:
        pulls = github_get('repos/' + repository + '/commits/' + sha + '/pulls')
        if sha != head and not any(p.get('merged_at') and p.get('merge_commit_sha') == sha for p in pulls):
            continue  # this workflow's own commit, or a push whose own run already failed visibly
        number = find_merged_pr(pulls, sha)
        pr = github_get('repos/' + repository + '/pulls/' + str(number))
        credit = introduced_credit(sha)
        state = validate_merge(pr, {**state, 'drafting_credit': credit} if credit else state,
                               repository, sha, os.environ['GITHUB_REF'])
        numbers.append(number)
    sync_labels(state, package)
    with open(os.environ['GITHUB_OUTPUT'], 'a') as output:
        output.write('changed=true\n')
    print('Recorded merge of PR ' + ', '.join('#' + str(n) for n in numbers))
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['accept', 'sync', 'manifest', 'check'])
    parser.add_argument('--sources', action='store_true', help='with check: verify sources only')
    args = parser.parse_args()
    if args.command == 'accept':
        accept()
    elif args.command == 'sync':
        sync_labels(read_state())
    elif args.command == 'manifest':
        refresh_manifest()
    else:
        check_package(sources_only=args.sources)
