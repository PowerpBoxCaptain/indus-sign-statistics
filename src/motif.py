"""Does a seal's text depend on the animal carved on it?
Pairs each distinct text with the object's iconography label (the dataset's own abbreviation), keeps
motifs with >= 25 distinct texts, and measures sign-motif mutual information against shuffled motifs.
Usage: python3 -I src/motif.py <repo-root>"""
import sys, re, random, math, collections as C

ROOT = sys.argv[1]
sys.path.insert(0, ROOT + "/src")
import compare as K

sql = open(ROOT + "/data/indus/population-script.sql", encoding="utf-8", errors="replace").read()

def block(table):
    m = re.search(r"INSERT INTO\s*%s\s*\([^)]*\)\s*VALUES(.*?);\s*$" % table, sql, re.S | re.M)
    return K.tuples(m.group(1))

ico = {r[0]: r[1].split(":")[0] for r in block("ICONOGRAPHY")}
seq = C.defaultdict(list)
for s, g, i in block("GLYPHSEQUENCE"):
    if g != "0": seq[s].append((int(i), g))          # GLYPH 0 is "<br>", a line break, not a sign
texts = {s: tuple(g for _, g in sorted(v)) for s, v in seq.items()}

print("motif labels (raw counts, objects):", C.Counter(ico.values()).most_common(14))
pairs = sorted({(ico[s], t) for s, t in texts.items() if s in ico})
mc = C.Counter(m for m, _ in pairs)
top = [m for m, c in mc.most_common() if c >= 25]
pairs = [(m, t) for m, t in pairs if m in top]
print("motifs with >= 25 distinct texts:", {m: mc[m] for m in top})

def mi(pr):
    j = C.Counter((m, g) for m, t in pr for g in set(t))
    mm = C.Counter(m for m, t in pr for g in set(t)); gg = C.Counter(g for m, t in pr for g in set(t))
    n = sum(j.values())
    return sum(v / n * math.log2(v * n / (mm[m] * gg[g])) for (m, g), v in j.items())

real = mi(pairs); r = random.Random(3)
ms = [m for m, _ in pairs]; ts = [t for _, t in pairs]; null = []
for _ in range(300):
    r.shuffle(ms); null.append(mi(list(zip(ms, ts))))
mu = sum(null) / len(null); sd = (sum((x - mu) ** 2 for x in null) / (len(null) - 1)) ** .5
print(f"sign-motif mutual information {real:.3f} bits vs shuffled motifs {mu:.3f}±{sd:.3f} ({(real - mu) / sd:.1f} sd)")

allc = C.Counter(g for _, t in pairs for g in set(t)); N = len(pairs)
for m in top:
    tm = [t for mm, t in pairs if mm == m]; c = C.Counter(g for t in tm for g in set(t))
    lift = sorted(((c[g] / len(tm)) / (allc[g] / N), g, c[g]) for g in c if c[g] >= 5)[::-1][:4]
    print(f"  {m:10} n={len(tm):4}  most over-used signs: " + ", ".join(f"{g} x{l:.1f} ({k})" for l, g, k in lift))
