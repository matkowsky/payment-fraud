#!/usr/bin/env bash
# Small, content-pinned official TeX Live runtime overlay; no system TeX changes.
# Revisions: acmart 80934, libertine 77682, inconsolata 79618,
# newtx 78101, libertinus-fonts 72484. SHA-512 verified against tlnet metadata.
# Dated 2026-11-17 snapshot, revisioned filenames and content hashes are pinned. Fail closed on
# missing/changed bytes; update pins only through review. No unpinned fallback.
set -euo pipefail
root="${RUNNER_TEMP:?}/paper-build-tools"
archives="$root/archives"
mkdir -p "$archives" "$root/texmf"
cat > "$root/SHA512SUMS" <<'HASHES'
9feecc99f903b22d8dc9535f50d625733911a1148471c2e69429f1edcf47654426892103091dcfc7d0f1660fbbf85e741060f80498c44756465a02081ae97c81  acmart.r80934.tar.xz
0c0af352a20df5a278f78d1d8de37bf0bed0988f851807e0f2b167392282179290255a3820c2c4bfc9731bf127c6dad4ea9d4d2776a70e91534dc1f90d998bc9  libertine.r77682.tar.xz
a502ec67e7a1f45a3326cd57d2fef68b642a167810e797c80c4e708bec96f481c80d79a5ab6e767f63abe68c79c267a7dbc78514decb2ed4f9735d47d43065a6  inconsolata.r79618.tar.xz
0ad536f62eba6a38da9dad5e9a14dfe931eb5c185ead490e67a959f8720944e36747e145bc30c2cb17f3b69b8bdde4f645e7022b3d76a2cd8bdd3ff1b22b1120  newtx.r78101.tar.xz
234dc32fa5b1f1c7a974444b264a1c258b7a12e1658f45146135d3f75ea8e94b4860282da79b5cdeb587c65f12d7476006d8546505c2842c306be72f51ee21df  libertinus-fonts.r72484.tar.xz
HASHES
while read -r checksum archive; do
  curl --fail --location --proto '=https' --proto-redir '=https' --retry 3 --connect-timeout 30 --max-time 180 \
    "https://texlive.info/tlnet-archive/2026/11/17/tlnet/archive/$archive" \
    --output "$archives/$archive"
done < "$root/SHA512SUMS"
(cd "$archives" && sha512sum --check "$root/SHA512SUMS")
# Reject traversal/links before extraction, even though archive bytes are pinned.
python3 - "$archives" "$root/texmf" "$root/SHA512SUMS" <<'PYTHON'
from pathlib import Path, PurePosixPath
import sys, tarfile
for line in Path(sys.argv[3]).read_text().splitlines():
    archive = Path(sys.argv[1]) / line.split()[1]
    with tarfile.open(archive) as source:
        for entry in source.getmembers():
            path = PurePosixPath(entry.name)
            if path.is_absolute() or '..' in path.parts or not (entry.isfile() or entry.isdir()):
                raise SystemExit('Unsafe archive entry: ' + entry.name)
        source.extractall(sys.argv[2], filter='data')
PYTHON
mktexlsr "$root/texmf"
export TEXMFHOME="$root/texmf"
# Explicit portable Pandoc pin matches REPRODUCE.md, avoiding template drift.
archive=pandoc-3.1.3-linux-amd64.tar.gz
curl --fail --location --proto '=https' --proto-redir '=https' --retry 3 --connect-timeout 30 --max-time 180 \
  "https://github.com/jgm/pandoc/releases/download/3.1.3/$archive" \
  --output "$root/$archive"
echo "74bc434908e4d858b3edbfd6271d2e9e499477837e5df1d630df4e62f113803d  $root/$archive" | sha256sum --check -
tar -xzf "$root/$archive" -C "$root" --no-same-owner
export PATH="$root/pandoc-3.1.3/bin:$PATH"
# Fail before the build if the base runner's required tools or packages are missing.
for command in pandoc xelatex inkscape pdftotext pdfinfo; do command -v "$command" >/dev/null; done
for package in acmart.cls libertine.sty inconsolata.fontspec newtxmath.sty \
  LibertinusMath-Regular.otf fontspec.sty unicode-math.sty longtable.sty \
  xurl.sty needspace.sty placeins.sty seqsplit.sty lmodern.sty; do
  test -n "$(kpsewhich "$package")" || { echo "Missing TeX dependency: $package" >&2; exit 1; }
done
pandoc --version | sed -n '1p'
printf 'TEXMFHOME=%s\n' "$TEXMFHOME" >> "${GITHUB_ENV:?}"
printf '%s\n' "$root/pandoc-3.1.3/bin" >> "${GITHUB_PATH:?}"
