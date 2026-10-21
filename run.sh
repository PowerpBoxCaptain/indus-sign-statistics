#!/usr/bin/env bash
# Reproduce every result in results/ from the pinned inputs. Needs python3 with numpy and Pillow.
set -euo pipefail
cd "$(dirname "$0")"
[ -f data/indus/population-script.sql ] || ./fetch_data.sh
python3 -I src/structural.py data/indus/population-script.sql > results/structural.txt
python3 -I src/compare.py . > results/compare.md
python3 -I src/grammar_groups.py . > results/grammar-and-groups.md
python3 -I src/shape_family.py . > results/shape-family.txt
python3 -I src/motif.py . > results/motif.txt
python3 -I src/render.py .
python3 -I src/numerals.py . > results/numerals.txt
python3 -I src/numeral_position.py . >> results/numerals.txt
python3 -I src/step2_endings.py . > results/endings.md
python3 -I src/picture_test.py . > results/picture-test.txt
python3 -I src/number_anchor.py . > results/number-anchor.md
python3 -I src/numbered_names.py . > results/numbered-names.txt
python3 -I src/prejar_slot.py . > results/prejar-slot.md
python3 -I blind/symbols.py .
python3 -I blind/match.py . > /dev/null
echo "done: results/"
