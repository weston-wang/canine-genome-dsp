# Deposit & posting kit — MTAP/PRMT5 canine HS hypothesis note

Goal: maximum reach, minimal interfacing. You upload once and you are done; nothing
obliges you to respond to anyone. The uploadable file is **`hypothesis_note.pdf`**.

**Recommended plan:**
- **Primary — OSF Preprints** (Route A): run by the *Center for Open Science* (nonprofit,
  clean reputation, no publisher baggage, minimal email spam). Accepts an honest hypothesis
  note *as-is*, gives a permanent DOI, indexed by Google Scholar → better field reach than
  Zenodo, near-certain acceptance. Best fit for your goals.
- **Fallback — Research Square**: legitimate, established (powers Springer Nature's "In
  Review"), free to post, DOI, Scholar-indexed. Commercial but not controversial. Use if
  OSF stalls.
- **Permanence anchor — Zenodo** (Route B): guaranteed, permanent, zero screening. Do this
  too, or instead, if you just want the record to exist forever. (This field does not browse
  Zenodo, so its reach is search-only.)
- **Skip bioRxiv** (Route C): its policy requires data and excludes commentary/hypothesis
  pieces, so it would very likely reject this note as written. Details in Route C.

Post to **one** preprint server (duplicate preprints are discouraged). OSF Preprints for
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
> MTAP loss and PRMT5 synthetic lethality as an untested, non-reroutable maintenance target in canine histiocytic sarcoma

**Authors**
> Wes Wang   (affiliation: leave blank, or "Unaffiliated" if required)

**Resource type**: Preprint  ·  **License**: Creative Commons Attribution 4.0 (CC-BY-4.0)

**Keywords** (these drive discovery — keep them)
> canine histiocytic sarcoma; MTAP; PRMT5; synthetic lethality; CDKN2A; PTPN11; Bernese Mountain Dog; MEK inhibitor; maintenance therapy; comparative oncology; ctDNA; precision oncology

**Abstract** (paste the abstract from the note verbatim; it is written to match how a
researcher searches — the terms above appear in the first two sentences on purpose)

---

## Route A — OSF Preprints (recommended primary)

Run by the **Center for Open Science** (nonprofit). Free, permanent DOI, indexed by Google
Scholar, accepts hypothesis/theoretical pieces (no "must contain data" rule), light
moderation for scope/appropriateness. Clean reputation, minimal solicitation email.

1. Go to **osf.io** → create a free account (or log in). Confirm your email.
2. Top menu → **Create new** → **Preprint**. Choose the provider **OSF Preprints** (the
   general one), not a branded community.
3. **Upload** `hypothesis_note.pdf` as the preprint file.
4. Fields to paste:
   - **Title / Abstract / Keywords** — from the metadata block above.
   - **Authors**: Wes Wang. (Affiliation optional on OSF — leave blank, or "Unaffiliated".)
     Add your dedicated email as contact.
   - **Subjects** (OSF taxonomy): *Medicine and Health Sciences → Oncology* (and/or
     *Life Sciences*). It concerns veterinary / comparative oncology.
   - **License**: CC BY 4.0.
   - **Conflicts / funding**: none. AI assistance is already disclosed in the note's
     Limitations; no extra field needed.
5. **Submit.** After a brief moderation it posts with a DOI and is picked up by Scholar.

### Fallback if OSF stalls — Research Square
Legitimate and established (it powers Springer Nature's "In Review"); free to post, DOI,
Scholar-indexed; commercial but not controversial. Go to **researchsquare.com** →
**Post a preprint**, upload the same PDF, paste the same metadata.

(Preprints.org — run by the publisher MDPI — is another option but comes with heavy
journal-solicitation email and a mixed publisher reputation; OSF and Research Square are
cleaner, so it's not the recommendation.)

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
