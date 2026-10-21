"""Is there a numbered-name slot? Fixed number compounds (a sign that almost always takes one number value,
e.g. 7+585) against counted pairs (a sign that takes many values, e.g. n+390). Checks: position in the
text, whether two compounds share a text, and the signs around them. Reading order = stored reversed.
Usage: python3 -I src/numbered_names.py <study-root>"""
import sys, collections as C

sys.path.insert(0, sys.argv[1] + "/src")
import compare as K

VALUE = {"3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "13": 3, "14": 4, "15": 5, "16": 6, "17": 7,
         "18": 8, "19": 9, "27": 7, "55": 9}
texts = [list(t) for t in sorted({tuple(reversed(t)) for t in K.indus()})]

pairs = C.defaultdict(list)            # partner sign -> list of (text index, position, value)
for ti, t in enumerate(texts):
    for i in range(1, len(t)):
        if t[i - 1] in VALUE and t[i] not in VALUE:
            pairs[t[i]].append((ti, i - 1, VALUE[t[i - 1]]))

fixed, counted = {}, {}
for y, occ in pairs.items():
    if len(occ) < 5: continue
    vc = C.Counter(v for _, _, v in occ); top, n = vc.most_common(1)[0]
    if n / len(occ) >= 0.9: fixed[y] = (top, occ)
    elif len(vc) >= 3: counted[y] = occ
print("fixed compounds (one value in >= 90% of uses):",
      ", ".join(f"{fixed[y][0]}+{y} ({len(fixed[y][1])})" for y in sorted(fixed, key=lambda k: -len(fixed[k][1]))))
print("counted signs (3+ values):", ", ".join(f"{y} ({len(o)})" for y, o in sorted(counted.items(), key=lambda kv: -len(kv[1]))))

def where(group):
    fs, fe, lens = C.Counter(), C.Counter(), []
    for y, occ in group.items():
        for ti, p, _ in occ:
            L = len(texts[ti]); lens.append(L)
            fs[min(p, 3)] += 1; fe[min(L - (p + 2), 3)] += 1          # pair occupies p and p+1
    n = sum(fs.values())
    lab = {0: "0", 1: "1", 2: "2", 3: "3+"}
    return n, sum(lens) / len(lens), " ".join(f"{lab[k]}:{fs[k]/n:.0%}" for k in sorted(fs)), " ".join(f"{lab[k]}:{fe[k]/n:.0%}" for k in sorted(fe))

print("\n== 1. Position (signs before the pair · signs after the pair)")
for name, grp in (("fixed compounds", {y: o for y, (_, o) in fixed.items()}), ("counted pairs", counted)):
    n, L, s, e = where(grp)
    print(f"   {name:15} n={n:3} · mean text length {L:.1f} · before: {s} · after: {e}")

print("\n== 2. Do two different fixed compounds share a text?")
has = C.defaultdict(set)
for y, (_, occ) in fixed.items():
    for ti, _, _ in occ: has[ti].add(y)
both = [ti for ti, ys in has.items() if len(ys) > 1]
N = len(texts); rates = {y: len({ti for ti, _, _ in o}) / N for y, (_, o) in fixed.items()}
ys = list(rates); exp = sum(rates[a] * rates[b] * N for i, a in enumerate(ys) for b in ys[i + 1:])
print(f"   texts with 2+ different fixed compounds: {len(both)} (expected if independent: {exp:.2f})",
      "; ".join("-".join(texts[ti]) for ti in both[:5]))

print("\n== 3. What surrounds them (sign just before · sign just after)")
for name, grp in (("fixed compounds", {y: o for y, (_, o) in fixed.items()}), ("counted pairs", counted)):
    before, after = C.Counter(), C.Counter()
    for y, occ in grp.items():
        for ti, p, _ in occ:
            t = texts[ti]
            before[t[p - 1] if p > 0 else "(start)"] += 1
            after[t[p + 2] if p + 2 < len(t) else "(end)"] += 1
    n = sum(before.values())
    print(f"   {name:15} before: " + ", ".join(f"{k} {v/n:.0%}" for k, v in before.most_common(5)))
    print(f"   {'':15} after:  " + ", ".join(f"{k} {v/n:.0%}" for k, v in after.most_common(5)))

print("\n== 4. Frames: for each fixed compound, the (sign before, sign after) frame, and what else fills that frame")
for y, (v, occ) in sorted(fixed.items(), key=lambda kv: -len(kv[1][1])):
    frames = C.Counter()
    for ti, p, _ in occ:
        t = texts[ti]
        frames[(t[p - 1] if p > 0 else "^", t[p + 2] if p + 2 < len(t) else "$")] += 1
    (fb, fa), fn = frames.most_common(1)[0]
    fillers = C.Counter()
    for t in texts:
        tt = ["^"] + t + ["$"]
        for i in range(len(tt)):
            if tt[i] != fb: continue
            for j in range(i + 2, min(i + 5, len(tt))):
                if tt[j] == fa: fillers["-".join(tt[i + 1:j])] += 1; break
    others = [(k, c) for k, c in fillers.most_common() if k != f"{[g for g, val in VALUE.items() if val == v][0]}-{y}"]
    print(f"   {v}+{y}: commonest frame {fb} _ {fa} ({fn} of {len(occ)}); other fillers of that frame: "
          + (", ".join(f"{k} ({c})" for k, c in others[:6]) or "none"))
