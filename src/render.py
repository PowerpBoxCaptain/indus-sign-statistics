"""Render Indus sign shapes from the corpus font (sk_indus_script-webfont.ttf, GLYPH table maps id -> codepoint).
Sheets: the 12 context groups, the context-neighbour pairs, the 40 commonest signs.
Usage: python3 -I src/render.py <study-root>"""
import sys, io, re, contextlib, html
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = sys.argv[1]
sys.argv = [sys.argv[0], ROOT]
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(ROOT + "/src/grammar_groups.py").read())       # gives ind, keep, S, freq, groups, cluster, vectors

sql = open(ROOT + "/data/indus/population-script.sql", encoding="utf-8", errors="replace").read()
block = re.search(r"INSERT INTO GLYPH \(GLYPHID, UNICODE\) VALUES(.*?)\n\s*\n", sql, re.S).group(1)
cp = {gid: chr(int(m.group(1), 16)) for gid, u in K.tuples(block) if (m := re.fullmatch(r"&#x([0-9A-Fa-f]+);", u))}

SIGN = ImageFont.truetype(ROOT + "/data/indus/sk_indus_script-webfont.ttf", 64)
LAB = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
BIG = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
CELL, PAD = 92, 8

def glyph(gid):
    im = Image.new("L", (CELL, CELL - 20), 255)
    ch = cp.get(gid)
    if ch: ImageDraw.Draw(im).text(((CELL) // 2, (CELL - 20) // 2), ch, font=SIGN, fill=0, anchor="mm")
    return im

blank = Image.new("L", (CELL, CELL - 20), 255)
NOTDEF = Image.new("L", (CELL, CELL - 20), 255)
ImageDraw.Draw(NOTDEF).text((CELL // 2, (CELL - 20) // 2), "", font=SIGN, fill=0, anchor="mm")

def cell(gid, note=""):
    c = Image.new("L", (CELL, CELL), 255)
    g = glyph(gid)
    if gid not in cp or np.array_equal(np.asarray(g), np.asarray(blank)) or np.array_equal(np.asarray(g), np.asarray(NOTDEF)):
        ImageDraw.Draw(g).text((CELL // 2, (CELL - 20) // 2), "?", font=BIG, fill=120, anchor="mm")
    c.paste(g, (0, 0))
    ImageDraw.Draw(c).text((CELL // 2, CELL - 10), f"{gid}{note}", font=LAB, fill=60, anchor="mm")
    return c

def sheet(rows, path, width=12):
    """rows: list of (title, [(gid, note), ...])."""
    lines = []
    for title, items in rows:
        lines.append(("T", title))
        for i in range(0, len(items), width): lines.append(("C", items[i:i + width]))
    h = sum(26 if k == "T" else CELL for k, _ in lines) + 2 * PAD
    im = Image.new("L", (width * CELL + 2 * PAD, h), 255); d = ImageDraw.Draw(im); y = PAD
    for k, v in lines:
        if k == "T": d.text((PAD, y + 4), v, font=BIG, fill=0); y += 26
        else:
            for j, (gid, note) in enumerate(v): im.paste(cell(gid, note), (PAD + j * CELL, y))
            y += CELL
    im.save(path)

first = C.Counter(t[0] for t in ind if len(t) > 1); last = C.Counter(t[-1] for t in ind if len(t) > 1)
def tag(s):
    n = freq[s]; f, l = first[s] / n, last[s] / n
    return " ◂" if f > .5 else " ▸" if l > .5 else ""

out = ROOT + "/results/"
rows = []
for gi, grp in enumerate(sorted(groups, key=len, reverse=True), 1):
    mem = sorted(grp, key=lambda i: -freq[keep[i]])
    rows.append((f"G{gi} · {len(grp)} signs · by frequency  (◂ mostly at stored start, ▸ mostly at stored end)",
                 [(keep[i], tag(keep[i])) for i in mem]))
sheet(rows, out + "groups.png")

codes = np.array([int(k) for k in keep]); pairs = []
for i in range(len(keep)):
    j = [j for j in np.argsort(-S[i]) if j != i][0]
    if abs(codes[i] - codes[j]) <= 10: pairs.append((keep[i], keep[j], S[i, j]))
pairs.sort(key=lambda p: -p[2])
sheet([("Context-neighbour pairs with nearby codes (sign → its closest context match)",
        [x for a, b, s in pairs for x in ((a, ""), (b, f" ·{s:.2f}"))])], out + "neighbour-pairs.png", width=12)

top = [g for g, _ in C.Counter(x for t in ind for x in t).most_common(40)]
sheet([("40 commonest signs (distinct texts), with count", [(g, f" ({freq[g]})") for g in top])], out + "top40.png", width=10)

missing = [g for g in set(x for t in ind for x in t) if g not in cp]
print(f"glyph map {len(cp)} ids · signs in corpus without a glyph: {len(missing)}")
print(f"pairs drawn {len(pairs)}")
