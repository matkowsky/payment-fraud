"""Synchronize draft labels after a verified merge; never publish a release."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import subprocess
import urllib.request

PACKAGE = Path(__file__).resolve().parents[1]
MANIFEST = 'MANIFEST_SHA256.txt'
LABELS = {
    'proposed': 'Proposed revision for version {version} · Not accepted or published',
    'accepted': 'Accepted working draft for version {version} · Not published',
}


def read_state(package=PACKAGE):
    state = json.loads((package / 'REVISION_STATUS.json').read_text())
    if state['status'] not in LABELS:
        raise ValueError('Unknown revision status')
    if not re.fullmatch(r'\d+\.\d+', state['version']):
        raise ValueError('Invalid version')
    if not isinstance(state.get('drafting_credit'), str) or not state['drafting_credit'].strip():
        raise ValueError('The actual drafting contribution must be recorded')
    if type(state['proposal_pr']) is not int or state['proposal_pr'] <= 1:
        raise ValueError('A manuscript proposal PR is required; review-only PR #1 is excluded')
    if state['status'] == 'accepted' and (not re.fullmatch(r'[0-9a-f]{40}', state.get('merge_commit_sha', ''))
                                        or not state.get('merged_at') or not state.get('merged_by')):
        raise ValueError('Accepted status requires merge attribution')
    return state


def validate_merge(pr, state, repository, head, ref):
    """Require the actual merged PR and exact checked-out merge commit."""
    if ref != 'refs/heads/main':
        raise ValueError('Acceptance automation runs only on main')
    if pr.get('number') != state['proposal_pr'] or not pr.get('merged'):
        raise ValueError('Configured proposal has not been merged')
    if pr.get('base', {}).get('ref') != 'main' or pr['base']['repo']['full_name'] != repository:
        raise ValueError('Merge targets a different repository or branch')
    if pr.get('merge_commit_sha') != head:
        raise ValueError('Checked-out commit is not the proposal merge commit')
    if not pr.get('merged_at') or not (pr.get('merged_by') or {}).get('login'):
        raise ValueError('Merge attribution is missing')
    return {
        **state,
        'status': 'accepted',
        'merge_commit_sha': head,
        'merged_at': pr['merged_at'],
        'merged_by': pr['merged_by']['login'],
    }


def sync_labels(state, package=PACKAGE):
    label = LABELS[state['status']].format(**state)
    edits = {}
    pattern = r'(?:Proposed revision for version \d+\.\d+ · Not accepted or published|Accepted working draft for version \d+\.\d+ · Not published)'
    for name in ('manuscript', 'supplement'):
        path = package / 'SOURCE' / (name + '.md')
        text, count = re.subn(pattern, lambda _: label, path.read_text())
        if count != 1:
            raise ValueError('Expected exactly one status line in ' + str(path))
        edits[path] = text
    status = '**Status: ' + ('proposed for review; not accepted or published.' if state['status'] == 'proposed' else 'accepted working draft; not published.') + '**'
    readme = package / 'README.md'
    text, count = re.subn(r'<!-- revision-status -->.*?<!-- /revision-status -->',
                         '<!-- revision-status -->\n' + status + '\n<!-- /revision-status -->',
                         readme.read_text(), flags=re.S)
    if count != 1:
        raise ValueError('README status marker is missing or duplicated')
    edits[readme] = text
    details = ('# Working manuscript status\n\n' + status + '\n\n'
               'Proposal: [PR #' + str(state['proposal_pr']) + '](https://github.com/matkowsky/payment-fraud/pull/' + str(state['proposal_pr']) + ').\n\n')
    if state['status'] == 'accepted':
        details += ('Merged by GitHub account **' + state['merged_by'] + '** at ' + state['merged_at'] + '.\n\n'
                    'Accepted merge commit: `' + state['merge_commit_sha'] + '`.\n\n')
    details += (state['drafting_credit'] + ' '
                'Technical checks are recorded separately in PROPOSAL.md. '
                'This status does not establish independent review, empirical validation or publication.\n\n'
                'After a verified merge into main, GitHub Actions synchronizes these labels, rebuilds both documents, '
                'runs the checks and refreshes the package manifest. A failed run leaves the last committed files intact; '
                'the PR merge record remains the authority for acceptance. A versioned publication is separate.\n')
    edits[package / 'STATUS.md'] = details
    edits[package / 'REVISION_STATUS.json'] = json.dumps(state, indent=2) + '\n'
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


def check_package(package=PACKAGE):
    state = read_state(package)
    proposal = os.environ.get('PROPOSAL_NUMBER')
    if proposal is not None and (state['status'] != 'proposed' or state['proposal_pr'] != int(proposal)):
        raise ValueError('A proposal must identify its own PR and retain proposed status until merge')
    label = LABELS[state['status']].format(**state)
    for name in ('SOURCE/manuscript.md', 'SOURCE/supplement.md', 'MANUSCRIPT.md', 'SUPPLEMENT.md'):
        if label not in (package / name).read_text():
            raise ValueError('Stale document status: ' + name)
    expected = dict(line.split('  ', 1)[::-1] for line in (package / MANIFEST).read_text().splitlines())
    actual = {p.relative_to(package).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in package_files(package)}
    if expected != actual:
        raise ValueError('Manifest mismatch')
    print('Status labels and ' + str(len(actual)) + ' manifest entries verified')


def github_get(path):
    request = urllib.request.Request('https://api.github.com/' + path, headers={
        'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
    })
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def accept():
    state = read_state()
    if os.environ.get('GITHUB_REF') != 'refs/heads/main':
        raise ValueError('Acceptance requires main')
    if state['status'] == 'accepted':
        print('Already synchronized; no changes')
        return
    repository = os.environ['GITHUB_REPOSITORY']
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    if github_get('repos/' + repository + '/branches/main')['commit']['sha'] != head:
        raise ValueError('Main advanced; refusing to overwrite newer work')
    pr = github_get('repos/' + repository + '/pulls/' + str(state['proposal_pr']))
    accepted = validate_merge(pr, state, repository, head, os.environ['GITHUB_REF'])
    sync_labels(accepted)
    with open(os.environ['GITHUB_OUTPUT'], 'a') as output:
        output.write('changed=true\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['accept', 'sync', 'manifest', 'check'])
    command = parser.parse_args().command
    if command == 'accept':
        accept()
    elif command == 'sync':
        sync_labels(read_state())
    elif command == 'manifest':
        refresh_manifest()
    else:
        check_package()
