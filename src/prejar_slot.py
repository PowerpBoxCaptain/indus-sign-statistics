"""Who fills the slot before the closing jar? For texts ending with the jar (sign 740, reading order =
stored order reversed, inferred), the unit right before it: a single sign, or number + sign.
Specialists: signs found before a final jar far more than chance (order shuffled inside each text, 500x).
Jar-optional check: in texts NOT ending with the jar, how often do the specialists end the text?
Usage: python3 -I src/prejar_slot.py <study-root>  → stdout + results/prejar-slot-signs.png"""
import sys, io, contextlib, random, collections as C

ROOT = sys.argv[1]
sys.path.insert(0, ROOT + "/src")
import compare as K

JAR = "740"
NUM = {"3", "4", "5", "6", "7", "13", "14", "15", "16", "17", "18", "19", "27", "55"}
texts = [list(t) for t in sorted({tuple(reversed(t)) for t in K.indus()})]
jar_final = [t for t in texts if len(t) >= 2 and t[-1] == JAR]
other = [t for t in texts if len(t) >= 2 and t[-1] != JAR]
print(f"distinct texts {len(texts)} · ending with the jar {len(jar_final)} ({len(jar_final)/len(texts):.0%}) · other texts of 2+ signs {len(other)}")

units = C.Counter()
for t in jar_final:
    y = t[-2]
    units[(t[-3] + "+" + y) if len(t) >= 3 and t[-3] in NUM and y not in NUM else y] += 1
print(f"\n== 1. Fillers of the slot before a final jar: {sum(units.values())} uses, {len(units)} different units")
print("   commonest: " + ", ".join(f"{u} ({c})" for u, c in units.most_common(20)))
single = sum(c for u, c in units.items() if c == 1)
print(f"   units seen only once there: {single} ({single/len(units):.0%} of the different units)")

def prejar(ts):
    c = C.Counter()
    for t in ts:
        if len(t) >= 2 and t[-1] == JAR: c[t[-2]] += 1
    return c
real = prejar(texts)
tot = C.Counter(g for t in texts for g in t)
rng = random.Random(2026); sims = C.defaultdict(list)
for _ in range(500):
    s = prejar([rng.sample(t, len(t)) for t in texts])
    for g in tot: sims[g].append(s[g])
rows = []
for g, r in real.items():
    if r < 5 or g == JAR: continue
    m = sum(sims[g]) / 500; sd = (sum((x - m) ** 2 for x in sims[g]) / 499) ** .5 or 0.5
    rows.append((g, r, tot[g], m, (r - m) / sd))
rows.sort(key=lambda r: -r[4])
spec = [r for r in rows if r[4] >= 3]
print(f"\n== 2. Slot specialists (before a final jar >= 5 times, z >= 3): {len(spec)}")
print("| sign | before final jar | all uses | share | expected | z | ends a no-jar text |")
print("|---|---|---|---|---|---|---|")
oth_final = C.Counter(t[-1] for t in other); oth_tot = C.Counter(g for t in other for g in t)
for g, r, n, m, z in spec:
    of = oth_final[g] / oth_tot[g] if oth_tot[g] else float("nan")
    print(f"| {g} | {r} | {n} | {r/n:.0%} | {m:.1f} | {z:+.1f} | {oth_final[g]}/{oth_tot[g]} ({of:.0%}) |")

# jar-optional: specialists vs other signs, share of their uses (in no-jar texts) that end the text
sp = {g for g, *_ in spec}
def end_share(S):
    e = sum(oth_final[g] for g in S); n = sum(oth_tot[g] for g in S); return e / n if n else float("nan"), n
es, en = end_share(sp)
rest = [g for g in oth_tot if g not in sp and g != JAR and g not in NUM and tot[g] >= 20]
eo, eon = end_share(rest)
print(f"\n== 3. Jar optional? In texts not ending with the jar, uses that END the text:"
      f" specialists {es:.0%} (of {en}) vs other common signs {eo:.0%} (of {eon})")

with contextlib.redirect_stdout(io.StringIO()):
    exec(open(ROOT + "/src/render.py").read().split("first = C.Counter")[0])
sheet([("Slot specialists: signs before a closing jar far more than chance (times before the jar / all uses)",
        [(g, f" ({r}/{n})") for g, r, n, m, z in spec])], ROOT + "/results/prejar-slot-signs.png", width=10)
