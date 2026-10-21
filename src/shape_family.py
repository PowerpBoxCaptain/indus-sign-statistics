"""Do signs that keep the same company also have nearby catalogue codes (i.e. the same shape family)?
For each sign seen >= 15 times, take its closest match by shared neighbours and ask whether the two
codes are within 10 of each other. Null: the same similarity matrix with sign labels shuffled.
Usage: python3 -I src/shape_family.py <repo-root>"""
import sys, io, random, contextlib
import numpy as np

ROOT = sys.argv[1]
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(ROOT + "/src/grammar_groups.py").read())

keep, S, freq = vectors(ind, 15)
codes = np.array([int(k) for k in keep])

def score(S):
    hits = 0
    for i in range(len(keep)):
        j = [j for j in np.argsort(-S[i]) if j != i][0]
        hits += abs(codes[i] - codes[j]) <= 10
    return hits

real = score(S); r = random.Random(5); null = []
for _ in range(500):
    p = list(range(len(keep))); r.shuffle(p); null.append(score(S[np.ix_(p, p)]))
m, sd = np.mean(null), np.std(null, ddof=1)
print(f"nearest neighbour (by shared context) has a code within ±10: {real}/{len(keep)} signs; "
      f"shuffled-labels null {m:.1f}±{sd:.1f}; p≈{(np.sum(np.array(null) >= real) + 1) / 501:.3f}")
