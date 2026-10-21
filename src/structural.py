"""Structural pass over the Indus corpus SQL dump (yajnadevam/indus-website, GPL-3.0).
Reads the dump as text; never executes it. Usage: python3 -I structural.py <dump.sql>"""
import sys, re, math, random, collections as C

sql = open(sys.argv[1], encoding="utf-8", errors="replace").read()

def rows(table):
    """Tuples from every INSERT INTO <table> ... VALUES block."""
    out = []
    for m in re.finditer(r"INSERT INTO\s+%s\s*\(([^)]*)\)\s*VALUES(.*?);\s*$" % table, sql, re.S | re.M):
        out += tuples(m.group(2))
    return out

def tuples(body):
    """Split '(a, "b, (c)"), (...)' into rows, respecting quoted strings."""
    out, row, cur, q, depth = [], [], "", None, 0
    for ch in body:
        if q:
            if ch == q: q = None
            else: cur += ch
        elif ch in "\"'": q = ch
        elif ch == "(":
            depth += 1; row, cur = [], ""
        elif ch == ")" and depth:
            depth -= 1; row.append(cur.strip()); out.append(row)
        elif ch == "," and depth:
            row.append(cur.strip()); cur = ""
        elif depth: cur += ch
    return out

sites = {r[0]: r[1] for r in rows("SITE")}
seals = {int(r[0]): {"site": sites.get(r[1], r[1]), "cisi": r[3]} for r in rows("SEAL")}
insc = {int(r[0]): {"complete": r[1], "dir": r[2]} for r in rows("INSCRIPTION")}
feat = {r[0]: r[1] for r in rows("FEATURE")}
objtype = C.defaultdict(set)
for s, q in rows("ICONOGRAPHYFEATURES"):
    objtype[int(s)].add(feat.get(q, q).split(":")[0])
seq = C.defaultdict(list)
for s, g, i in rows("GLYPHSEQUENCE"):
    if g != "0": seq[int(s)].append((int(i), int(g)))   # GLYPH 0 is "<br>", a line break, not a sign
texts = {s: [g for _, g in sorted(v)] for s, v in seq.items()}

P = print
P("== CORPUS")
P(f"seals {len(seals)} · inscription rows {len(insc)} · texts with signs {len(texts)}")
tok = [g for t in texts.values() for g in t]
P(f"sign tokens {len(tok)} · sign types {len(set(tok))}")
dirs = C.Counter(insc.get(s, {}).get("dir") for s in texts)
comp = C.Counter(insc.get(s, {}).get("complete") for s in texts)
P(f"direction field {dict(dirs)} · complete field {dict(comp)}")
P("sites (texts):", ", ".join(f"{k} {v}" for k, v in C.Counter(seals[s]["site"] for s in texts if s in seals).most_common(8)))
P("object type (texts):", dict(C.Counter(t for s in texts for t in objtype.get(s, {"?"})).most_common(8)))

# Working set: complete texts, deduplicated by identical sequence (repeated impressions inflate counts).
full = [t for s, t in texts.items() if insc.get(s, {}).get("complete") == "Y"]
dedup = sorted(set(map(tuple, full)))
P(f"\n== WORKING SET: complete texts {len(full)} → distinct sequences {len(dedup)}")
L = C.Counter(len(t) for t in dedup)
P("length distribution:", " ".join(f"{k}:{L[k]}" for k in sorted(L)))
P(f"mean length {sum(len(t) for t in dedup)/len(dedup):.2f} · max {max(L)}")

uni = C.Counter(g for t in dedup for g in t)
N = sum(uni.values())
P(f"\n== FREQUENCY (distinct set): tokens {N}, types {len(uni)}")
hapax = sum(1 for c in uni.values() if c == 1)
P(f"signs used once (hapax) {hapax} = {hapax/len(uni):.0%} of types, {hapax/N:.1%} of tokens")
ranked = [c for _, c in uni.most_common()]
for k in (10, 50, 100, 200):
    P(f"top {k} signs cover {sum(ranked[:k])/N:.1%} of tokens")
xs = [math.log(r) for r in range(1, len(ranked) + 1)]; ys = [math.log(c) for c in ranked]
mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
P(f"Zipf slope (log freq vs log rank, all types) {slope:.2f}")
P("top 15:", " ".join(f"{g}:{c}" for g, c in uni.most_common(15)))

P("\n== POSITION (IDX 0 = first stored sign; texts of length ≥2)")
first, last, mid = C.Counter(), C.Counter(), C.Counter()
for t in dedup:
    if len(t) < 2: continue
    first[t[0]] += 1; last[t[-1]] += 1
    for g in t[1:-1]: mid[g] += 1
for g, c in uni.most_common(15):
    tot = first[g] + last[g] + mid[g]
    if tot: P(f"  sign {g:>4}: n={tot:4} first {first[g]/tot:5.0%} middle {mid[g]/tot:5.0%} last {last[g]/tot:5.0%}")
# Same check split by the dump's direction field, for the commonest sign.
g0 = uni.most_common(1)[0][0]
for d in ("L/R", "R/L"):
    ts = [texts[s] for s in texts if insc.get(s, {}).get("dir") == d and insc[s]["complete"] == "Y" and len(texts[s]) >= 2]
    if ts:
        P(f"  sign {g0} in {d} texts: first {sum(t[0]==g0 for t in ts)}, last {sum(t[-1]==g0 for t in ts)} of {len(ts)}")

P("\n== REPETITION inside a text")
rep = [t for t in dedup if len(set(t)) < len(t)]
P(f"texts with a repeated sign {len(rep)}/{len(dedup)} = {len(rep)/len(dedup):.1%}")
adj = sum(1 for t in dedup for a, b in zip(t, t[1:]) if a == b)
P(f"adjacent doubles (same sign twice in a row) {adj}")

P("\n== PAIRS AND RUNS")
bi = C.Counter((a, b) for t in dedup for a, b in zip(t, t[1:]))
P("top bigrams:", " ".join(f"{a}-{b}:{c}" for (a, b), c in bi.most_common(12)))
tri = C.Counter(tuple(t[i:i+3]) for t in dedup for i in range(len(t) - 2))
P("top trigrams:", " ".join("-".join(map(str, k)) + f":{c}" for k, c in tri.most_common(8)))
P(f"distinct bigram types {len(bi)}, of which seen once {sum(c==1 for c in bi.values())}")

def H(counter):
    n = sum(counter.values()); return -sum(c / n * math.log2(c / n) for c in counter.values())

def cond_entropy(ts):
    b = C.Counter((a, c) for t in ts for a, c in zip(t, t[1:]))
    f = C.Counter(a for t in ts for a in t[:-1])
    n = sum(b.values())
    return -sum(c / n * math.log2(c / f[a]) for (a, _), c in b.items())

P("\n== ENTROPY (bits). Plug-in estimates: small samples bias these low; compare like with like only.")
real = cond_entropy(dedup)
P(f"unigram H {H(uni):.2f} · conditional H(next|prev) {real:.2f}")
random.seed(7)
def null(f, k=20):
    v = [cond_entropy(f()) for _ in range(k)]; m = sum(v) / k
    return m, (sum((x - m) ** 2 for x in v) / (k - 1)) ** 0.5
pool = [g for t in dedup for g in t]
def shuffled_within(): return [random.sample(t, len(t)) for t in dedup]
def shuffled_corpus():
    p = pool[:]; random.shuffle(p); out, i = [], 0
    for t in dedup: out.append(p[i:i+len(t)]); i += len(t)
    return out
m1, s1 = null(shuffled_within); m2, s2 = null(shuffled_corpus)
P(f"null A, order shuffled inside each text: {m1:.2f} ± {s1:.2f}")
P(f"null B, signs shuffled across the corpus: {m2:.2f} ± {s2:.2f}")
P(f"real is {(m1-real)/s1:.1f} sd below A and {(m2-real)/s2:.1f} sd below B")

P("\n== SITES (distinct complete texts per site, mean length, share of top-10 signs)")
top10 = {g for g, _ in uni.most_common(10)}
bysite = C.defaultdict(set)
for s, t in texts.items():
    if insc.get(s, {}).get("complete") == "Y" and s in seals: bysite[seals[s]["site"]].add(tuple(t))
for site, ts in sorted(bysite.items(), key=lambda kv: -len(kv[1]))[:6]:
    toks = [g for t in ts for g in t]
    P(f"  {site:14} {len(ts):5} texts · mean len {len(toks)/len(ts):.2f} · top-10 share {sum(g in top10 for g in toks)/len(toks):.0%}")
