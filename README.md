# Indus sign statistics

A small, reproducible look at the structure of the Indus script (c. 2600–1900 BCE): how its signs are
distributed, where they sit in a text, how it compares with real languages and with a non-linguistic
code cut to the same size, and which signs keep the same company.

**This is not a decipherment.** No sign is given a sound or a meaning here. Every number below is
computed from the data, and every reading of any sign stays open.

Commissioned and directed by Capt. Anil Sharma; implementation with an AI assistant (Claude, Anthropic).

![Context-neighbour pairs](results/neighbour-pairs.png)

## Findings

All figures come from `results/` and are rebuilt by `./run.sh`.

1. **Corpus.** 2,543 inscribed objects, which reduce to 1,902 distinct sign sequences once repeated
   texts (multiple impressions, tablet series) are merged. 591 sign types; mean length 4.65 signs,
   longest 17. 36% of sign types occur only once, and the 10 commonest signs make up a third of all
   occurrences.
2. **Signs keep places.** One sign (code 740, the "jar") makes up about 11% of all occurrences and
   stands at the same end of a text in 70% of its uses. It almost never stands at the other end.
   Several other signs are just as tied to one end or to the middle.
3. **Between a language and a code.** Against same-size samples of Vedic Sanskrit (syllables),
   Old Tamil (aksharas), English (words) and chess openings (moves):
   - Indus signs are more tied to their position than any of the three languages, about as much as
     chess moves (position information 0.36, against 0.10–0.22 for the languages and 0.33 for chess).
   - Once position is held fixed, the order of signs still carries structure at the level of Old
     Tamil (22% below a slot-preserving shuffle, against 24% for Tamil, 18% for Sanskrit, 12% for
     English and 27% for chess).
   - Signs rarely repeat within a text (4.4% of texts), close to English words (4.6%) and below the
     syllable scripts (8–13%). This fits signs that stand for words more than for single sounds.
4. **One very predictable end.** At one end of a text five signs fill 59% of the slot, led by the jar.
   Old Tamil phrases show a similarly predictable end (their recurring suffixes). The Indus pattern
   fits a closing marker such as a suffix, but a title or a classifier would produce the same shape,
   and so does the opening of a chess game.
5. **Signs that look alike behave alike.** Grouping signs by the neighbours they keep, 27 of 94
   common signs have as their closest match a sign with a catalogue code within 10 of their own,
   against 2.2 expected by chance (p ≈ 0.002, 500 shuffles). The catalogue numbers group signs by
   shape, and the rendered pairs show the same shape families: stroke counts 3/4/5 (number-like), the
   fish with and without added marks, cone, branch, jar and figure variants. Modifiers change a sign
   without moving it out of its slot.

6. **The text barely depends on the picture.** Pairing each distinct text with the animal carved on
   its object (the dataset's own iconography labels; six motifs with at least 25 texts), the
   sign-motif mutual information is 0.188 bits against 0.175 ± 0.007 for shuffled motifs, only
   1.9 sd above chance. The label "Bull1" alone carries 913 of the 1,134 texts (most likely the one-horned bull, the commonest
   seal animal; the dump does not define its labels). Picture and
   text carry largely separate information, as expected if the animal is an emblem and the text a
   name or title.

7. **Later Hindu sacred symbols do not resemble the signs more than other traditions' symbols do.**
   A pre-registered blind test ([`blind/PREREGISTRATION.md`](blind/PREREGISTRATION.md)) drew 10 Hindu
   sacred symbols and 10 each from Christian, Chinese and Egyptian tradition in one line style, and
   let a computer find each one's closest Indus sign by skeleton shape. Mean distance: Hindu 2.30 px,
   Christian 2.27, Chinese 2.28, Egyptian 1.98; one-sided permutation p = 0.73. Under the rule fixed
   in advance this is **no excess resemblance found**. Random signs from real pictographic scripts
   match about as well. Simple shapes (a circle with a cross, three lines) find look-alikes in every
   tradition ([`blind/matches.png`](blind/matches.png)). This tests the script's signs only: the seal
   pictures, where the scholarly case for continuity rests, are not in the data.

8. **The pictures follow fixed rules, and some seals carry no writing at all.** 202 seals were coded
   by eye from the photographic plates of the *Corpus of Indus Seals and Inscriptions*, vol. 1
   (Joshi & Parpola 1987), 75 from Mohenjo-daro, 87 from Harappa and 40 from Lothal
   ([`results/seal-coding-202.csv`](results/seal-coding-202.csv)). The cult stand appears only
   before the one-horned bull (50 of 50 where readable); the trough only before bison, buffalo and
   rhinoceros (14 of 14). Swastika seals (25 of 25) and geometric seals (14 of 14) never carry text;
   animal seals and picture-less seals almost always do. Several Lothal seals have text along the top
   and an empty field below, as if the text were cut first. The pages were chosen for variety, so
   this is not a random sample of all seals, and the coding is one person's reading of photographs.

9. **Seal texts are individual, and the animal does not follow the text.** Of 1,469 seals with text,
   88% carry a text found on no other object, while 65% of tablets share their text with another
   tablet, as moulded series would. Of 40 texts found on two or more seals, 82% keep the same animal
   on every copy, but shuffling the animal labels gives 84% ± 2% (the one-horned bull is 85% of
   seals), so a text does not stay with its animal more than chance; 7 texts appear with different
   animals, for example on a one-horned-bull seal and an elephant seal. No part of the text (opening
   sign, closing sign, middle) is clearly tied to the animal. This fits a text that identifies an
   individual and an emblem that does not belong to that individual, such as a sign of office or kind
   of business, better than a personal clan sign. It is a reading, not a proof: the one-horned bull's
   dominance limits the test, and the animal labels are the dataset's own (checked against the corpus
   plate headings for the joinable cases). [`results/picture-test.txt`](results/picture-test.txt)

The same grouping method was first run on Old Tamil, where the answer is known. It recovers letters
that share a consonant strongly (11.8 sd above chance) and letters that share a vowel weakly (2.4 sd).
It works, but only partly.

## Toward the language (steps 1–7)

What can be said about the language behind the signs, short of reading them?

1. **Numbers come before what they count, weakly.** The short-stroke number signs (codes 3–7,
   13–19, 27, 55) end a text in 3.0% of their uses, against 15.9% ± 9.3% for other signs of the same
   frequency (only 1.2% of 500 control sets are as low). A second measure, which signs take several
   different numbers on each side, is even (21 against 21). Numbers before nouns fits Dravidian,
   Indo-Aryan and Munda alike, so this argues only against a Sumerian-type order, where numbers
   follow. The result depends on the reading direction (right to left, taken from the jar sign's
   text-final place). [`results/numerals.txt`](results/numerals.txt)
2. **Ending patterns do not separate the candidate families.** Inside words, Vedic Sanskrit (written
   syllables), Old Tamil (aksharas) and Santali (a Munda language, from the Santali Wikipedia) all make
   the last unit the most predictable (0.68–0.76 of their own unit entropy) and none makes the
   second-last predictable. In short phrases, the Indus end is more fixed than any of them (0.68
   against 0.78–0.88) and its start less (1.02 against 0.81–0.89): a formula with a fixed close.
   [`results/endings.md`](results/endings.md)
3. **The outside record of the language is two names.** Sumerian texts describe Meluhha (the usual
   identification of the Indus region) only in Sumerian words: "black land", highland *mes* timber,
   carnelian, francolins, a bird called *ha-ia₃*, gold, tin-bronze, boats. A seal names "a translator
   of the Meluhhan language". The two personal names Nanaza and Samar are, by the specialists' own
   account (read here only secondhand), the only possible words of the language. Two names cannot
   choose a family. [`results/meluhha-evidence.md`](results/meluhha-evidence.md)

4. **Numbers are used two ways: counting, and fixed numbered names.** Taking the signs that follow a
   number far more often than chance (order shuffled inside each text, 500 times), one group takes
   many different values, as counted things would: 390 (a forked branch) after 3 to 8, z +9.7; 220
   after 3 to 9; 405 and 407 (branches with twigs) after 3 to 8; 900 (an arc) after 3 to 5; 156,
   mostly on tablets. Another group always takes the same value, like a fixed name: 585 follows 7 in
   15 of its 25 uses, 575 always follows 7, 423 always follows 3. The jar sign is preceded by a number
   less often than chance. Most of these pairs are on seals rather than tablets, which fits counts and
   numbered names inside identifiers better than bookkeeping. Shapes are described here, not read.
   [`results/number-anchor.md`](results/number-anchor.md), [`results/number-anchor-signs.png`](results/number-anchor-signs.png)

5. **A slot before the closing jar holds one unit, sometimes a numbered name.** Only three fixed
   number compounds exist: 7 + 585 (15 uses), 7 + 575 (12) and 3 + 423 (5); the 7 appears both as
   seven strokes in a row and as 4 + 3 in two rows. In about half their uses exactly one sign follows
   them, and the sign after them is the jar 72% of the time. Counted pairs (a number + 390, 220 and so
   on) behave differently: they end the text themselves in 62% of uses and are followed by the jar only
   15% of the time. Where 7 + 585 stands in the frame "33 _ jar", single signs (923, 760, 176, 904)
   also stand. This suggests a frame of the form [...] [one unit] [jar], where the unit is a single
   sign or a numbered name acting as one word, with counting in a different kind of text. The numbers
   are small (32 uses; each frame seen 2 to 5 times) and the reading direction is inferred, so this is
   a pattern, not a proven grammar. [`results/numbered-names.txt`](results/numbered-names.txt)
6. **The slot before the jar is an open class with a bound core.** 35% of distinct texts end with the
   jar. The unit before it is filled 665 times by 161 different units, half of them seen there only
   once, as a slot for names or identifiers would be. A core of 36 signs stands there far more often
   than chance: sign 760 in 61 of its 77 uses (z +29.8), and 752, 772 and 773 almost always; several of
   the strongest are U-shaped, vessel-like signs. In texts that do not end with the jar, these signs end
   the text less often than other signs (17% against 27%), so they need the jar after them, like a stem
   with its fixed ending. The counted signs 390 and 405 are the exception: in jar-less texts they end
   the text 62% and 79% of the time. Two endings, then: an open-class unit plus the jar, or a number
   plus a counted sign without it. The jar behaves as a closing element bound to what precedes it,
   which fits a case ending or title marker, and equally a closing formula in a code.
   [`results/prejar-slot.md`](results/prejar-slot.md), [`results/prejar-slot-signs.png`](results/prejar-slot-signs.png)

7. **Indus-script seals made abroad follow different rules.** Round "Gulf Type" seals with Indus
   signs were found in Bahrain, Failaka, Mesopotamia and Iran. Their inscriptions are drawn in
   Laursen (2010, Fig. 11); we transcribed all 29 into sign features, right to left, each sign with a
   confidence mark ([`abroad/laursen-fig11-transcription.csv`](abroad/laursen-fig11-transcription.csv)).
   Three are left out: one is in Linear Elamite, one carries no text, one is pictorial. Against this
   repository's dataset:

   | | inscriptions | open with the "twins" sign | end with a jar-like sign |
   |---|---|---|---|
   | home texts (this dataset) | 1,902 | 0.4% | 35% |
   | Gulf Type seals found abroad | 21 | 24% (p ≈ 5 × 10⁻⁹) | 14% (p = 0.035) |
   | Gulf Type seals found in the Indus Valley | 5 | 0 | 0 |

   The "twins" sign (two human figures side by side) opening these inscriptions was first noted by
   Parpola (1994) and set out by Laursen (2010), who calls it "the only rule-like regularity so far
   attested in this 'western written language'" and concludes that the language of these seals was,
   "with only a few exceptions ... of non-Harappan origin". Our transcription confirms the opening and
   adds that these texts seldom close with the jar, the sign that ends a third of home texts: a change
   in how the text is framed, not only in the names it carries. Whether that means another language,
   names from another tradition, or a later way of writing (most Gulf Type seals date from about 2050 BC
   on) is not decided by this. The transcription is one reader's reading of drawings, and the
   jar-like count includes doubtful U shapes, so the shortfall is if anything understated.
   [`results/laursen-abroad.txt`](results/laursen-abroad.txt)

Taken together: order and position statistics can rule some kinds of language out, but they cannot
choose between Dravidian, Indo-Aryan and Munda, which look alike on every measure tried. Choosing
needs evidence about sounds, which the record does not yet hold.

## Relation to prior work

Most of the structural findings above re-derive results that were already published or found in
parallel, and should be read as independent replications rather than discoveries:

| here | prior or parallel work |
|---|---|
| findings 1–4 (structure, signs keeping places, the jar ending, comparison with languages) | Mahadevan 1977; Rao et al. 2009; Yadav et al. 2010; Koshy 2026 (§8–9, with Linear B, Sumerian and Egyptian, size-matched) |
| finding 5 (look-alike signs behave alike) | Koshy 2026 (§4: a weak but real agreement between shape and behaviour) |
| findings 6, 9 (text independent of the animal) | Koshy 2026 (§4), and Marshall (1931), who already reported the same inscription over different animals |
| finding 9 (seal texts individual) | Kriger & Hunt 2026; Koshy 2026 (95% of Mohenjo-daro seal texts unique) |
| steps 1 and 4 (number signs) | Mahadevan; Kriger & Hunt 2026; Koshy 2026 (§6: short strokes go mainly with "forked stem" signs, our 390/405/407) |
| step 2 (suffixing cannot be told from a phrase-final formula) | Koshy 2026 (§14) reaches the same conclusion |
| steps 5–6 (the slot before the jar) | Koshy 2026 (§5, §8: the pre-final sign and the ending behave as one unit; the slot is open) |
| step 7 (the "twins" opening abroad) | Parpola 1994; Laursen 2010; Koshy 2026 (finding 5) |

What, as far as we could find, is not already in these sources: the pre-registered blind test of
Hindu sacred symbols (finding 7), the shortfall of jar endings on Gulf Type seals measured against home
texts (step 7), the particular fixed number compounds 7 + 585, 7 + 575 and 3 + 423 as fillers of the
slot before the jar (step 5), and the inclusion of a Munda language (Santali) in the endings test
(step 2). The reading direction used throughout (right to left) follows the literature and Mackay's own
statement; none of our statistics can confirm a direction, since they would read the same way reversed.

Koshy, N. S. (2026). *Indus script: machine-readable seal catalogues from Mackay (1938) and Marshall
(1931), with photo-coded text features and a reproducible analysis pipeline.* Zenodo,
[10.5281/zenodo.22852769](https://doi.org/10.5281/zenodo.22852769). Kriger, C. & Hunt (2026),
"Positional constraints, sequence uniqueness, and stroke numerals in Indus seal inscriptions from
Mohenjo-Daro" (as cited by Koshy; not read here).

## Limits

- **Direction.** The sign order is taken as stored. That the stored start is the reading end (the
  script is mostly read right to left) is an inference from the jar sign's known text-final place,
  not a field in the data.
- **Sanskrit.** The syllable splitter attaches final consonants to the last syllable, which scatters
  Sanskrit's case endings. The Sanskrit grammar-shape row is not a fair test until it splits by
  written akshara.
- **Genre.** The language samples are verse and prose cut to the Indus lengths, not seal-like texts
  (names, titles, formulae). A genre-matched comparison, for example Mesopotamian seal inscriptions,
  has not been done.
- **Entropy.** Plug-in estimates on about 9,000 tokens are biased low. Only comparisons between
  samples of the same size, and against shuffles of the same text, are meaningful.
- **Corpus choices.** Identical sequences are merged; the line-break marker is removed; 45 rare
  signs have no glyph in the font and show as "?". The sign catalogue (the corpus's own numbering)
  decides what counts as one sign, and other catalogues split and merge signs differently.

## Reproduce

```
./fetch_data.sh   # downloads all inputs from upstream, pinned to commits, sha256-checked
./run.sh          # rebuilds everything in results/
```

Needs Python 3 with `numpy` and `Pillow`. Every script runs offline once the data is fetched.

| script | output |
|---|---|
| `src/structural.py` | `results/structural.txt`: counts, positions, pairs, entropy against shuffles |
| `src/compare.py` | `results/compare.md`: the same-size comparison table |
| `src/grammar_groups.py` | `results/grammar-and-groups.md`: ends test and context groups |
| `src/shape_family.py` | `results/shape-family.txt`: code-distance test |
| `src/motif.py` | `results/motif.txt`: text against the carved animal |
| `src/numerals.py`, `src/numeral_position.py` | `results/numerals.txt`: number signs and word order |
| `src/step2_endings.py` | `results/endings.md`: ending patterns against Sanskrit, Tamil, Santali |
| `src/number_anchor.py` | `results/number-anchor.md`, `results/number-anchor-signs.png`: signs that follow numbers |
| `src/numbered_names.py` | `results/numbered-names.txt`: fixed number compounds and the slot before the jar |
| `src/laursen_abroad.py` | `results/laursen-abroad.txt`: Gulf Type seal inscriptions (Laursen 2010) against home texts |
| `src/prejar_slot.py` | `results/prejar-slot.md`, `results/prejar-slot-signs.png`: every filler of the slot before the jar |
| `src/picture_test.py` | `results/picture-test.txt`: repeated texts, text slots and object types against the carved animal |
| (by hand) | `results/seal-coding-202.csv`: picture coding of 202 seals; `results/meluhha-evidence.md`: sources on Meluhha, quote or null |
| `src/render.py` | `results/*.png`: sign sheets |
| `blind/symbols.py`, `blind/match.py` | `blind/drawings.png`, `blind/result.txt`, `blind/matches.png`: the blind symbols test |

## Data and credit

No data is redistributed here; `fetch_data.sh` downloads each file from its source.

| input | source | licence |
|---|---|---|
| Indus sign sequences and sign font | [yajnadevam/indus-website](https://github.com/yajnadevam/indus-website) @ `2434249` | GPL-3.0 |
| Rig Veda lines (IAST) | [Equationist/indusscript-decipherment-stats](https://github.com/Equationist/indusscript-decipherment-stats) @ `90c70d8` | Unlicense |
| Tirukkural (original lines only) | [tk120404/thirukkural](https://github.com/tk120404/thirukkural) @ `cf3ff6c` | Apache-2.0 |
| Chess openings | [lichess-org/chess-openings](https://github.com/lichess-org/chess-openings) @ `a6189a3` | CC0-1.0 |
| *Pride and Prejudice* | [Project Gutenberg #1342](https://www.gutenberg.org/ebooks/1342) | public domain (US) |
| Santali Wikipedia, dump of 2026-10-01 | [dumps.wikimedia.org/satwiki](https://dumps.wikimedia.org/satwiki/) | CC BY-SA 4.0 |

Seal pictures were read from the plates of *Corpus of Indus Seals and Inscriptions*, vol. 1 (Joshi &
Parpola 1987, Memoirs of the Archaeological Survey of India 86), as hosted by the Indira Gandhi
National Centre for the Arts. No image or text of that volume is reproduced here, only our coding.
Sumerian passages are quoted from the Electronic Text Corpus of Sumerian Literature (Oxford).

The Indus sequences follow the Interactive Corpus of Indus Texts (ICIT) of Bryan K. Wells and Andreas
Fuls, which rests on the corpora of Iravatham Mahadevan (1977) and Asko Parpola and colleagues (CISI).
This study uses only the sign sequences, sites and object types. The dataset's maintainer has proposed
a reading of the script; this study neither uses nor evaluates it.

Related work: Rao et al., *Science* 324 (2009); Farmer, Sproat and Witzel (2004); Parpola, in *Qala'at al-Bahrain* vol. 1 (1994), pp. 304–315; Laursen, *Arabian Archaeology and Epigraphy* 21 (2010): 96–134;
Nair, arXiv:2604.17828 (2026); Tiwari, NLP4DH 2026.

## Licence

Code: GNU Affero General Public License v3.0 (`LICENSE`). Copyright © 2026 Capt. Anil Sharma.
Rendered sign sheets in `results/` are drawn with the GPL-3.0 font above.
