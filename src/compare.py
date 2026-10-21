"""Same-size comparison: Indus vs languages vs a real non-linguistic code, plus per-corpus nulls.
Usage: python3 -I src/compare.py <study-root>     (reads data/, never executes it)

Each comparison corpus is cut into texts that start at a natural unit (line, sentence, opening)
with lengths drawn from the Indus length distribution, deduplicated like the Indus set, and
sampled to the Indus text count. Five draws per corpus; mean ± sd reported."""
import sys, re, json, math, random, unicodedata, collections as C

ROOT = sys.argv[1]
D = ROOT + "/data/"

# ---------- Indus (same parser as structural.py) ----------
def tuples(body):
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

def indus():
    sql = open(D + "indus/population-script.sql", encoding="utf-8", errors="replace").read()
    m = re.search(r"INSERT INTO\s+GLYPHSEQUENCE\s*\([^)]*\)\s*VALUES(.*?);\s*$", sql, re.S | re.M)
    seq = C.defaultdict(list)
    for s, g, i in tuples(m.group(1)):
        if g != "0": seq[s].append((int(i), g))          # GLYPH 0 is "<br>", a line break, not a sign
    return sorted({tuple(g for _, g in sorted(v)) for v in seq.values()})

# ---------- comparison corpora: lists of natural units, each a token list ----------
SK_V = ["ai", "au", "ā", "ī", "ū", "ṝ", "ṛ", "ḷ", "a", "i", "u", "e", "o"]
SK_C2 = ["kh", "gh", "ch", "jh", "ṭh", "ḍh", "th", "dh", "ph", "bh"]
def sk_syllables(word):
    w = unicodedata.normalize("NFC", word.lower()); ph, i = [], 0
    while i < len(w):
        two = w[i:i+2]
        if two in SK_C2 or two in ("ai", "au"): ph.append(two); i += 2
        else: ph.append(w[i]); i += 1
    syl, onset = [], ""
    for p in ph:
        if p in SK_V: syl.append(onset + p); onset = ""
        elif p in ("ṁ", "ṃ", "ḥ") and syl: syl[-1] += p
        elif p.isalpha() or p in SK_C2: onset += p
    if onset and syl: syl[-1] += onset
    return syl

def sanskrit():
    units = []
    for line in open(D + "compare/rv.txt", encoding="utf-8"):
        u = [s for w in line.split() for s in sk_syllables(w)]
        if u: units.append(u)
    return units

def aksharas(text):
    out = []
    for ch in unicodedata.normalize("NFC", text):
        cat = unicodedata.category(ch)
        if cat.startswith("M") and out: out[-1] += ch
        elif cat.startswith("L"): out.append(ch)
    return out

def tamil():
    k = json.load(open(D + "compare/thirukkural.json", encoding="utf-8"))["kural"]
    return [u for x in k for u in (aksharas(x["Line1"]), aksharas(x["Line2"])) if u]

def english():
    t = open(D + "compare/english.txt", encoding="utf-8").read()
    t = t[t.find("*** START"):t.find("*** END")]
    t = t[t.find("\n"):]
    return [w for w in (re.findall(r"[a-z]+", s.lower()) for s in re.split(r"[.!?]+", t)) if w]

def chess():
    units = []
    for f in "abcde":
        for line in open(D + f"compare/chess_{f}.tsv", encoding="utf-8").read().splitlines()[1:]:
            pgn = line.split("\t")[2]
            units.append([m for m in pgn.split() if not re.fullmatch(r"\d+\.+", m)])
    return units

# ---------- text construction ----------
def cut(units, lengths, n, rng):
    """Texts = first k tokens of a unit, k from the Indus lengths; dedup; sample n."""
    seen = set()
    for u in rng.sample(units, len(units)):
        seen.add(tuple(u[:rng.choice(lengths)]))
    pool = sorted(seen)
    return rng.sample(pool, min(n, len(pool)))

# ---------- metrics ----------
def cond_H(ts):
    b = C.Counter((a, c) for t in ts for a, c in zip(t, t[1:]))
    f = C.Counter(a for t in ts for a in t[:-1])
    n = sum(b.values())
    return -sum(c / n * math.log2(c / f[a]) for (a, _), c in b.items())

def H(cnt):
    n = sum(cnt.values()); return -sum(c / n * math.log2(c / n) for c in cnt.values())

def pclass(i, L): return (min(i, 2), min(L - 1 - i, 2))

def slot_null(ts, rng):
    """Keep every token's position class, shuffle which token fills it across the corpus."""
    by = C.defaultdict(list)
    for t in ts:
        for i, g in enumerate(t): by[pclass(i, len(t))].append(g)
    for v in by.values(): rng.shuffle(v)
    it = {k: iter(v) for k, v in by.items()}
    return [[next(it[pclass(i, len(t))]) for i in range(len(t))] for t in ts]

def pos_info(ts):
    """I(token; first/middle/last) / H(class), texts of length >= 3."""
    j = C.Counter(); tk = C.Counter(); cl = C.Counter()
    for t in ts:
        if len(t) < 3: continue
        for i, g in enumerate(t):
            c = "F" if i == 0 else "L" if i == len(t) - 1 else "M"
            j[(g, c)] += 1; tk[g] += 1; cl[c] += 1
    n = sum(j.values())
    mi = sum(v / n * math.log2((v / n) / ((tk[g] / n) * (cl[c] / n))) for (g, c), v in j.items())
    return mi / H(cl)

def metrics(ts, rng):
    uni = C.Counter(g for t in ts for g in t); N = sum(uni.values())
    ranked = [c for _, c in uni.most_common()]
    xs = [math.log(r) for r in range(1, len(ranked) + 1)]; ys = [math.log(c) for c in ranked]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    hc = cond_H(ts)
    within = sum(cond_H([rng.sample(t, len(t)) for t in ts]) for _ in range(5)) / 5
    slot = sum(cond_H(slot_null(ts, rng)) for _ in range(5)) / 5
    pi = pos_info(ts)
    pi0 = sum(pos_info([rng.sample(t, len(t)) for t in ts]) for _ in range(5)) / 5
    return {
        "texts": len(ts), "tokens": N, "types": len(uni),
        "mean_len": N / len(ts),
        "hapax_types%": 100 * sum(c == 1 for c in uni.values()) / len(uni),
        "top10%": 100 * sum(ranked[:10]) / N,
        "zipf": sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs),
        "repeat%": 100 * sum(len(set(t)) < len(t) for t in ts) / len(ts),
        "H1": H(uni), "Hcond": hc,
        "order_gain%": 100 * (within - hc) / within,
        "beyond_slots%": 100 * (slot - hc) / slot,
        "pos_info": pi - pi0,
    }

def summarise(name, runs):
    keys = runs[0].keys(); row = {"corpus": name}
    for k in keys:
        v = [r[k] for r in runs]; m = sum(v) / len(v)
        sd = (sum((x - m) ** 2 for x in v) / (len(v) - 1)) ** 0.5 if len(v) > 1 else 0
        row[k] = (m, sd)
    return row

def main():
    ind = [list(t) for t in indus()]
    lengths = [len(t) for t in ind]; n = len(ind)
    rows = [summarise("Indus", [metrics(ind, random.Random(s)) for s in range(5)])]
    for name, f in [("Sanskrit (Rig Veda, syllables)", sanskrit), ("Old Tamil (Kural, aksharas)", tamil),
                    ("English (words)", english), ("Chess openings (moves)", chess)]:
        units = f(); runs = []
        for s in range(5):
            rng = random.Random(100 + s)
            runs.append(metrics(cut(units, lengths, n, rng), rng))
        rows.append(summarise(name, runs))
        print(f"# {name}: {len(units)} natural units", file=sys.stderr)
    cols = ["texts", "tokens", "types", "mean_len", "hapax_types%", "top10%", "zipf", "repeat%",
            "H1", "Hcond", "order_gain%", "beyond_slots%", "pos_info"]
    print("| corpus | " + " | ".join(cols) + " |")
    print("|---" * (len(cols) + 1) + "|")
    for r in rows:
        cells = []
        for c in cols:
            m, sd = r[c]
            cells.append(f"{m:.0f}" if c in ("texts", "tokens", "types") else
                         f"{m:.2f}±{sd:.2f}" if sd >= 0.005 else f"{m:.2f}")
        print(f"| {r['corpus']} | " + " | ".join(cells) + " |")

if __name__ == "__main__":
    main()
