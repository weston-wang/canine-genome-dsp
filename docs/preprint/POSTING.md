# Deposit & posting kit — MTAP/PRMT5 canine HS hypothesis note

Goal: maximum reach, minimal interfacing. You upload once and you are done; nothing
obliges you to respond to anyone. The uploadable file is **`hypothesis_note.pdf`**.

**Recommended plan (updated Aug 2025):**
- **~~OSF Preprints~~ — no longer usable.** OSF **suspended its generalist preprint server
  on 8/25/2025**; only discipline-specific community servers (psychology/social science/
  education) remain, none fitting canine oncology. Skip OSF.
- **Primary — Research Square** (Route A): multidisciplinary, free, permanent DOI,
  Scholar-indexed, no "must-contain-data" rule → accepts the honest note as-is. Legitimate
  (powers Springer Nature's "In Review"); commercial but not controversial. Confirmed open.
  Tip: upload a **.docx** if you have one — Research Square renders Word files as full-text
  HTML, which is more discoverable than a PDF-only record.
- **Permanence anchor — Zenodo** (Route B): guaranteed, permanent, zero screening. Do this
  too, or instead, if you just want the record to exist forever. (Search-only reach.)
- **Also fine — Preprints.org** (MDPI): works and is biomedical-appropriate, but expect
  heavy journal-solicitation email and a mixed publisher reputation. Use only if you prefer
  it to Research Square.
- **Skip bioRxiv** (Route C): its policy requires data and excludes commentary/hypothesis
  pieces, so it would very likely reject this note as written.

Post to **one** preprint server (duplicate preprints are discouraged). Research Square for
reach, plus Zenodo if you want a second permanent copy, is the sweet spot.

---

## Author

Byline is set to **Wes Wang — PhD, digital signal processing** (noted as outside your field of training; the DSP background supports the quantitative modeling). No affiliation label — the name and the PhD line stand on their own. If a form *requires* an affiliation field, put **Unaffiliated**.

Optional, both free and one-time:
- A **dedicated email** (a fresh Gmail/Proton) as the contact, so notifications land
  somewhere you can ignore and no personal inbox is touched.
- An **ORCID iD** (orcid.org, 2-minute signup) — not required, but it makes the deposit
  look established and lets any future record attach to the same identity.

---

## Copy-paste metadata (use for Zenodo and any preprint server)

**Title**
> MTAP loss as an untested, genotype-anchored maintenance target in canine histiocytic sarcoma: PRMT5 and MAT2A synthetic lethality

**Authors**
> Wes Wang   (affiliation: leave blank, or "Unaffiliated" if required)

**Resource type**: Preprint  ·  **License**: Creative Commons Attribution 4.0 (CC-BY-4.0)

**Keywords** (these drive discovery — keep them)
> canine histiocytic sarcoma; MTAP; PRMT5; MAT2A; synthetic lethality; CDKN2A; PTPN11; Bernese Mountain Dog; MEK inhibitor; maintenance therapy; comparative oncology; ctDNA; precision oncology

**Abstract** (paste verbatim)
> Canine histiocytic sarcoma (HS) is an aggressive malignancy with a strong breed predisposition (notably the Bernese Mountain Dog) mapping to the CDKN2A/MTAP germline locus, and with somatic MAPK-pathway drivers — chiefly PTPN11/SHP2 — in roughly 60% of tumours. Current translational effort centres on MEK inhibition, now in a canine Phase I, and on ctDNA monitoring of the PTPN11 driver. These pathway targets are reroutable, so durable control depends on surveillance and drug-switching. I note a specific, testable gap: despite MTAP being co-located with the CDKN2A predisposition locus and homozygous MTAP deletion conferring PRMT5 synthetic-lethal dependency in ~10–15% of human cancers, I found no published evaluation of MTAP status or PRMT5-inhibitor sensitivity in canine HS. If an MTAP-null subset exists, two clinical-stage drug classes exploit that deletion — MTA-cooperative PRMT5 inhibitors (including brain-penetrant congeners) and MAT2A inhibitors — offering the most genotype-anchored maintenance option in this disease, complementing the reroutable MEK majority. This anchor is not absolute: acquired PRMT5-inhibitor resistance is documented without MTAP restoration, via MAPK reprogramming, and confers collateral MEK sensitivity — a defined second line rather than an open exit. I outline the hypothesis, a genotype-tiered maintenance-at-emergence (prevention) framing, and a small set of cheap, decisive experiments led by MTAP immunostaining of archived tissue. This is a computational, model-assisted synthesis intended to orient research; it contains no new experimental data.

---

## Route A — Research Square (recommended primary)

Multidisciplinary, free, permanent DOI, Google Scholar-indexed, no "must-contain-data" rule.
Screening is light (complete author info, declaration statements, health-risk check).

1. Go to **researchsquare.com/submit** → create an account (or log in). Confirm email.
2. **Upload** the manuscript. **Prefer a `.docx`** if available — Research Square renders
   Word files as **full-text HTML** (more discoverable); `hypothesis_note.pdf` also works.
3. Fields to enter:
   - **Title / Abstract / Keywords** — from the metadata block above.
   - **Article type**: pick the closest available to a hypothesis/perspective. If there is no
     "Hypothesis" option, choose **Research Article** (their screen is about completeness and
     health-risk, not requiring data).
   - **Area of study / subject**: **Oncology** (and/or Biology / Veterinary Medicine).
   - **Authors**: Wes Wang. Affiliation: **Unaffiliated** if required; dedicated email.
   - **Declarations**: **Competing interests** = none; **Funding** = none; **Data
     availability** = no new data (optionally link `github.com/weston-wang/canine-genome-dsp`).
     AI assistance is already disclosed in the note's Limitations.
   - **License**: CC BY 4.0 if offered.
4. **Submit.** After the short screen it posts with a DOI (`10.21203/rs...`) and is indexed.

(Alternative: **Preprints.org** — run by MDPI — is biomedical-appropriate and works the same
way, but expect heavy journal-solicitation email and a mixed publisher reputation.)

---

## Route B — Zenodo (permanence anchor; do in addition, or if you skip preprints)

1. Go to **zenodo.org**, sign in (GitHub or ORCID login works).
2. **New upload** → drag in `hypothesis_note.pdf`.
3. Fill the fields from the metadata block above. Resource type = *Preprint*. License = *CC-BY-4.0*.
4. (Optional) Under **Related identifiers**, add the repo URL
   `https://github.com/weston-wang/canine-genome-dsp` as *"is supplemented by"*.
5. **Publish.** Permanent DOI immediately; indexed by Google Scholar within days.

Guaranteed and permanent, but search-only reach — this field does not browse Zenodo.

### Optional: mint a DOI straight from the repo
Zenodo → Account → GitHub → flip the repo **on**, then cut a release; Zenodo auto-creates a
record for the *code*. Use in addition if you want the software itself citable.

---

## Route C — bioRxiv (not recommended for this note)

bioRxiv has the best field reach, **but** its stated policy is that *all article types must
contain data* and that *narrative reviews, commentaries, and opinion/hypothesis pieces are
not acceptable article types* (biorxiv.org/submit-a-manuscript). This note is a hypothesis
piece with no new data, so it would very likely be screened out (~80%). The only way onto
bioRxiv would be to **restructure it as a computational modeling *research article***
(Methods = the model; Results = the durability outputs) — which means presenting the
illustrative probabilities as headline results, the overstatement we deliberately avoided.
Not worth it here. If you ever generate real MTAP-frequency or PRMT5-sensitivity data,
*that* paper belongs on bioRxiv.

---

## Keeping interfacing to zero

- Use the dedicated email; mute the account's notifications.
- Preprint/Zenodo comments are rare and optional — you may answer or ignore, with no
  obligation. Reach here comes from indexing and alerts, not from you engaging.
- You do not need to promote it. The keywords + the alert system do the targeting.

## Honest expectation

This is a message in a bottle with a good address on it. It is permanent, citable, and
lands in the right keyword feeds — but whether one of the ~10 canine-HS groups picks it
up depends on them. The single highest-value thing it asks for is cheap: an MTAP stain
on archived tissue. That is the hook most likely to make someone act.
