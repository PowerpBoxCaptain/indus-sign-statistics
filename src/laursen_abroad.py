"""Script abroad, on published sources only: Gulf Type seal inscriptions as drawn in Laursen 2010, Fig. 11
(transcribed by us into feature tokens, abroad/laursen-fig11-transcription.csv), against this repository's
public dataset. Reading order is right to left (the figure shows impressions; the dataset is reversed from
storage order). Tests: how often a text OPENS with the "twins" sign (two human figures side by side,
ICIT 91; Parpola's no. 16) and how often it ENDS with the jar (ICIT 740), with hypergeometric p-values.
Usage: python3 -I src/laursen_abroad.py <repo-root>"""
import sys, csv
from math import comb

ROOT = sys.argv[1]
sys.path.insert(0, ROOT + "/src")
import compare as K

rows = list(csv.DictReader(open(ROOT + "/abroad/laursen-fig11-transcription.csv", encoding="utf-8")))
home = [tuple(reversed(t)) for t in K.indus()]
H = len(home)
h_tw = sum(t[0] == "91" for t in home); h_jar = sum(t[-1] == "740" for t in home)

def p_ge(k, n, K_, N): return sum(comb(K_, i) * comb(N - K_, n - i) for i in range(k, min(n, K_) + 1)) / comb(N, n)
def p_le(k, n, K_, N): return sum(comb(K_, i) * comb(N - K_, n - i) for i in range(0, k + 1)) / comb(N, n)

print(f"Home baseline (this repository's dataset, {H} distinct texts, reading order): "
      f"open with twins {h_tw} ({h_tw/H:.1%}); end with the jar {h_jar} ({h_jar/H:.1%})")
for name, use in (("Gulf Type seals found abroad", "abroad"), ("Gulf Type seals found in the Indus Valley", "home-find")):
    g = [r for r in rows if r["use"] == use]; n = len(g)
    tw = sum(r["first"] == "TW" for r in g); jar = sum(r["last"] == "JAR?" for r in g)
    print(f"\n{name}: {n} inscriptions (Laursen 2010, Fig. 11)")
    print(f"   open with twins: {tw} ({tw/n:.0%}) · p(>= {tw} if like home) = {p_ge(tw, n, h_tw, H + n):.2g}")
    print(f"   end with a jar-like sign: {jar} ({jar/n:.0%}) · p(<= {jar} if like home) = {p_le(jar, n, h_jar, H + n):.2g}")
    hc = [r for r in g if r["confidence"] != "low"]
    print(f"   medium/high-confidence readings only ({len(hc)}): twins first {sum(r['first']=='TW' for r in hc)}, "
          f"jar-like last {sum(r['last']=='JAR?' for r in hc)}")
print(f"\nExcluded from the tests: {', '.join(r['seal'] for r in rows if r['use']=='exclude')} (Linear Elamite, no text, pictorial)")
