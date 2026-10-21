"""Two tests on the Indus corpus, with Sanskrit and Tamil run the same way.
A. Grammar shape: are the signs at one end of a text more predictable than at the other?
   Suffixing languages (Sanskrit fusional, Tamil agglutinative) put recurring endings last.
B. Sign groups: cluster signs by the neighbours they keep (left and right context only),
   first checked on Tamil, where the true groups (shared vowel, shared consonant) are known.
Usage: python3 -I src/grammar_groups.py <study-root>"""
import sys, math, random, unicodedata, collections as C
import numpy as np

ROOT = sys.argv[1]
sys.path.insert(0, ROOT + "/src")
import compare as K

rng = random.Random(11)
ind = [list(t) for t in K.indus()]
lengths = [len(t) for t in ind]
N = len(ind)

# ---------- word-aligned language texts ----------
def sk_words():
    out = []
    for line in open(K.D + "compare/rv.txt", encoding="utf-8"):
        ws = [K.sk_syllables(w.replace("ṁ", "ṃ")) for w in line.split()]
        ws = [w for w in ws if w]
        if ws: out.append(ws)
    return out

def ta_words():
    import json
    k = json.load(open(K.D + "compare/thirukkural.json", encoding="utf-8"))["kural"]
    out = []
    for x in k:
        for line in (x["Line1"], x["Line2"]):
            ws = [K.aksharas(w) for w in line.split()]
            ws = [w for w in ws if w]
            if ws: out.append(ws)
    return out

def word_texts(lines, r):
    """Whole words from the line start, as many as fit in a length drawn from the Indus set."""
    seen = set()
    for ws in r.sample(lines, len(lines)):
        k, t = r.choice(lengths), []
        for w in ws:
            if t and len(t) + len(w) > k: break
            t += w
        seen.add(tuple(t))
    pool = sorted(seen)
    return [list(t) for t in r.sample(pool, min(N, len(pool)))]

def edge_profile(ts, depth=3):
    """Entropy (bits) and top-5 share of the token at each distance from each end."""
    out = {}
    for side in ("start", "end"):
        for d in range(depth):
            c = C.Counter((t[d] if side == "start" else t[-1 - d]) for t in ts if len(t) > d + 1)
            n = sum(c.values())
            out[(side, d)] = (K.H(c), 100 * sum(v for _, v in c.most_common(5)) / n, n)
    return out

print("## A. Grammar shape: entropy at each end (lower = more predictable, endings-like)\n")
print("Indus 'start' = stored position 0, inferred to be the reading END (jar-sign end).\n")
print("| corpus | start+0 | start+1 | start+2 | end-0 | end-1 | end-2 |")
print("|---|---|---|---|---|---|---|")
def row(name, ts):
    p = edge_profile(ts)
    cells = [f"{p[(s, d)][0]:.2f} b · top5 {p[(s, d)][1]:.0f}%" for s in ("start", "end") for d in range(3)]
    print(f"| {name} | " + " | ".join(cells) + " |")
row("Indus", ind)
sk, ta = sk_words(), ta_words()
for name, lines in (("Sanskrit, whole words", sk), ("Old Tamil, whole words", ta)):
    row(name, word_texts(lines, rng))
row("Chess openings", K.cut(K.chess(), lengths, N, rng))
# Word-level view inside the languages: first vs last syllable of every word.
for name, lines in (("Sanskrit", sk), ("Old Tamil", ta)):
    ws = [w for l in lines for w in l if len(w) >= 2]
    f, l = C.Counter(w[0] for w in ws), C.Counter(w[-1] for w in ws)
    print(f"\n{name}, every word of ≥2 units: first-unit entropy {K.H(f):.2f} b, last-unit entropy {K.H(l):.2f} b")

# ---------- B. distributional groups ----------
def vectors(ts, min_n):
    freq = C.Counter(g for t in ts for g in t)
    keep = sorted(g for g, c in freq.items() if c >= min_n)
    idx = {g: i for i, g in enumerate(keep)}
    ctx = {}
    rows = C.defaultdict(C.Counter)
    for t in ts:
        p = ["<B>"] + t + ["<E>"]
        for i in range(1, len(p) - 1):
            if p[i] in idx:
                rows[p[i]]["L:" + p[i - 1]] += 1; rows[p[i]]["R:" + p[i + 1]] += 1
    for r in rows.values():
        for k in r: ctx.setdefault(k, len(ctx))
    M = np.zeros((len(keep), len(ctx)))
    for g, r in rows.items():
        for k, v in r.items(): M[idx[g], ctx[k]] = v
    tot = M.sum(); pr = M.sum(1, keepdims=True) / tot; pc = M.sum(0, keepdims=True) / tot
    with np.errstate(divide="ignore", invalid="ignore"):
        pmi = np.log2((M / tot) / (pr * pc))
    P = np.where(M > 0, np.maximum(pmi, 0), 0)            # PPMI
    P /= np.linalg.norm(P, axis=1, keepdims=True) + 1e-12
    return keep, P @ P.T, freq

def cluster(S, k):
    """Average-linkage agglomerative clustering on a cosine-similarity matrix."""
    groups = [[i] for i in range(len(S))]
    while len(groups) > k:
        best, bi, bj = -9, 0, 0
        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                s = S[np.ix_(groups[i], groups[j])].mean()
                if s > best: best, bi, bj = s, i, j
        groups[bi] += groups.pop(bj)
    return groups

def purity(groups, labels):
    return sum(C.Counter(labels[i] for i in g).most_common(1)[0][1] for g in groups) / sum(map(len, groups))

def random_purity(groups, labels, reps=200):
    flat = [i for g in groups for i in g]; sizes = [len(g) for g in groups]; v = []
    for _ in range(reps):
        rng.shuffle(flat); it = iter(flat)
        v.append(purity([[next(it) for _ in range(s)] for s in sizes], labels))
    m = sum(v) / reps; return m, (sum((x - m) ** 2 for x in v) / (reps - 1)) ** 0.5

def ta_parts(a):
    base = a[0]; marks = a[1:]
    vowel = "inherent-a" if not marks else ("pulli" if marks == "்" else marks)
    if unicodedata.name(base, "").startswith("TAMIL LETTER") and base in "அஆஇஈஉஊஎஏஐஒஓஔ":
        vowel = "vowel-letter"
    return base, vowel

print("\n## B. Sign groups by shared neighbours\n")
ta_ts = word_texts(ta, rng)
keep, S, _ = vectors(ta_ts, 15)
g = cluster(S, 12)
cons = [ta_parts(a)[0] for a in keep]; vow = [ta_parts(a)[1] for a in keep]
for name, lab in (("same vowel sign", vow), ("same consonant", cons)):
    p = purity(g, lab); m, sd = random_purity(g, lab)
    print(f"Tamil check, {len(keep)} aksharas into 12 groups: purity by {name} {p:.2f} vs random {m:.2f}±{sd:.2f} ({(p-m)/sd:.1f} sd)")

keep, S, freq = vectors(ind, 15)
groups = cluster(S, 12)
first = C.Counter(t[0] for t in ind if len(t) > 1); last = C.Counter(t[-1] for t in ind if len(t) > 1)
print(f"\nIndus, {len(keep)} signs seen ≥15 times, 12 groups (largest first). "
      "Pos = share at stored start / at stored end:\n")
pos_lab = []
for s in keep:
    n = freq[s]; f, l = first[s] / n, last[s] / n
    pos_lab.append("start" if f > .5 else "end" if l > .5 else "middle")
for gi, grp in enumerate(sorted(groups, key=len, reverse=True), 1):
    sims = [S[i, j] for i in grp for j in grp if i < j]
    coh = sum(sims) / len(sims) if sims else float("nan")
    mem = sorted(grp, key=lambda i: -freq[keep[i]])
    pc = C.Counter(pos_lab[i] for i in grp)
    print(f"G{gi:<2} n={len(grp):<3} cohesion {coh:.2f} · {dict(pc)} · "
          + " ".join(f"{keep[i]}({freq[keep[i]]})" for i in mem[:14]) + (" …" if len(mem) > 14 else ""))
p = purity(groups, pos_lab); m, sd = random_purity(groups, pos_lab)
print(f"\nHow far the groups just restate position: purity by start/middle/end {p:.2f} vs random {m:.2f}±{sd:.2f}")

print("\nNearest neighbours (cosine) of the 10 commonest signs:")
order = sorted(range(len(keep)), key=lambda i: -freq[keep[i]])
for i in order[:10]:
    nn = [j for j in np.argsort(-S[i]) if j != i][:5]
    print(f"  {keep[i]:>4}: " + ", ".join(f"{keep[j]} {S[i, j]:.2f}" for j in nn))
