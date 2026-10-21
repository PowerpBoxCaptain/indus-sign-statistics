"""The 40 hand-drawn symbols of the pre-registered blind test, all with the same primitives and stroke.
python3 -I blind/symbols.py <study-root>  → blind/drawings.png (sheet for a sanity look, not for matching)"""
import math
from PIL import Image, ImageDraw

W, S = 200, 8          # canvas size, stroke width

def canvas():
    im = Image.new("L", (W, W), 255); return im, ImageDraw.Draw(im)

def L(d, *pts): d.line(pts, fill=0, width=S, joint="curve")
def E(d, box): d.ellipse(box, outline=0, width=S)
def A(d, box, a0, a1): d.arc(box, a0, a1, fill=0, width=S)
def P(d, pts): d.polygon(pts, outline=0, width=S)
def dot(d, x, y, r=7): d.ellipse((x - r, y - r, x + r, y + r), fill=0)

def spiral(d, cx, cy, turns=2.5, r0=6, r1=70):
    pts = []
    for i in range(200):
        t = i / 199; a = t * turns * 2 * math.pi; r = r0 + (r1 - r0) * t
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    L(d, *pts)

# ---------------- H, Hindu ----------------
def swastika(d):
    L(d, (100, 30), (100, 170)); L(d, (30, 100), (170, 100))
    L(d, (100, 30), (170, 30)); L(d, (170, 100), (170, 170)); L(d, (100, 170), (30, 170)); L(d, (30, 100), (30, 30))
def trishula(d):
    L(d, (100, 40), (100, 180)); L(d, (60, 40), (60, 80)); L(d, (140, 40), (140, 80))
    A(d, (60, 40, 140, 120), 0, 180); L(d, (85, 30), (100, 15), (115, 30))
def lotus(d):
    E(d, (80, 80, 120, 120))
    for k in range(8):
        a = k * math.pi / 4; cx, cy = 100 + 55 * math.cos(a), 100 + 55 * math.sin(a)
        pts = [(100 + 25 * math.cos(a + s), 100 + 25 * math.sin(a + s)) for s in (-.5, .5)]
        L(d, pts[0], (cx, cy), pts[1])
def chakra(d):
    E(d, (25, 25, 175, 175)); E(d, (88, 88, 112, 112))
    for k in range(8):
        a = k * math.pi / 4; L(d, (100 + 12 * math.cos(a), 100 + 12 * math.sin(a)), (100 + 75 * math.cos(a), 100 + 75 * math.sin(a)))
def shankha(d):
    spiral(d, 90, 95, 2.2, 5, 55); L(d, (145, 95), (175, 160), (95, 150))
def kalasha(d):
    E(d, (45, 80, 155, 175)); L(d, (75, 82), (75, 60), (125, 60), (125, 82))
    E(d, (80, 25, 120, 60)); L(d, (75, 60), (40, 40)); L(d, (125, 60), (160, 40))
def lingam(d):
    A(d, (70, 30, 130, 90), 180, 360); L(d, (70, 60), (70, 130)); L(d, (130, 60), (130, 130))
    E(d, (30, 115, 170, 165)); L(d, (170, 140), (195, 140))
def damaru(d):
    L(d, (50, 30), (150, 30), (110, 100), (150, 170), (50, 170), (90, 100), (50, 30))
    L(d, (90, 100), (40, 85)); L(d, (110, 100), (160, 115)); dot(d, 36, 84); dot(d, 164, 116)
def tripundra(d):
    for y in (65, 100, 135): L(d, (30, y), (170, y))
def yantra(d):
    E(d, (15, 15, 185, 185)); P(d, [(100, 30), (165, 140), (35, 140)]); P(d, [(100, 170), (165, 60), (35, 60)])

# ---------------- C1, Christian ----------------
def latin_cross(d): L(d, (100, 20), (100, 180)); L(d, (55, 65), (145, 65))
def celtic_cross(d): L(d, (100, 15), (100, 185)); L(d, (40, 75), (160, 75)); E(d, (65, 40, 135, 110))
def chi_rho(d): L(d, (90, 20), (90, 180)); A(d, (60, 20, 130, 80), 270, 90); L(d, (40, 70), (140, 170)); L(d, (140, 70), (40, 170))
def ichthys(d): A(d, (15, -36, 175, 124), 15, 135); A(d, (15, 76, 175, 236), 225, 345)   # two arcs crossing at ~90°: nose and tail
def anchor(d):
    L(d, (100, 45), (100, 170)); E(d, (85, 15, 115, 45)); L(d, (65, 70), (135, 70)); A(d, (35, 100, 165, 180), 0, 180)
    L(d, (35, 140), (45, 125)); L(d, (165, 140), (155, 125))
def chalice(d):
    A(d, (45, 0, 155, 100), 0, 180); L(d, (45, 50), (155, 50)); L(d, (100, 100), (100, 160)); L(d, (60, 165), (140, 165))
def fleur(d):
    A(d, (75, 20, 125, 120), 180, 360); L(d, (75, 70), (100, 20), (125, 70)); A(d, (20, 60, 90, 130), 270, 90)
    A(d, (110, 60, 180, 130), 90, 270); L(d, (60, 120), (140, 120)); L(d, (100, 120), (100, 180))
def crown(d): L(d, (35, 150), (35, 60), (70, 105), (100, 50), (130, 105), (165, 60), (165, 150), (35, 150))
def heart(d):
    A(d, (25, 40, 105, 120), 135, 360); A(d, (95, 40, 175, 120), 180, 45); L(d, (37, 108), (100, 175), (163, 108))
def trefoil(d):
    for cx, cy in ((100, 60), (65, 115), (135, 115)): E(d, (cx - 35, cy - 35, cx + 35, cy + 35))

# ---------------- C2, Chinese ----------------
def taijitu(d):
    E(d, (20, 20, 180, 180)); A(d, (60, 20, 140, 100), 270, 90); A(d, (60, 100, 140, 180), 90, 270)
    dot(d, 100, 60, 9); E(d, (90, 130, 110, 150))
def qian(d):
    for y in (60, 100, 140): L(d, (35, y), (165, y))
def kun(d):
    for y in (60, 100, 140): L(d, (35, y), (88, y)); L(d, (112, y), (165, y))
def ding(d):
    A(d, (35, 40, 165, 150), 0, 180); L(d, (35, 95), (165, 95)); L(d, (60, 140), (50, 185)); L(d, (140, 140), (150, 185))
    L(d, (100, 150), (100, 185)); P(d, [(50, 95), (50, 60), (70, 60), (70, 95)]); P(d, [(130, 95), (130, 60), (150, 60), (150, 95)])
def coin(d): E(d, (20, 20, 180, 180)); P(d, [(75, 75), (125, 75), (125, 125), (75, 125)])
def endless_knot(d):
    for k in range(4):
        L(d, (40 + 40 * k, 40), (40 + 40 * k, 160)); L(d, (40, 40 + 40 * k), (160, 40 + 40 * k))
    A(d, (15, 15, 65, 65), 180, 270); A(d, (135, 135, 185, 185), 0, 90)
def cloud(d): spiral(d, 70, 110, 1.5, 4, 35); spiral(d, 130, 90, 1.5, 4, 35); L(d, (35, 110), (20, 160), (180, 160), (165, 90))
def gourd(d): E(d, (70, 25, 130, 85)); E(d, (45, 75, 155, 180)); L(d, (100, 25), (110, 5))
def fan(d):
    A(d, (15, 15, 185, 185), 200, 340)
    for a in (200, 235, 270, 305, 340):
        r = math.radians(a); L(d, (100, 160), (100 + 85 * math.cos(r), 100 + 85 * math.sin(r)))
def bagua(d):
    P(d, [(100 + 80 * math.cos(math.radians(22.5 + 45 * k)), 100 + 80 * math.sin(math.radians(22.5 + 45 * k))) for k in range(8)])
    E(d, (75, 75, 125, 125))

# ---------------- C3, Egyptian ----------------
def ankh(d): E(d, (70, 15, 130, 85)); L(d, (100, 85), (100, 185)); L(d, (45, 95), (155, 95))
def was(d): L(d, (100, 40), (100, 185)); L(d, (100, 40), (130, 20), (145, 40)); L(d, (100, 185), (85, 170)); L(d, (100, 185), (115, 170))
def djed(d):
    L(d, (85, 60), (85, 185)); L(d, (115, 60), (115, 185)); L(d, (85, 60), (100, 20), (115, 60))
    for y in (70, 85, 100, 115): L(d, (55, y), (145, y))
def eye(d):
    A(d, (20, 50, 180, 150), 180, 360); A(d, (20, 50, 180, 150), 0, 180); dot(d, 100, 100, 18)
    L(d, (100, 150), (100, 185), (80, 185)); L(d, (60, 145), (70, 185))
def scarab(d):
    E(d, (70, 50, 130, 160)); E(d, (80, 25, 120, 55)); L(d, (100, 60), (100, 155))
    for y in (75, 105, 135): L(d, (70, y), (35, y - 15)); L(d, (130, y), (165, y - 15))
def shen(d): E(d, (40, 20, 160, 140)); L(d, (40, 165), (160, 165)); L(d, (85, 140), (85, 165)); L(d, (115, 140), (115, 165))
def sun_disc(d): E(d, (50, 50, 150, 150)); dot(d, 100, 100, 10)
def feather(d): L(d, (100, 185), (100, 20)); A(d, (55, 15, 145, 185), 270, 90); A(d, (55, 15, 145, 185), 90, 270)
def crook(d): L(d, (110, 185), (110, 60)); A(d, (60, 15, 160, 105), 180, 360); L(d, (60, 60), (70, 80))
def pyramid(d): P(d, [(100, 30), (180, 165), (20, 165)]); L(d, (100, 30), (120, 165))

SETS = {
    "H Hindu": [swastika, trishula, lotus, chakra, shankha, kalasha, lingam, damaru, tripundra, yantra],
    "C1 Christian": [latin_cross, celtic_cross, chi_rho, ichthys, anchor, chalice, fleur, crown, heart, trefoil],
    "C2 Chinese": [taijitu, qian, kun, ding, coin, endless_knot, cloud, gourd, fan, bagua],
    "C3 Egyptian": [ankh, was, djed, eye, scarab, shen, sun_disc, feather, crook, pyramid],
}

def render(f):
    im, d = canvas(); f(d); return im

if __name__ == "__main__":
    import sys
    from PIL import ImageFont
    root = sys.argv[1]
    lab = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    C = 110; sheet = Image.new("L", (10 * C + 160, 4 * (C + 10)), 255); dr = ImageDraw.Draw(sheet)
    for r, (name, fs) in enumerate(SETS.items()):
        dr.text((5, r * (C + 10) + 45), name, font=lab, fill=0)
        for c, f in enumerate(fs):
            sheet.paste(render(f).resize((90, 90)), (160 + c * C, r * (C + 10) + 5))
            dr.text((160 + c * C, r * (C + 10) + 97), f.__name__, font=lab, fill=80)
    sheet.save(root + "/blind/drawings.png")
    print("drawn:", sum(map(len, SETS.values())))
