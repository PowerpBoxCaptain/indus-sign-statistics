"""Picture test: is the carved animal an emblem and the text a name or title?
Data: our corpus dump (texts, object types, the dump's own picture labels, checked against the CISI plate
headings: "Bull1" = unicorn in 91% of joinable cases). Reading order = stored order reversed (inferred).
P1  identical texts on several seals: do the copies share one animal more than chance?
P2  where does the text-animal link sit: opening sign, closing sign(s), or the middle?
P3  text length and repetition by object type.
Nulls: animal labels shuffled among the same seals (2,000 shuffles, seed 2026).
Usage: python3 -I src/picture_test.py <study-root>"""
import sys, re, math, random, collections as C

ROOT = sys.argv[1]
sys.path.insert(0, ROOT + "/src")
import compare as K

sql = open(ROOT + "/data/indus/population-script.sql", encoding="utf-8", errors="replace").read()
def block(t):
    m = re.search(r"INSERT INTO\s*%s\s*\([^)]*\)\s*VALUES(.*?);\s*$" % t, sql, re.S | re.M); return K.tuples(m.group(1))
feat = {r[0]: r[1] for r in block("FEATURE")}
otype = {}
for s, q in block("ICONOGRAPHYFEATURES"):
    otype.setdefault(s, feat.get(q, q).split(":")[0])
motif = {r[0]: r[1].split(":")[0] for r in block("ICONOGRAPHY")}
seq = C.defaultdict(list)
for s, g, i in block("GLYPHSEQUENCE"):
    if g != "0": seq[s].append((int(i), g))
text = {s: tuple(reversed([g for _, g in sorted(v)])) for s, v in seq.items()}      # reading order

seals = [s for s in text if otype.get(s) == "SEAL" and s in motif]
mc = C.Counter(motif[s] for s in seals)
keep = {m for m, c in mc.items() if c >= 15}
seals = [s for s in seals if motif[s] in keep]
print(f"seals with text and a picture label: {len(seals)} · labels kept (>=15 seals): {dict(mc.most_common(len(keep)))}")
rng = random.Random(2026)

# ---------- P1: repeated texts ----------
by_text = C.defaultdict(list)
for s in seals:
    if len(text[s]) >= 2: by_text[text[s]].append(s)
groups = [g for g in by_text.values() if len(g) >= 2]
def same_share(lab):
    return sum(len({lab[s] for s in g}) == 1 for g in groups) / len(groups)
real = same_share(motif)
null = []
ids = [s for g in groups for s in g]; labs = [motif[s] for s in ids]
for _ in range(2000):
    rng.shuffle(labs); null.append(same_share(dict(zip(ids, labs))))
m = sum(null) / len(null); sd = (sum((x - m) ** 2 for x in null) / (len(null) - 1)) ** .5
print(f"\n== P1 texts (2+ signs) found on 2+ seals: {len(groups)} texts on {len(ids)} seals")
print(f"   copies all carrying the same animal: {real:.0%} · shuffled labels {m:.0%} ± {sd:.0%} · z {(real-m)/sd:+.1f}"
      f" · p ≈ {(sum(x >= real for x in null)+1)/(len(null)+1):.4f}")
mixed = [g for g in groups if len({motif[s] for s in g}) > 1]
print(f"   texts whose copies carry different animals: {len(mixed)}; examples:",
      "; ".join("-".join(text[g[0]]) + " → " + "/".join(sorted({motif[s] for s in g})) for g in mixed[:4]))

# ---------- P2: where the link sits ----------
def mi(pairs):
    j = C.Counter(pairs); a = C.Counter(x for x, _ in pairs); b = C.Counter(y for _, y in pairs); n = len(pairs)
    return sum(v / n * math.log2(v * n / (a[x] * b[y])) for (x, y), v in j.items())
uniq = {}
for s in seals:                      # one object per (text, animal) so copies do not inflate the link
    uniq.setdefault((text[s], motif[s]), s)
objs = list(uniq.values())
slots = {
    "opening sign": lambda t: [t[0]],
    "closing sign": lambda t: [t[-1]],
    "closing pair": lambda t: [t[-2:]] if len(t) >= 2 else [],
    "middle signs": lambda t: list(t[1:-1]),
}
print(f"\n== P2 link between text slot and animal ({len(objs)} distinct text-animal pairs; mutual information vs shuffled animals)")
for name, f in slots.items():
    pairs = [(x, motif[s]) for s in objs for x in f(text[s])]
    r = mi(pairs); ys = [y for _, y in pairs]; xs = [x for x, _ in pairs]; nl = []
    for _ in range(500):
        rng.shuffle(ys); nl.append(mi(list(zip(xs, ys))))
    m = sum(nl) / len(nl); sd = (sum((x - m) ** 2 for x in nl) / (len(nl) - 1)) ** .5
    print(f"   {name:13} n={len(pairs):5}  MI {r:.3f} vs {m:.3f} ± {sd:.3f}  excess {r-m:+.3f}  z {(r-m)/sd:+.1f}")

# ---------- P3: object types ----------
print("\n== P3 text by object type (all objects with text)")
ty = C.defaultdict(list)
for s, t in text.items(): ty[otype.get(s, "?")].append(t)
for k, ts in sorted(ty.items(), key=lambda kv: -len(kv[1]))[:6]:
    c = C.Counter(ts)
    print(f"   {k:5} objects {len(ts):5} · mean length {sum(map(len, ts))/len(ts):.2f} · distinct texts {len(c):5}"
          f" · share of objects whose text recurs {sum(v for v in c.values() if v > 1)/len(ts):.0%}")
