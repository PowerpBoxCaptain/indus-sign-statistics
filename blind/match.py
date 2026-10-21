"""Matcher and decision rule exactly as in PREREGISTRATION.md (written after it, run once).
Usage: python3 -I blind/match.py <study-root>  → blind/result.txt, blind/matches.png"""
import sys, re, random, unicodedata
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = sys.argv[1]
sys.path.insert(0, ROOT + "/src"); sys.path.insert(0, ROOT + "/blind")
import compare as K
import symbols as SYM

N = 64
FONTS = "/usr/share/fonts/truetype/noto/"

def norm(im):
    """Binarise, crop to ink, fit in N×N keeping aspect, thin to a skeleton; return points or None."""
    a = np.asarray(im.convert("L")) < 128
    ys, xs = np.nonzero(a)
    if len(xs) < 5: return None
    crop = Image.fromarray(((~a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]) * 255).astype(np.uint8))
    w, h = crop.size; s = (N - 4) / max(w, h)
    crop = crop.resize((max(1, round(w * s)), max(1, round(h * s))), Image.BILINEAR)
    c = Image.new("L", (N, N), 255); c.paste(crop, ((N - crop.size[0]) // 2, (N - crop.size[1]) // 2))
    sk = zhang_suen(np.asarray(c) < 128)
    p = np.argwhere(sk)
    return p.astype(float) if len(p) >= 3 else None

def zhang_suen(img):
    img = img.copy().astype(np.uint8)
    changed = True
    while changed:
        changed = False
        for step in (0, 1):
            P = np.pad(img, 1)
            p2, p3, p4, p5 = P[:-2, 1:-1], P[:-2, 2:], P[1:-1, 2:], P[2:, 2:]
            p6, p7, p8, p9 = P[2:, 1:-1], P[2:, :-2], P[1:-1, :-2], P[:-2, :-2]
            nb = [p2, p3, p4, p5, p6, p7, p8, p9]
            B = sum(n.astype(int) for n in nb)
            seq = nb + [p2]
            A = sum(((seq[i] == 0) & (seq[i + 1] == 1)).astype(int) for i in range(8))
            if step == 0: c1, c2 = p2 * p4 * p6, p4 * p6 * p8
            else: c1, c2 = p2 * p4 * p8, p2 * p6 * p8
            rm = (img == 1) & (B >= 2) & (B <= 6) & (A == 1) & (c1 == 0) & (c2 == 0)
            if rm.any(): img[rm] = 0; changed = True
    return img.astype(bool)

def chamfer(a, b):
    d = np.sqrt(((a[:, None, :] - b[None, :, :]) ** 2).sum(-1))
    return (d.min(1).mean() + d.min(0).mean()) / 2

def glyph_img(font, ch, size=150):
    im = Image.new("L", (200, 200), 255)
    ImageDraw.Draw(im).text((100, 100), ch, font=font, fill=0, anchor="mm")
    return im

# ---- Indus signs from the corpus font, plus left-right mirrors ----
sql = open(ROOT + "/data/indus/population-script.sql", encoding="utf-8", errors="replace").read()
block = re.search(r"INSERT INTO GLYPH \(GLYPHID, UNICODE\) VALUES(.*?)\n\s*\n", sql, re.S).group(1)
cp = {gid: chr(int(m.group(1), 16)) for gid, u in K.tuples(block) if (m := re.fullmatch(r"&#x([0-9A-Fa-f]+);", u))}
corpus = {g for t in K.indus() for g in t}
ifont = ImageFont.truetype(ROOT + "/data/indus/sk_indus_script-webfont.ttf", 150)
indus = []
for gid in sorted(corpus, key=int):
    if gid not in cp: continue
    im = glyph_img(ifont, cp[gid]); p = norm(im)
    if p is None: continue
    indus.append((gid, p, im))
    pm = p.copy(); pm[:, 1] = N - 1 - pm[:, 1]
    indus.append((gid + "m", pm, im.transpose(Image.FLIP_LEFT_RIGHT)))
n_signs = len({g.rstrip("m") for g, _, _ in indus})

def score(img):
    p = norm(img)
    best = min(((chamfer(p, q), g, im) for g, q, im in indus), key=lambda x: x[0])
    return best, len(p)

# ---- the 40 drawn symbols ----
rows = []
for set_name, fs in SYM.SETS.items():
    for f in fs:
        img = SYM.render(f); (d, g, gim), n = score(img)
        rows.append((set_name, f.__name__, d, g, n, img, gim))

out = []
P = lambda s="": out.append(s)
P(f"Indus signs matched: {n_signs} (of 591 in the corpus; the rest have no glyph), each also mirrored")
P("\n| set | symbol | best distance (px) | closest Indus sign | skeleton length |")
P("|---|---|---|---|---|")
for s, nm, d, g, n, _, _ in rows:
    P(f"| {s} | {nm} | {d:.2f} | {g.rstrip('m')}{' (mirrored)' if g.endswith('m') else ''} | {n} |")

H = np.array([r[2] for r in rows if r[0].startswith("H")])
Cs = {s: np.array([r[2] for r in rows if r[0] == s]) for s in SYM.SETS if not s.startswith("H")}
Call = np.concatenate(list(Cs.values()))
obs = H.mean() - Call.mean()
rng = np.random.default_rng(2026); allv = np.concatenate([H, Call]); hits = 0
for _ in range(10000):
    p = rng.permutation(allv); hits += (p[:10].mean() - p[10:].mean()) <= obs
pval = (hits + 1) / 10001
P("\n## Primary statistic")
P(f"mean distance H {H.mean():.2f} · controls (C1∪C2∪C3) {Call.mean():.2f} · difference {obs:+.2f} px")
for s, v in Cs.items(): P(f"  {s}: {v.mean():.2f}")
P(f"one-sided permutation p = {pval:.4f} (10,000 shuffles, seed 2026; small difference = H closer)")
supported = pval < 0.05 and all(H.mean() < v.mean() for v in Cs.values())
P(f"DECISION (pre-registered rule): {'H1 SUPPORTED' if supported else 'no excess resemblance found'}")

# ---- secondary: font baselines (signs not drawn by us) ----
P("\n## Secondary: font baselines (10 random signs, 200 draws per font, seed 2026)")
r = random.Random(2026)
for fname, lo, hi in (("NotoSansEgyptianHieroglyphs-Regular.ttf", 0x13000, 0x1342F),
                      ("NotoSansAnatolianHieroglyphs-Regular.ttf", 0x14400, 0x14646),
                      ("NotoSansLinearA-Regular.ttf", 0x10600, 0x10767)):
    f = ImageFont.truetype(FONTS + fname, 150)
    cands = [c for c in range(lo, hi + 1) if unicodedata.name(chr(c), "")]
    pool = []
    for c in r.sample(cands, min(120, len(cands))):
        im = glyph_img(f, chr(c))
        if norm(im) is not None: pool.append(score(im)[0][0])
    means = [np.mean(r.sample(pool, 10)) for _ in range(200)]
    pct = 100 * np.mean(np.array(means) <= H.mean())
    P(f"  {fname.split('-')[0]}: pool {len(pool)} signs, mean of 10-sign draws {np.mean(means):.2f} ± {np.std(means):.2f}; "
      f"H's mean {H.mean():.2f} is closer than {100 - pct:.0f}% of draws")

P("\n## Confound: skeleton length vs distance (all 40)")
L = np.array([r[4] for r in rows]); D = np.array([r[2] for r in rows])
P(f"  correlation r = {np.corrcoef(L, D)[0, 1]:.2f} (negative = simpler drawings land closer... positive = the reverse)")
open(ROOT + "/blind/result.txt", "w").write("\n".join(out) + "\n"); print("\n".join(out))

# ---- picture: each symbol beside its closest Indus sign ----
lab = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
C = 80; sheet = Image.new("L", (10 * 2 * C + 40, 4 * (C + 30)), 255); dr = ImageDraw.Draw(sheet)
for i, (s, nm, d, g, n, img, gim) in enumerate(rows):
    row, col = divmod(i, 10); x, y = 20 + col * 2 * C, row * (C + 30) + 5
    sheet.paste(img.resize((C - 6, C - 6)), (x, y)); sheet.paste(gim.resize((C - 6, C - 6)), (x + C - 6, y))
    dr.text((x, y + C - 4), f"{nm[:12]} → {g.rstrip('m')}", font=lab, fill=0)
    dr.text((x, y + C + 10), f"{d:.2f} px", font=lab, fill=90)
sheet.save(ROOT + "/blind/matches.png")
