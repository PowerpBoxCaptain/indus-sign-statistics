"""Numbers as an anchor: which signs follow a number sign far more often than chance (candidate counted
things), what number values they take, and on which objects. Reading order = stored order reversed
(inferred). Number values are stroke counts read from the glyphs. Null: order shuffled inside each text.
Usage: python3 -I src/number_anchor.py <study-root>  → stdout + results/number-anchor-signs.png"""
import sys, re, io, contextlib, random, collections as C

ROOT = sys.argv[1]
sys.path.insert(0, ROOT + "/src")
import compare as K

VALUE = {"3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "13": 3, "14": 4, "15": 5, "16": 6, "17": 7,
         "18": 8, "19": 9, "27": 7, "55": 9}
NUM = set(VALUE)

sql = open(ROOT + "/data/indus/population-script.sql", encoding="utf-8", errors="replace").read()
def block(t):
    m = re.search(r"INSERT INTO\s*%s\s*\([^)]*\)\s*VALUES(.*?);\s*$" % t, sql, re.S | re.M); return K.tuples(m.group(1))
feat = {r[0]: r[1] for r in block("FEATURE")}
otype = {}
for s, q in block("ICONOGRAPHYFEATURES"): otype.setdefault(s, feat.get(q, q).split(":")[0])
seq = C.defaultdict(list)
for s, g, i in block("GLYPHSEQUENCE"):
    if g != "0": seq[s].append((int(i), g))
objs = {s: list(reversed([g for _, g in sorted(v)])) for s, v in seq.items()}
texts = [list(t) for t in sorted({tuple(t) for t in objs.values()})]          # distinct texts

def after_counts(ts):
    a, tot = C.Counter(), C.Counter()
    for t in ts:
        for i, g in enumerate(t):
            if g in NUM: continue
            tot[g] += 1
            if i > 0 and t[i - 1] in NUM: a[g] += 1
    return a, tot

real, tot = after_counts(texts)
rng = random.Random(2026); sims = C.defaultdict(list)
for _ in range(500):
    a, _ = after_counts([rng.sample(t, len(t)) for t in texts])
    for g in tot: sims[g].append(a[g])

vals = C.defaultdict(list); where = C.defaultdict(C.Counter)
for t in texts:
    for i in range(1, len(t)):
        if t[i - 1] in NUM and t[i] not in NUM: vals[t[i]].append(VALUE[t[i - 1]])
for s, t in objs.items():
    for i in range(1, len(t)):
        if t[i - 1] in NUM and t[i] not in NUM: where[t[i]][otype.get(s, "?")] += 1

rows = []
for g in tot:
    if real[g] < 5: continue
    m = sum(sims[g]) / len(sims[g]); sd = (sum((x - m) ** 2 for x in sims[g]) / (len(sims[g]) - 1)) ** .5 or 0.5
    rows.append((g, real[g], tot[g], m, (real[g] - m) / sd, sorted(set(vals[g]))))
rows.sort(key=lambda r: -r[4])
n_num = sum(1 for t in texts for g in t if g in NUM)
print(f"distinct texts {len(texts)} · number-sign occurrences {n_num} · signs following a number at least 5 times: {len(rows)}\n")
print("| sign | after a number | all uses | share | expected (shuffled) | z | number values seen | objects (after a number) |")
print("|---|---|---|---|---|---|---|---|")
for g, r, n, m, z, v in rows:
    print(f"| {g} | {r} | {n} | {r/n:.0%} | {m:.1f} | {z:+.1f} | {','.join(map(str, v))} | "
          + ", ".join(f"{k} {c}" for k, c in where[g].most_common(3)) + " |")

cands = [r for r in rows if r[4] >= 3]
print(f"\ncandidates (z >= 3): {len(cands)} → " + ", ".join(r[0] for r in cands))

# ---- sheet: the candidates' shapes, and the number signs for reference ----
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(ROOT + "/src/render.py").read().split("first = C.Counter")[0])
sheet([("Signs that follow a number far more than chance (z >= 3), strongest first: sign (times after a number / all uses)",
        [(r[0], f" ({r[1]}/{r[2]})") for r in cands]),
       ("Number signs, with stroke value", [(g, f" ={VALUE[g]}") for g in sorted(NUM, key=int)])],
      ROOT + "/results/number-anchor-signs.png", width=10)
