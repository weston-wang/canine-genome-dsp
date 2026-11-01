# Radiation literature sweep (working notes; 2026-10-04)

## Record check (what is ALREADY IN RECORD, where)
- Radiation kill DERIVED by LQ from Maeda 2016 (PMID 27257868): `lymphoma_grounded_inputs.py` RT_SURVIVAL (SF2/SF5: CLBL1 .53/.06, OSW .61/.15, 1771 .75/.27, CLL1390 .85/.36); `docs/universe/SWEEP_stemcell.md` s4.1 (full-text check: plating eff, limiting dilution; SF2 not correlated with S-phase fraction / doubling time across 27 lines -> "cycle independent"), `SWEEP_hct_model.md` s7.2 ("Division gating: no (radiation cycle-independent in 27 canine lines) DERIVED"). All lines are log-phase/cycling; "no canine quiescent-cell assay" (s4.1) is already stated.
- In-vivo dose-modifying factor 1.9 (Malaise 1986, PMID 3009370): SWEEP_stemcell s4.1, SWEEP_hct_model s7.2.
- TBI dose-escalation did NOT cut relapse in dogs (Appelbaum 1985 PMID 3887690: 8.4 vs 13.5 Gy; Deeg 1985 PMID 3901841): SWEEP_stemcell s4.1 "Reality check that the derivation FAILS"; record advises "do not credit TBI above ~10 Gy".
- Uckun 1992 PMID 1429095 (primary T-ALL/NHL SF2 0.36, CD3+ 0.44; relapse after TBI-ASCT 16/19 CD3+): SWEEP_stemcell s4.1. B-ALL CD24- D0 239 cGy PMID 8443393 also there.
- Half-body: PMIDs 19627472, 42525883, 37700548, 40088118 (T-cell PFI 292 d vs B 2127 d), 41183984, 19178684: SWEEP_exists / hct_model / toxicity profiles.
- ALL cranial boost PMID 29191665: SWEEP_persistent_graft.md.
- Dogs survive 700 cGy TBI with care, die >=800 cGy w/o HCT (PMID 19747631): SWEEP_stemcell 4.2.
- FL 2x2 Gy, PMID 20970029; WBRT 24101038 (23.4 Gy), 41420297 (dog 10x4 Gy), PCNSL radioresistance 1572835 / 10563430: in grounded_inputs / SWEEP_cnsregimens.
- UNIVERSE.md s.C line 109: "The model treats radiation as division-gated (conservative)... re-running non-gated changes nothing" (sensitivity only). Catalogue note (core/lymphoma_catalogue.py l.181): craniospinal RT "Still DIVISION-GATED"; potency 'ASSUMED'. SWEEP_hct_model s7.2 says non-gated (derived). => the record is INCONSISTENT: gating default True in catalogue vs. DERIVED non-gated in the HCT sweep. This sweep does not change that, it grades it.

## NEW findings (this sweep)  [verified in PubMed abstract unless marked]
(see sections below, appended incrementally)

### Q1 gating
- 15718417 / 19188704 / 12194750 (Deriano 2005 Blood; Salin 2009; Blaise 2002): B-CLL cells (circulating CLL cells are overwhelmingly G0/G1, non-cycling) undergo radiation-induced apoptosis in ~85% of patients; ~15% of patients' cells are resistant (NHEJ/DNA-PK overactivity; 13q14.3 + another aberration, p53 mutation/17p del). Verified in abstracts ("approximately 15% ... resistant ... contrary to approximately 85% of patients and normal human lymphocytes"; Salin).  => MEASURED (human) that most non-cycling malignant lymphoid cells die by interphase apoptosis; a resistant minority exists (~15%).
- 19351849 (Firat 2009 Cancer Res): "radiosensitivity of resting lymphoid cells ... strongly depend on p53" (mouse). Verified.
- 10549603 (Meijer 1999 IJRB): human G0 peripheral lymphocytes: interphase apoptosis after 1-3 Gy; growth factors rescue it; dose-rate effect on reproductive death. Verified (qualitative).
- 18220472 (Belloni 2008 Radiat Res): G0 human lymphocytes: apoptosis eliminates cells with dicentrics. 
- Maeda 2016 (27257868) abstract verified: SF2 0.19-0.93 across 27 lines; "no significant correlation of SF2 with S-phase fraction, doubling time, chromosome number, ploidy"; correlation with plating efficiency.
- 10406057 (Aref 1999): human chemo-resistant DLBCL lines WSU-DLCL2, SK-DHL2B: SF2 0.42, 0.35; alpha/beta 2 and 8.6 Gy; repair sublethal damage. Verified.
- 1429095 (Uckun 1992): n=42 primary T-lineage ALL/NHL: mean SF2 0.36+/-0.04, alpha 0.558; 14/42 SF2>=0.50 and alpha<=0.2; CD3+ (n=28) SF2 0.441, D0 189.6 cGy; CD3- (n=14) SF2 0.189, D0 108.7 cGy. Verified (already in record).

### Q2 stem/progenitor
- 20619763 (Milyavsky 2010 Cell Stem Cell): human HSC (quiescent, CD34+CD38-) show delayed DSB rejoining, persistent gH2AX, ENHANCED p53/ASPP1-dependent apoptosis after gamma-radiation vs progenitors. Verified. => quiescent stem cells are MORE radiosensitive for apoptosis, not less.
- 29666389 (Biechonski 2018 Sci Rep): irradiated human HSPCs (rare quiescent) undergo rapid ATM-dependent apoptosis, unlike committed progenitors; reduced NHEJ; clonal aberrations in 10% of survivors; stroma suppresses apoptosis. Verified.
- 6582910 (Kimler 1984): human marrow CFU-C D0 avg 0.88 Gy, no shoulder; AML colony-forming cells D0 0.66 Gy; no recovery from sublethal damage. Verified. 3610711: normal CFU-C D0 0.98 Gy (0.83-1.19), n 0.99. Verified. (committed progenitors, not quiescent HSC.)
- Dog: 920 cGy TBI lethal; 700 cGy survivable with intensive care; >=800 cGy marrow aplasia without HCT (19747631). Verified. 
