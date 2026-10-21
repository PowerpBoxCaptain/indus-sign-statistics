"""Position baseline for the number signs: how often do they end a text, against frequency-matched other signs?
Reading order = stored order reversed (jar sign text-final; inferred). Seed 7, 500 control sets.
Usage: python3 -I src/numeral_position.py <repo-root>"""
import sys, random, collections as C

sys.path.insert(0, sys.argv[1] + "/src")
import compare as K

texts = [list(reversed(t)) for t in K.indus()]
freq = C.Counter(g for t in texts for g in t)
NUM = ["3", "4", "5", "6", "7", "13", "14", "15", "16", "17", "18", "19", "27", "55"]
excl = set(NUM) | {"1", "2", "31", "32", "33", "35", "740"}

def pos(S):
    S = set(S); f = l = n = 0
    for t in texts:
        if len(t) < 2: continue
        for i, g in enumerate(t):
            if g in S:
                n += 1; f += i == 0; l += i == len(t) - 1
    return f / n, l / n, n

rf, rl, rn = pos(NUM)
pool = [g for g in freq if g not in excl]
rng = random.Random(7); F, L = [], []
for _ in range(500):
    pick = []
    for g in NUM:
        cand = sorted(pool, key=lambda x: abs(freq[x] - freq[g]))[:15]
        pick.append(rng.choice([c for c in cand if c not in pick] or cand))
    a, b, _ = pos(pick); F.append(a); L.append(b)

def z(x, v):
    m = sum(v) / len(v); s = (sum((y - m) ** 2 for y in v) / (len(v) - 1)) ** .5; return m, s, (x - m) / s

mf, sf, zf = z(rf, F); ml, sl, zl = z(rl, L)
print("== position baseline (texts of 2+ signs; jar sign and the tick/stroke series excluded from controls)")
print(f"numerals: first {rf:.1%}, last {rl:.1%} (n={rn})")
print(f"frequency-matched other signs: first {mf:.1%} ± {sf:.1%} (numerals z {zf:+.1f}); last {ml:.1%} ± {sl:.1%} (numerals z {zl:+.1f})")
print(f"share of control sets with last-share as low as the numerals': {sum(x <= rl for x in L) / len(L):.3f}")
