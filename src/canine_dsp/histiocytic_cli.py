"""Demo/report functions for the Corgi HS driver-hypothesis analysis in `histiocytic_origin`."""

import json
import time
from pathlib import Path
from urllib.error import URLError

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .alphafold import align_residue_numbers, download_structure, read_plddt_track
from .histiocytic_origin import (
    CANDIDATE_DRIVERS,
    CORGI_CLINICAL_FEATURES,
    HUMAN_HISTIOCYTOSIS_DRIVERS,
    MTAP_CDKN2A_LOCUS,
    TISSUE_RESIDENT_MACROPHAGE_ONTOGENY,
    VERIFIED_HOTSPOT_CONTROLS,
    hotspot_salience,
    permutation_pvalue,
)
from .spectral import bicoherence, coherence, spectral_entropy
from .uniprot import DOG_TAXID, HUMAN_TAXID, resolve_uniprot_accession


def _hotspot_conservation(human_seq: str, dog_seq: str, hotspots: dict[int, str]) -> list[dict]:
    """For each human hotspot: verify the expected wild-type residue is really there, then report
    the aligned dog position and whether dog carries the same residue.

    Verifying the human residue first is the check that catches a mis-transcribed or stale
    literature position outright, instead of silently comparing the wrong column.
    """
    if not hotspots:
        return []
    mapping = align_residue_numbers(human_seq, dog_seq)
    rows = []
    for position, expected in sorted(hotspots.items()):
        observed_human = human_seq[position - 1] if 0 < position <= len(human_seq) else None
        row = {"human_position": position, "expected_human_residue": expected,
               "observed_human_residue": observed_human,
               "human_residue_matches_literature": observed_human == expected}
        if position in mapping:
            dog_position, identical = mapping[position]
            row.update(dog_position=dog_position,
                       dog_residue=dog_seq[dog_position - 1],
                       hotspot_conserved_in_dog=bool(identical),
                       # The practically load-bearing number: a lab sequencing this gene in a dog
                       # and looking at the human coordinate would read the wrong residue whenever
                       # this is nonzero.
                       numbering_offset_human_minus_dog=position - dog_position)
        else:
            row.update(dog_position=None, dog_residue=None, hotspot_conserved_in_dog=False,
                       note="human position falls in an alignment gap -- no dog counterpart")
        rows.append(row)
    return rows


def _retrying(call, attempts: int = 3, delay: float = 2.0):
    """Retry a network call on transient transport errors only. Needed to keep a real finding
    distinguishable from a flaky connection: this analysis reports "no dog entry exists" as a
    substantive result (that is how PLAUR's absence was established for the HSA module), and a
    bare `Connection reset by peer` produced an identical-looking row on the first run of this
    demo.
    """
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            return call()
        except (URLError, OSError) as error:
            last = error
            if attempt < attempts - 1:
                time.sleep(delay * (attempt + 1))
    raise last  # type: ignore[misc]


def corgi_driver_hypothesis_demo(out: Path, genes: list[str] | None = None,
                                 bicoherence_nperseg: int = 64, permutations: int = 10_000,
                                 seed: int = 7) -> None:
    """Structural/DSP triage of the candidate driver panel for Corgi primary CNS / pulmonary HS. Per
    candidate gene: resolve human and dog UniProt accessions, pull both AlphaFold models, measure
    whole-protein ortholog conservation, check whether each established human hotspot residue is
    actually conserved at the aligned dog position, and run three signal analyses on the
    structural-confidence (pLDDT) tracks -- * human-vs-dog magnitude-squared coherence: is the
    *domain architecture* conserved, not just the residue identities?
    """
    out.mkdir(parents=True, exist_ok=True)
    candidates = {candidate.gene: candidate for candidate in CANDIDATE_DRIVERS}
    selected = list(candidates) if genes is None else genes

    rows, hotspot_rows, salience_reports, tracks = [], [], [], {}
    for gene in selected:
        candidate = candidates.get(gene)
        row = {"gene": gene,
               "tier": candidate.tier if candidate else "(not in the candidate panel)",
               "found": False}
        try:
            human_accession = _retrying(lambda: resolve_uniprot_accession(gene, HUMAN_TAXID))
            dog_accession = _retrying(lambda: resolve_uniprot_accession(gene, DOG_TAXID))
            human_track = read_plddt_track(_retrying(
                lambda: download_structure(human_accession, out / "structures" / f"{gene}_human")))
            dog_track = read_plddt_track(_retrying(
                lambda: download_structure(dog_accession, out / "structures" / f"{gene}_dog")))
            human_seq = "".join(human_track["residue_type"])
            dog_seq = "".join(dog_track["residue_type"])
            tracks[gene] = (human_track, dog_track)

            mapping = align_residue_numbers(human_seq, dog_seq)
            identical = sum(1 for _, same in mapping.values() if same)
            freq, coh = coherence(human_track["plddt"].to_numpy(), dog_track["plddt"].to_numpy())
            dog_plddt = dog_track["plddt"].to_numpy()
            nperseg = min(bicoherence_nperseg, len(dog_plddt) // 3)
            mean_bicoherence = None
            if nperseg >= 8:
                _, b2 = bicoherence(dog_plddt, nperseg=nperseg)
                mean_bicoherence = float(np.nanmean(b2))

            row.update(
                found=True, human_uniprot=human_accession, dog_uniprot=dog_accession,
                human_length=len(human_seq), dog_length=len(dog_seq),
                identity_fraction_of_aligned=identical / len(mapping) if mapping else 0.0,
                mean_human_dog_plddt_coherence=float(np.mean(coh[1:])) if len(coh) > 1 else None,
                dog_plddt_spectral_entropy=spectral_entropy(np.abs(np.fft.rfft(dog_plddt)) ** 2),
                mean_dog_plddt_bicoherence=mean_bicoherence,
            )

            if candidate and candidate.hotspots:
                for hotspot in _hotspot_conservation(human_seq, dog_seq, candidate.hotspots):
                    hotspot_rows.append({"gene": gene, **hotspot})

            if gene in VERIFIED_HOTSPOT_CONTROLS:
                salience = hotspot_salience(dog_plddt, dog_seq)
                dog_positions = []
                for human_position in VERIFIED_HOTSPOT_CONTROLS[gene]:
                    if human_position in mapping:
                        dog_positions.append(mapping[human_position][0])
                report = permutation_pvalue(salience, dog_positions, permutations, seed)
                salience_reports.append({"gene": gene, "dog_positions_tested": dog_positions,
                                        **report})
        except ValueError as error:
            # The resolver raises ValueError when a query genuinely returns no entry -- a real
            # annotation gap, and a substantive finding rather than a failure to be retried.
            row.update(error=f"{type(error).__name__}: {error}", error_kind="no_entry_found")
        except (URLError, OSError, KeyError) as error:
            row.update(error=f"{type(error).__name__}: {error}", error_kind="transient_or_transport")
        rows.append(row)

    table = pd.DataFrame(rows)
    table.to_csv(out / "candidate_driver_triage.csv", index=False)
    if hotspot_rows:
        pd.DataFrame(hotspot_rows).to_csv(out / "hotspot_conservation.csv", index=False)
    if salience_reports:
        pd.DataFrame(salience_reports).to_csv(out / "hotspot_salience_validation.csv", index=False)

    if tracks:
        n = len(tracks)
        fig, axes = plt.subplots(n, 1, figsize=(10, 2.4 * n), squeeze=False)
        for ax, (gene, (human_track, dog_track)) in zip(axes[:, 0], tracks.items()):
            ax.plot(human_track["residue_number"], human_track["plddt"], label="human",
                   color="tab:blue", linewidth=.9)
            ax.plot(dog_track["residue_number"], dog_track["plddt"], label="dog",
                   color="tab:orange", linewidth=.9, alpha=.8)
            candidate = candidates.get(gene)
            if candidate:
                for position in candidate.hotspots:
                    ax.axvline(position, color="tab:red", linestyle="--", linewidth=.8)
            ax.set(ylabel="pLDDT", title=f"{gene} (dashed red = human hotspot positions)")
            ax.legend(fontsize=7)
        axes[-1, 0].set(xlabel="residue number")
        fig.tight_layout(); fig.savefig(out / "candidate_plddt_tracks.png", dpi=160); plt.close(fig)

    checkable = [r for r in rows if r.get("found")]
    unconserved = [h for h in hotspot_rows if not h.get("hotspot_conserved_in_dog")]
    mismatched_literature = [h for h in hotspot_rows
                            if not h.get("human_residue_matches_literature")]
    shifted = [h for h in hotspot_rows if h.get("numbering_offset_human_minus_dog")]

    # Whether the nonlinear salience method may be used downstream at all. It is applied to the
    # verified control hotspots FIRST, and only earns the right to nominate residues in candidates
    # that have no established hotspot (CSF1R, CSF1) if it beats chance on those controls. If it
    # does not, that is a negative result to report, not a step to skip past.
    significant = [r for r in salience_reports if (r.get("p_value") or 1.0) < 0.05]
    salience_verdict = {
        "controls_tested": [r["gene"] for r in salience_reports],
        "controls_significant": [r["gene"] for r in significant],
        "passed_positive_control": bool(significant),
        "cleared_for_downstream_use": bool(significant),
        "conclusion": (
            "The second-order Volterra salience model did NOT beat a permutation null at any "
            "verified control hotspot, so it is reported as a failed method and is deliberately "
            "NOT used to nominate candidate residues in CSF1R/CSF1 or anywhere else. Note the "
            "low power (1-2 positions per protein) cuts both ways: this is a failed validation, "
            "not a demonstration that no such signal exists."
            if not significant else
            "The salience model beat its permutation null on at least one verified control "
            "hotspot."),
    }
    summary = {
        "question": "Which driver genes should be sequenced first in Pembroke Welsh Corgi primary "
                   "CNS or primary pulmonary histiocytic sarcoma, given that no Corgi-specific and "
                   "no anatomic-site-stratified canine HS mutation data exists?",
        "clinical_features_reasoned_from": CORGI_CLINICAL_FEATURES,
        "ontogeny_argument": TISSUE_RESIDENT_MACROPHAGE_ONTOGENY,
        "cross_species_landscape": HUMAN_HISTIOCYTOSIS_DRIVERS,
        "germline_susceptibility_locus": MTAP_CDKN2A_LOCUS,
        "candidate_panel": [
            {"gene": c.gene, "tier": c.tier, "rationale": c.rationale,
             "hotspots": c.hotspots, "lineage_link": c.lineage_link,
             "druggable_by": c.druggable_by}
            for c in CANDIDATE_DRIVERS if c.gene in selected],
        "triage": rows,
        "hotspot_conservation": hotspot_rows,
        "hotspot_salience_validation": salience_reports,
        "nonlinear_salience_verdict": salience_verdict,
        "counts": {
            "genes_requested": len(selected),
            "structurally_checkable": len(checkable),
            "hotspots_checked": len(hotspot_rows),
            "hotspots_not_conserved_in_dog": len(unconserved),
            "literature_positions_that_did_not_match_the_human_structure": len(mismatched_literature),
            "hotspots_whose_dog_residue_number_differs_from_human": len(shifted),
        },
        "actionable_sequencing_note": (
            "Human and dog residue numbering do not agree for every candidate: see "
            "`numbering_offset_human_minus_dog` in hotspot_conservation."),
        "unverified_extrapolations": [
            "the tissue-resident-macrophage cell-of-origin argument is an inference from Iba-1 "
            "positivity plus anatomic site, not a lineage-tracing result in any dog -- no study "
            "has established the cell of origin of canine HS at any site",
            "human LCH/Erdheim-Chester genetics are used as the cross-species prior; canine HS "
            "already demonstrably differs at one node (PTPN11/KRAS reported instead of BRAF), so "
            "the human landscape constrains the search rather than predicting the answer",
            "sequence identity and hotspot-residue conservation establish chemical plausibility "
            "only; a perfectly conserved residue says nothing about whether it is ever actually "
            "mutated in this breed and disease",
            "the Volterra salience analysis is exploratory, fit per-protein with no held-out data, "
            "and validated only against a handful of known hotspots -- see its permutation p-value "
            "and power caveat rather than treating a rank as evidence",
            "CSF1R and CSF1 carry no established activating hotspot to check, so for them the "
            "structural work can only confirm the ortholog exists and is conserved -- it cannot "
            "nominate a residue, and a structural rearrangement (the mechanism in tenosynovial "
            "giant cell tumour) would be invisible to hotspot sequencing entirely",
        ],
        "warning": "A prioritized sequencing hypothesis, not a molecular diagnosis.",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")
