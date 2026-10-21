#!/usr/bin/env bash
# Download every input from its upstream, pinned to a commit, and check each file's sha256.
# Nothing is redistributed in this repository; all data stays under its own licence.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p data/indus data/compare

get() {  # get <url> <dest> <sha256>
  curl -fsSL --retry 2 -m 120 -o "$2" "$1"
  echo "$3  $2" | sha256sum -c --quiet || { echo "checksum mismatch: $2" >&2; exit 1; }
  echo "ok  $2"
}

IW=https://raw.githubusercontent.com/yajnadevam/indus-website/2434249618b1e74de3f26d28b90dfde093c3dd94
get $IW/population-script.sql data/indus/population-script.sql a1bcc150e91ede5e1c3ce813073d8ac7bfe370d2709be320132a651ba9c7a54c
get $IW/src/assets/fonts/sk_indus_script-webfont.ttf data/indus/sk_indus_script-webfont.ttf 2fccc124e03b8c3644e601e35e5d62af57c71d2b66396c21c15813a4a932c478

get https://raw.githubusercontent.com/Equationist/indusscript-decipherment-stats/90c70d813290b7d50756b574ec9dbedb6a7656be/rv_names_epithets.txt \
    data/compare/rv.txt 797ca3515e4455f952164dea36e2680167dc11bc86aedfc85ac017dc0c1182c1
get https://raw.githubusercontent.com/tk120404/thirukkural/cf3ff6c5a73c23b4092913156830457caab65fd4/thirukkural.json \
    data/compare/thirukkural.json e793099d6f300787329cf22bc0a144292d4af11b9dc3ca9595f1928692f4caee

CH=https://raw.githubusercontent.com/lichess-org/chess-openings/a6189a30dc273ccb21fc2536a9a2fefd5592a67a
get $CH/a.tsv data/compare/chess_a.tsv 3282e4c9155289a29224f9a85fba0decb46efa35c2fa5e39662d2ac48fb0f793
get $CH/b.tsv data/compare/chess_b.tsv 1d5ed134ebbd87915ead5683416e37583bb3e5ae3582b4d8cb5cb4aa7ef4f623
get $CH/c.tsv data/compare/chess_c.tsv 45e843c7b7e79a0d04d5bda879c9bd23f5a10974488bd8615e4f4c5d0749986f
get $CH/d.tsv data/compare/chess_d.tsv 1cf4057a8aece94f27bb3f278ad410ee2844831a642364eeceaafa091dbcceda
get $CH/e.tsv data/compare/chess_e.tsv 48c6f6645b031a5937c8386839debab0e2e48837251687ba1afb6369677f8546

# Project Gutenberg can re-issue a file with a new header; if this check fails, the text itself is unchanged
# but the comparison numbers for English may move slightly.
get https://www.gutenberg.org/cache/epub/1342/pg1342.txt data/compare/english.txt 3f6bb9d6f78e0293b56acd4714dd68cb7d6d1d293402031ce9d5a216bcaf9d75
