# Blind test: do later Hindu sacred symbols resemble Indus signs more than other traditions' symbols do?

Written and committed **before** any matching was run. In the private study repository where the
work was done, this file, `symbols.py` and `drawings.png` were committed at 2026-10-21 15:56:31 +0530,
and `match.py` with its single run at 15:58:26 +0530. This public repository received them together,
so its own log cannot show that order; the times above are stated, not provable here.

Public copy, two wording changes made after the run (the rules below are unchanged): the opening
words of the Question section, and this paragraph, which replaced "see the git log".

## Question
The question, 21 Oct 2026: if we add Hindu mythology symbols, do they share a common theme with
the Indus script? This test asks the narrow, checkable part: **shape resemblance** between later
Hindu sacred symbols and the 591 Indus signs of the corpus font, beyond what symbols of unrelated
traditions show.

## Sets (fixed now; 10 each; chosen as each tradition's well-known sacred or auspicious symbols that
can be drawn as a line figure)
- **H, Hindu:** swastika, trishula (trident), lotus (eight petals, top view), chakra (eight-spoked wheel),
  shankha (conch spiral), kalasha (pot with leaves), lingam on yoni base, damaru (hourglass drum),
  tripundra (three horizontal lines), yantra (two interlaced triangles in a circle).
- **C1, Christian:** Latin cross, Celtic cross, chi-rho, ichthys fish, anchor, chalice, fleur-de-lis,
  crown, heart, trefoil.
- **C2, Chinese:** taijitu (yin-yang), trigram qian (three lines), trigram kun (three broken lines),
  ding cauldron, cash coin, endless knot, cloud scroll, gourd, fan, bagua octagon.
- **C3, Egyptian:** ankh, was-sceptre, djed pillar, eye, scarab, shen ring, sun disc, feather, crook,
  pyramid.
- **Font baselines (not drawn by us):** 10 random signs each from the Noto fonts for Egyptian
  hieroglyphs, Anatolian hieroglyphs and Linear A, seed 2026, 200 draws per font.

Every symbol in H, C1, C2 and C3 is drawn by `symbols.py` with the same primitives (lines, arcs,
ellipses, polygons) and the same stroke width.

## Matcher (fixed now)
1. Each image is binarised, cropped to its ink, scaled to fit 64×64 keeping its aspect ratio, and
   thinned to a one-pixel skeleton (Zhang–Suen).
2. Distance between two shapes = symmetric chamfer distance between their skeleton point sets
   (mean nearest-point distance, both directions, averaged), in pixels.
3. A symbol's score = the smallest distance to any of the 591 Indus signs, also trying each Indus
   sign mirrored left-right. Lower = closer resemblance.

## Decision rule (fixed now)
- Primary statistic: mean score of H against the mean of C1 ∪ C2 ∪ C3 (30 symbols).
  One-sided permutation test, 10,000 shuffles of the 40 labels, seed 2026.
- **H1 (Hindu symbols resemble Indus signs more) is supported only if** p < 0.05 **and** H's mean is
  lower than each of C1, C2 and C3 separately.
- Otherwise the result is reported as "no excess resemblance found", which is not proof of no link.
- Secondary, reported only: H against the font baselines; each symbol's closest Indus sign, shown as
  pictures; each symbol's skeleton length (simple shapes match more easily, so this confound is
  shown, not corrected).

## Known weaknesses, stated in advance
- The drawer (an AI assistant) had already seen the Indus sign sheets. Committing the drawings
  before matching limits, but does not remove, that bias.
- Hand-drawn symbols are simpler than real carvings; simple figures (lines, circles) find close
  matches anywhere.
- Shape is not meaning. A match says two drawings look alike, nothing more.
- Seal pictures (the animals and scenes) are not in the data; this tests the signs only.
