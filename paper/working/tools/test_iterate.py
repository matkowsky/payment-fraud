"""Check the optional helper's exit-status behavior with controlled subprocesses.

This tests the helper, not the paper's research claims or its full build.
"""
from pathlib import Path
import shutil
import subprocess
import tempfile

HELPER = Path(__file__).with_name('iterate.sh')
NAME = 'MANUSCRIPT'


def case(build_status, check_status, previous=None):
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        shutil.copyfile(HELPER, root / 'iterate.sh')
        (root / 'BUILD.py').write_text(
            'from pathlib import Path\n'
            f'Path({NAME + ".md"!r}).write_text("new text\\n")\n'
            f'raise SystemExit({build_status})\n')
        (root / 'CHECK_CANDIDATE.py').write_text(
            'from pathlib import Path\n'
            'Path("checker-called").write_text("yes")\n'
            f'raise SystemExit({check_status})\n')
        args = ['sh', 'iterate.sh']
        if previous == 'different':
            (root / 'previous.md').write_text('old text\n')
            args += ['previous.md']
        elif previous == 'missing':
            args += ['missing.md']
        result = subprocess.run(args, cwd=root, capture_output=True, text=True)
        return result.returncode, (root / 'checker-called').exists()


assert case(7, 0) == (7, False), 'build failure must stop before checking'
assert case(0, 9) == (9, True), 'checker failure must reach the caller'
assert case(0, 0) == (0, True), 'successful build/check must succeed'
assert case(0, 0, 'different') == (0, True), 'a normal diff is not a failure'
assert case(0, 0, 'missing') == (2, False), 'missing comparison input must fail'
print('iterate.sh: 5 exit-status cases passed')
