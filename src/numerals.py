"""Step 1 toward the language: do number signs come before or after the sign they count?
Reading order = stored order reversed (anchor: the jar sign 740 is text-final in reading, and sits at
stored position 0 in 70% of its uses; an inference, stated in the output).
For a sign class S, "after-paradigm" = signs Y found right after >= 2 different members of S in reading
order (3 Y, 4 Y ...); "before-paradigm" = signs Y found right before >= 2 different members (Y 3, Y 4 ...).
Numeral-before-noun languages should show a larger after-paradigm. Nulls: order shuffled inside each
text; and random frequency-matched sets of other signs.
Usage: python3 -I src/numerals.py <study-root>"""
import sys, random, collections as C

ROOT = sys.argv[1]
sys.path.insert(0, ROOT + "/src")
import compare as K

texts = [list(reversed(t)) for t in K.indus()]          # reading order (inferred)
freq = C.Counter(g for t in texts for g in t)

CLASSES = {
    "numerals (short strokes, rows)": ["3", "4", "5", "6", "7", "13", "14", "15", "16", "17", "18", "19", "27", "55"],
    "small ticks 1, 2": ["1", "2"],
    "long strokes 31-35": ["31", "32", "33", "35"],
}

def stats(ts, S):
    S = set(S); after, before = C.defaultdict(set), C.defaultdict(set)
    tok_a = tok_b = 0; first = last = mid = 0
    for t in ts:
        for i, g in enumerate(t):
            if g not in S: continue
            if i == 0: first += 1
            elif i == len(t) - 1: last += 1
            else: mid += 1
            if i + 1 < len(t) and t[i + 1] not in S: after[t[i + 1]].add(g); tok_a += 1
            if i > 0 and t[i - 1] not in S: before[t[i - 1]].add(g); tok_b += 1
    pa = sum(len(v) >= 2 for v in after.values()); pb = sum(len(v) >= 2 for v in before.values())
    return {"after_par": pa, "before_par": pb, "tok_after": tok_a, "tok_before": tok_b,
            "first": first, "middle": mid, "last": last, "after": after, "before": before}

def asym(s):  # positive = counted signs tend to FOLLOW the class in reading order
    return s["after_par"] - s["before_par"]

rng = random.Random(2026)
pool = [g for g in freq if not any(g in v for v in CLASSES.values())]
print("Reading order inferred: stored order reversed (jar sign text-final).\n")
for name, S in CLASSES.items():
    S = [g for g in S if g in freq]
    real = stats(texts, S)
    shuf = [asym(stats([rng.sample(t, len(t)) for t in texts], S)) for _ in range(300)]
    m = sum(shuf) / len(shuf); sd = (sum((x - m) ** 2 for x in shuf) / (len(shuf) - 1)) ** .5 or 1
    # frequency-matched random sets: for each member, a non-class sign with the nearest frequency
    ctrl = []
    for _ in range(300):
        pick = []
        for g in S:
            cand = sorted(pool, key=lambda x: abs(freq[x] - freq[g]))[:12]
            pick.append(rng.choice([c for c in cand if c not in pick] or cand))
        ctrl.append(asym(stats(texts, pick)))
    cm = sum(ctrl) / len(ctrl); csd = (sum((x - cm) ** 2 for x in ctrl) / (len(ctrl) - 1)) ** .5 or 1
    tot = real["first"] + real["middle"] + real["last"]
    print(f"== {name}: {len(S)} signs, {tot} occurrences")
    print(f"   position in reading order: first {real['first']/tot:.0%} · middle {real['middle']/tot:.0%} · last {real['last']/tot:.0%}")
    print(f"   signs taking >=2 different class members AFTER them (Y after 3, 4...): {real['after_par']}")
    print(f"   signs taking >=2 different class members BEFORE them (Y before 3, 4...): {real['before_par']}")
    print(f"   asymmetry {asym(real):+d} · shuffled-order null {m:+.1f} ± {sd:.1f} (z {(asym(real)-m)/sd:+.1f})"
          f" · frequency-matched other signs {cm:+.1f} ± {csd:.1f} (z {(asym(real)-cm)/csd:+.1f})")
    if name.startswith("numerals"):
        top = sorted(real["after"].items(), key=lambda kv: -len(kv[1]))[:8]
        print("   commonest signs right AFTER numerals (sign: numerals seen before it):",
              "; ".join(f"{y}: {','.join(sorted(v, key=int))}" for y, v in top))
        topb = sorted(real["before"].items(), key=lambda kv: -len(kv[1]))[:8]
        print("   commonest signs right BEFORE numerals:",
              "; ".join(f"{y}: {','.join(sorted(v, key=int))}" for y, v in topb))
    print()
