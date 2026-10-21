"""Step 2 toward the language: how predictable are the units at each end of a word and of a short phrase?
Suffixing languages put recurring endings last; stacking (agglutinative) languages make the last TWO or
more units predictable. Compared: Vedic Sanskrit (written syllables, Devanagari-style), Old Tamil
(aksharas), Santali (Munda; Ol Chiki syllables, from the Santali Wikipedia) and the Indus texts.
Entropies are divided by each corpus's own unit entropy so different inventories can be compared.
Usage: python3 -I src/step2_endings.py <study-root>"""
import sys, re, bz2, json, math, random, unicodedata, collections as C
import xml.etree.ElementTree as ET

ROOT = sys.argv[1]
sys.path.insert(0, ROOT + "/src")
import compare as K

# ---------- Sanskrit, written-syllable split: final consonants become their own unit (as with a virama) ----------
def sk_aksharas(word):
    w = unicodedata.normalize("NFC", word.lower().replace("ṁ", "ṃ")); ph, i = [], 0
    while i < len(w):
        two = w[i:i+2]
        if two in K.SK_C2 or two in ("ai", "au"): ph.append(two); i += 2
        else: ph.append(w[i]); i += 1
    out, onset = [], ""
    for p in ph:
        if p in K.SK_V: out.append(onset + p); onset = ""
        elif p in ("ṃ", "ḥ") and out: out[-1] += p
        elif p.isalpha() or p in K.SK_C2: onset += p
    if onset: out.append(onset + "·")          # word-final consonant(s), written with virama
    return out

def sanskrit_lines():
    for line in open(K.D + "compare/rv.txt", encoding="utf-8"):
        ws = [a for a in (sk_aksharas(w) for w in line.split()) if a]
        if ws: yield ws

def tamil_lines():
    k = json.load(open(K.D + "compare/thirukkural.json", encoding="utf-8"))["kural"]
    for x in k:
        for line in (x["Line1"], x["Line2"]):
            ws = [a for a in (K.aksharas(w) for w in line.split()) if a]
            if ws: yield ws

# ---------- Santali (Ol Chiki): vowel letters close a syllable; marks attach to the unit before ----------
OL_V = {chr(c) for c in (0x1C5A, 0x1C5F, 0x1C64, 0x1C69, 0x1C6E, 0x1C73)}
OL_MARK = {chr(c) for c in range(0x1C78, 0x1C7E)}
def ol_syllables(word):
    out, onset = [], ""
    for ch in word:
        if ch in OL_MARK:
            if onset: onset += ch
            elif out: out[-1] += ch
        elif ch in OL_V: out.append(onset + ch); onset = ""
        else: onset += ch
    if onset: out.append(onset + "·")
    return out

def santali_lines(max_words=60000):
    n = 0
    with bz2.open(K.D + "compare/satwiki-latest-pages-articles.xml.bz2", "rt", encoding="utf-8") as f:
        for _, el in ET.iterparse(f):
            if not el.tag.endswith("}page"): continue
            ns = el.find("{*}ns"); txt = el.find(".//{*}text")
            if ns is not None and ns.text == "0" and txt is not None and txt.text and not txt.text.startswith("#"):
                t = re.sub(r"\{\{.*?\}\}|<ref.*?</ref>|<[^>]+>|\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", txt.text, flags=re.S)
                for sent in re.split(r"[᱾᱿।.!?\n]+", t):
                    ws = re.findall(r"[ᱚ-ᱽ]+", sent)
                    ws = [s for s in (ol_syllables(w) for w in ws) if s]
                    if ws:
                        yield ws; n += len(ws)
                        if n >= max_words: return
            el.clear()

# ---------- measures ----------
def H(c):
    n = sum(c.values()); return -sum(v / n * math.log2(v / n) for v in c.values()) if n else float("nan")

def word_profile(lines):
    """Normalised entropy of the unit at each position of words with >= 3 units."""
    words = [w for l in lines for w in l if len(w) >= 3]
    base = H(C.Counter(u for w in words for u in w))
    pos = {"first": C.Counter(), "second": C.Counter(), "second-last": C.Counter(), "last": C.Counter()}
    for w in words:
        pos["first"][w[0]] += 1; pos["second"][w[1]] += 1; pos["second-last"][w[-2]] += 1; pos["last"][w[-1]] += 1
    return len(words), {k: H(v) / base for k, v in pos.items()}

lengths = [len(t) for t in K.indus()]
def phrase_texts(lines, rng, n=1902):
    seen = set()
    for ws in rng.sample(lines, len(lines)):
        k, t = rng.choice(lengths), []
        for w in ws:
            if t and len(t) + len(w) > k: break
            t += w
        seen.add(tuple(t))
    pool = sorted(seen); return [list(t) for t in rng.sample(pool, min(n, len(pool)))]

def phrase_profile(ts):
    base = H(C.Counter(u for t in ts for u in t)); out = {}
    for side in ("start", "end"):
        for d in range(3):
            c = C.Counter((t[d] if side == "start" else t[-1 - d]) for t in ts if len(t) > d + 1)
            out[f"{side}{'+' if side == 'start' else '-'}{d}"] = H(c) / base
    return out

rng = random.Random(2026)
corpora = {"Sanskrit (written syllables)": list(sanskrit_lines()),
           "Old Tamil (aksharas)": list(tamil_lines()),
           "Santali / Munda (Ol Chiki syllables)": list(santali_lines())}

print("## A. Inside words of 3+ units: entropy of each position ÷ the corpus's own unit entropy (lower = more predictable)\n")
print("| corpus | words | first | second | second-last | last |")
print("|---|---|---|---|---|---|")
for name, lines in corpora.items():
    n, p = word_profile(lines)
    print(f"| {name} | {n} | {p['first']:.2f} | {p['second']:.2f} | {p['second-last']:.2f} | {p['last']:.2f} |")

print("\n## B. Short phrases of whole words, cut to the Indus lengths (Indus in reading order, right to left)\n")
cols = ["start+0", "start+1", "start+2", "end-2", "end-1", "end-0"]
print("| corpus | " + " | ".join(cols) + " |"); print("|---" * (len(cols) + 1) + "|")
indus = [list(reversed(t)) for t in K.indus()]
p = phrase_profile(indus); print("| Indus | " + " | ".join(f"{p[c]:.2f}" for c in cols) + " |")
for name, lines in corpora.items():
    runs = [phrase_profile(phrase_texts(lines, random.Random(s))) for s in range(5)]
    print(f"| {name} | " + " | ".join(f"{sum(r[c] for r in runs)/5:.2f}" for c in cols) + " |")
print("\nSantali units sampled:", sum(len(w) for l in corpora['Santali / Munda (Ol Chiki syllables)'] for w in l),
      "· words:", sum(len(l) for l in corpora['Santali / Munda (Ol Chiki syllables)']))
