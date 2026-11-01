# Derivation of "the bar" (GROWTH_PER_DAY = 0.0903 /day) from published data

Success criterion (CLAUDE.md, quoted): the bar is "real data **or** a rigorous model", with a
cross-species / disease / class transfer acceptable "if the transfer is justified in writing"; graded
MEASURED / TRANSFERRED / DERIVED / ASSUMED. Not "demonstrated in dogs".

Source of the number in the repo: `core/lymphoma_catalogue.py:33` (= the P-gp efflux clone under full CHOP;
`lymphoma_scenarios._SHARED_GROWTH = [.100,.092,.090,.088]`, labelled "illustrative, not fitted").
So the bar is the **intrinsic net per-day growth of a drug-insensitive (resistant) clone** (births minus
spontaneous death, in vivo), moved ~2% by residual drug effect. Doubling 7.68 d.
It is therefore an in-vivo NET rate. Gross rates (cell cycle, Tpot, culture) are ceilings on it;
observed net regrowth while still partly drug-suppressed is a floor on it.

## Table: estimate -> implied per-day rate  (r = ln2 / doubling time, or ln(B2/B1)/T)

| # | Estimate | Source (PMID) | Status | Implied /day | Role |
|---|---|---|---|---|---|
| A1 | Tpot median 3.4 d (Ts 7.23 h, LI 12.49%), 42 dogs, untreated lymphoma, flow BrdU. (Ts/LI = 2.41 d, lambda ~1.41, consistent) | Larue 1999, Int J Hyperthermia, PMID 10598945 | MEASURED, dog | 0.204 | CEILING (gross, zero cell loss) |
| A2 | Tpot by BrdU delayed biopsy, 55 dogs NHL; Tpot predicts first remission (p=0.017). Abstract gives no median | Vail 1996, Exp Hematol, PMID 8647231 | MEASURED, dog (value not retrieved) | n/a | corroborates A1 |
| A3 | Ki-67+ 30.2 +/- 10.8% (lymphoma, n=19) vs 2.7% normal | Bauer 2007, PMID 17939545 | MEASURED, dog | growth fraction ~0.3-0.7 | supports A1 |
| A4 | Ki-67 50-70% in 27/45, >70% in 12/45 | Sokolowska 2012, PMID 23390763 | MEASURED, dog | growth fraction ~0.5-0.7 | supports A1 |
| B1 | Untreated, AgNOR>5.5 (high-grade) median survival 38.5 d; AgNOR<4 median 154 d | Kiupel 1998, J Comp Pathol, PMID 9839202 | MEASURED, dog | with B_lethal 1e12: B_dx 1e10 -> 0.120; 3e10 -> 0.091; 1e11 -> 0.060 (T=38.5 d). Low-AgNOR (154 d): 0.015-0.030 | NATURAL-HISTORY consistency check (B_dx ASSUMED, not measured) |
| B2 | Prednisone alone, previously untreated nodal intermediate/large-cell, n=109: median OS 50 d (41-59) | Rassnick 2021 CLASS trial, JAVMA, PMID 34125606 | MEASURED, dog (steroid is active, so not purely untreated) | T=50 d: B_dx 1e10 -> 0.092; 3e10 -> 0.070; 1e11 -> 0.046 | as B1 |
| C1 | 2nd remission on CHOP retreatment, median 159 d (98 d if first remission <289 d), n=95 | Flory 2011 JAVMA, PMID 21320021 | MEASURED, dog | ln-range 2.3/4.6/6.9 over 98 d -> 0.024/0.047/0.071; over 159 d -> 0.015/0.029/0.043 | FLOOR on g (net, still drug-suppressed) |
| C2 | Rescue L-asparaginase+lomustine+prednisone in relapsed/refractory: median TTP 63 d (111 d if CR, 42 d if PR) | Saba 2007 JVIM, PMID 17338160 | MEASURED, dog | 63 d: 0.037/0.073/0.110; 111 d (CR dogs): 0.021/0.042/0.062 | FLOOR on g; upper cell (0.110) is an over-estimate (assumes 1e9 start and 1e12 endpoint for PR dogs too) |
| C3 | First CR duration: COAP 94 d vs UW-19 CHOP 174 d | Hosoya 2007 JVIM, PMID 18196747 | MEASURED, dog | 94 d: 0.025/0.049/0.073 | FLOOR on g |
| C4 | First CR duration CHOP-based 298-307 d; UW-25 high-dose, no maintenance: OS 270 d | Rassnick 2010 PMID 21062406; Rassnick 2007 PMID 18196748; Chun 2000 PMID 10772481 | MEASURED, dog | 300 d: 0.008/0.016/0.023 | FLOOR; mixes treated/untreated time, weak |
| D1 | In vitro doubling: 17-71 24 h; OSW 16 h; CLBL-1 19 h; CLL1390 37 h (range for all 27 canine lines 15-40 h) | Maeda 2016 PLoS One, PMID 27257868 | MEASURED, dog (in vitro) | 24 h 0.69; 16 h 1.04; 19 h 0.88; 37 h 0.45 | CEILING (all cells cycling, no loss, no hypoxia/immune) |
| D2 | CLBL-1 31 h (original), GL-1 27.3 h, Ema 26.6 h (via Cellosaurus / web search, underlying paper not opened) | Rutgen 2010 Leuk Res PMID 20153049; Cellosaurus CVCL_L322, L352 | MEASURED in vitro, secondhand | 0.54-0.61 | CEILING |
| E1 | Human tumour DT: <1 week to >1 yr, median ~2 months; cycle ~2 d; cell-loss factor "greatest when proliferation is most intensive" | Tubiana 1989 Acta Oncol, PMID 2650719 | TRANSFERRED (human, pan-tumour) | <7 d -> >=0.099; 60 d -> 0.012 | the bar (7.7 d) is at the fast edge of the human range |
| E2 | Burkitt lymphoma kinetic DT ~24 h | Iversen 1972 Eur J Cancer PMID 4677829 (primary, abstract unavailable); quoted in PMID 22027227, 3818193 | TRANSFERRED (human, most extreme lymphoma) | 0.69 | ABSOLUTE CEILING; not representative of canine multicentric B-cell/DLBCL-like |
| E3 | Human "malignant lymphoma" tumour DT ~29 d | search-engine snippet only, primary not opened | UNVERIFIED, do not rely | 0.024 | (not used) |

Not found / not used: a measured serial caliper/ultrasound volume-doubling time of untreated canine lymphoma
(PubMed searches returned nothing). A "clinical 66 h vs Tpot 25.6 h" Burkitt figure surfaced in a search snippet
and could not be traced to a source; it is NOT used.

## Arithmetic notes
- ln2/3.4 d = 0.2039 /day. The bar equals 0.0903/0.2039 = 44% of the gross potential rate, i.e. it
  corresponds to a cell-loss factor phi = 1 - 0.0903/0.2039 = 0.56.
- In vivo B_dx implied by the bar from natural history: ln(1e12/B)=0.0903*38.5=3.48 -> B = 3.1e10 cells
  (~31 g); from 50 d -> 1.1e10 (~11 g). Plausible for stage III-V dogs, but B_dx is assumed, so B1/B2
  are consistency checks only.
- Relapse arithmetic = ln(B_det/B_CR)/T with B_CR 1e9-1e10 (user's residual range), B_det 1e11-1e12.
  Because the resistant clone is still being partly suppressed (or off-drug with a sensitive subpopulation
  contributing) these are NET observed regrowth rates <= intrinsic g. They are floors.

## Conclusion

Bracket on the intrinsic net in-vivo growth rate g of a resistant canine lymphoma clone:
- FLOOR (observed net regrowth, dog, MEASURED): ~0.015-0.07 /day (central 0.03-0.05), max 0.11 only under
  the most aggressive reading (C2, 1e9 -> 1e12 over 63 d).
- Natural-history check (dog, MEASURED survival, ASSUMED B_dx): 0.046-0.12 for high-grade disease (38-50 d),
  0.015-0.03 for low-AgNOR disease.
- CEILING (gross, zero cell loss): Tpot 0.204 /day (dog, MEASURED, 10598945); in vitro 0.45-1.04; Burkitt 0.69.

So **0.0903/day sits at the upper end of every NET estimate** (1.3-6x above the relapse-regrowth floors; at
the edge of the human <1-week tumour range; inside the 0.092-0.120 natural-history result for the most
aggressive dogs) **but 2.3x BELOW the gross Tpot ceiling and 5-12x below culture.** It is conservative with
respect to what has been observed as net regrowth; it is not an upper bound on what the biology could do if
spontaneous cell loss were small. Its implied phi (0.56) is plausible but is not itself measured in dogs; the
only support is Tubiana's statement that phi is large in fast-proliferating tumours.

Grade: the bar moves from ASSUMED/illustrative to **DERIVED (bracketed) / TRANSFERRED** - a justified
central band, not a point estimate. It should no longer be listed as a bare literal. Honest wording:
"0.0903 /day is the upper end of the net in-vivo band (0.015-0.12) implied by dog relapse and natural-history
data, and 44% of the dog-measured gross potential rate (Tpot 3.4 d)".

What the bar represents and whether intrinsic growth is conservative: the bar is the untreated net growth of
the drug-insensitive clone, applied unchanged while the regimen runs (drug moves it ~2%). That is
conservative for a resistant clone in two respects: (1) it ignores any residual suppression (steroid,
partial cross-activity) that makes observed regrowth slower; (2) it ignores immune/host control.
It is NOT conservative if the resistant clone is faster than the bulk (resistance clones in the model are
set at or below the sensitive 0.100) or if cell loss is small, then g -> 0.20. Recommended, for robustness
and to avoid over-claiming closure: re-run `conjunction()` at g = 0.20 (Tpot ceiling) as a sensitivity row
and report which closures survive; do not re-tune the bar to force a closure.

Residual caveats: B_dx and B_CR are assumed (no canine burden measurement found); Vail 1996 median Tpot not
retrieved; Iversen 1972 and GL-1/Ema in vitro values are secondhand; no direct canine volume-doubling study found.
