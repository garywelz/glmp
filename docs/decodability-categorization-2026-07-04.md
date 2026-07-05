# Decodability Categorization — Batch 9 INSUFFICIENT_EVIDENCE Circuits

> ## ⚠️ PROVISIONAL / CONFOUNDED — NOT A VALID FINDING
>
> **Known confounds:**
> 1. **Several circuits (`trpR`, `argR`, `crp`, `fnr`, `soxS`) were anchored on the TF's OWN autoregulatory promoter**, not the operons that TF regulates. Their `INSUFFICIENT_EVIDENCE` results **do not test the biological circuit** named in the GLMP catalog.
> 2. **`mutM` uses a σ32 promoter** (RegulonDB PromoterSet); sigma factor is **not modeled** in `glmp_logic_parser.py`, and the documented −35/−10 constant is **unused at runtime** — but this promoter class is outside what the pipeline was designed or validated for.
>
> **The ≈50/50 bucket split and per-circuit decodability assignments below are NOT valid** pending a re-anchored re-run on regulated-operon promoters. This document is retained as an **honest lab-notebook entry** — flaws labeled, not hidden.

**Status: PROVISIONAL — RegulonDB-grounded proposal, pending biological validation AND re-anchoring**

**Date:** 2026-07-04  
**Context:** Jetson batch decode (`run_batch.py` v0.2.2); 10 E. coli circuits processed; 9 returned `dna_topology_class: INSUFFICIENT_EVIDENCE`; 1 (`ecoli_dna_damage_checkpoint`) decoded Class II via LexA custom PWM.  
**Data source:** RegulonDB **v14.5.0** flat files staged at `gs://regal-scholar-453620-r7-podcast-storage/validation/regulondb-v14/` (release 2026-01-28; NC_000913.3).  
**Method:** Read-only lookup of `PromoterSet.tsv`, `TF-RISet.tsv`, and `NetworkRegulatorGene.tsv` at the manifest anchor promoter (TSS + `firstGeneName` from each queue manifest). No decoder, PWM, or confidence-gate changes.

Each row is a **proposal** for Gary + a biologist to review — not settled findings.

---

## Anchor promoters (decode windows)

| circuit_id | anchor gene | TSS | promoter ID (RegulonDB) | σ factor (PromoterSet) |
|------------|-------------|-----|-------------------------|------------------------|
| `ecoli_aerobic_respiration` | cyoA | 451653 | RDBECOLIPMC03439 (cyoAp) | sigma70 (Strong) |
| `ecoli_amino_acid_biosynthesis` | trpR | 4632704 | RDBECOLIPMC03404 (trpRp) | sigma70 (Confirmed) |
| `ecoli_anaerobic_respiration` | fnr | 1399552 | RDBECOLIPMC03356 (fnrp) | sigma70 (Weak) |
| `ecoli_antibiotic_efflux_pumps` | soxS | 4277423 | RDBECOLIPMC03545 (soxSp) | sigma70 (Strong) |
| `ecoli_arginine_biosynthesis` | argR | 3384677 | RDBECOLIPMC03339 (argRp1) | sigma70 (Strong) |
| `ecoli_base_excision_repair` | mutM | 3811175 | RDBECOLIPMC02823 (mutMp) | **sigma32** (Strong) |
| `ecoli_catabolite_repression` | crp | 3485953 | RDBECOLIPMC03455 (crpp1) | sigma70 (Strong) |
| `ecoli_cold_shock_response` | cspA | 3719889 | RDBECOLIPMC03679 (cspAp1) | sigma70 (Confirmed) |
| `ecoli_e._coli_osmotic_stress_response` | ompC | 2312830 | RDBECOLIPMC03385 (ompCp1) | sigma70 (Confirmed) |

---

## Proposal table

| circuit | documented regulator(s) | RegulonDB citation | mechanism (documented) | bucket | PWM-to-build (if gap) | confidence / ambiguity note |
|---------|-------------------------|-------------------|------------------------|--------|----------------------|----------------------------|
| `ecoli_aerobic_respiration` | **ArcA** (repressor); **PdhR** (repressor) | TF-RISet **RDBECOLIRIC05365** (ArcA-P → cyoAp, Confirmed); NetworkRegulatorGene ArcA→cyoA (−, C), PdhR→cyoA (−, C); PromoterSet RDBECOLIPMC03439 | ArcA-P: **two-component response regulator** (repressor at operator near cyoAp); PdhR: **repressor** (pyruvate-sensing TF, network-level) | **TWO-LAYER (partial)** | ArcA (if pursuing DNA layer); PdhR | **Needs biologist review:** GLMP catalog treats this as electron-transport *execution* (ArcAB/FNR is a separate circuit). RegulonDB documents ArcA-P repression at cyoAp, but ArcA binding competence requires **EnvZ/ArcB phosphorylation** (not in sequence). No Confirmed CRP/FNR RI at this promoter in TF-RISet. |
| `ecoli_amino_acid_biosynthesis` | **TrpR** (repressor, autoregulation) | TF-RISet **RDBECOLIRIC05057** (TrpR-L-Trp → trpRp, Strong); NetworkRegulatorGene TrpR→trpR (−, S); PromoterSet RDBECOLIPMC03404 | **Repressor at operator**; active conformation **TrpR-L-tryptophan** (effector required) | **TWO-LAYER (partial)** | TrpR (approximate matrix exists in `laci_motif.meme` but **not wired in manifest**) | Manifest anchors **trpR autoreg promoter**, not trpEDCBA operon. Even with TrpR PWM, decode would reflect **L-Trp-dependent** repression — binding competence not sequence-only. Catalog Class II note flags diagram/topology mismatch. |
| `ecoli_anaerobic_respiration` | **FNR** (dual); **IHF** (activator); **ArcA** (repressor, TF-RISet Weak) | TF-RISet **RDBECOLIRIC04176** (FNR → fnrp, repressor); **RDBECOLIRIC04175** (IHF → fnrp, activator, Confirmed); NetworkRegulatorGene FNR→fnr (−+, S), IHF→fnr (+, C); PromoterSet RDBECOLIPMC03356 | FNR: **redox-sensitive dual regulator** (anaerobic activator/repressor depending on site); IHF: **activator** (DNA architectural binding); ArcA-P: **two-component** (Weak promoter RI) | **TWO-LAYER (partial)** | FNR; IHF (partial JASPAR coverage) | FNR activity depends on **[4Fe-4S]²⁺ vs apo-FNR** (oxygen/redox), not encoded in promoter sequence. fnrp PromoterSet confidence **Weak**. |
| `ecoli_antibiotic_efflux_pumps` | **SoxR** (activator); **SoxS** (autorepressor); **AcrR** (repressor); MgrR (repressor, network) | TF-RISet **RDBECOLIRIC01395** / **RDBECOLIRIC05480** (SoxR → soxSp, activator, Confirmed); **RDBECOLIRIC05481** (SoxS → soxSp, repressor); **RDBECOLIRIC01083** (AcrR → soxSp, repressor, Strong); PromoterSet RDBECOLIPMC03545 | SoxR: **redox-sensing activator** ([2Fe-2S] oxidation → SoxR-SoxS cascade); SoxS/AcrR: **repressors at soxSp** | **TWO-LAYER (partial)** | SoxS; SoxR (if isolating soxbox); AcrR | Primary efflux logic is **SoxR → SoxS → target promoters**; soxSp window captures cascade head. SoxR activation is **redox TWO-LAYER**; SoxS/AcrR sites are DNA-bindable but lack custom PWMs. **Needs biologist review** for whether soxS promoter alone represents “efflux pumps” circuit vs full regulon. |
| `ecoli_arginine_biosynthesis` | **ArgR** (repressor, autoregulation); Fur (−, network); ArcA (+, network) | TF-RISet **RDBECOLIRIC04316**, **RDBECOLIRIC04317** (ArgR-L-Arg → argRp1, repressor); NetworkRegulatorGene ArgR→argR (−, C), Fur→argR (−, S), ArcA→argR (+, S); PromoterSet RDBECOLIPMC03339 | ArgR-L-Arg: **repressor at operator** (arginine effector); Fur: **iron-responsive repressor** (network); ArcA: **two-component** (network) | **TWO-LAYER (partial)** | ArgR | ArgR binding requires **L-arginine** (documented conformation in TF-RISet). Manifest anchors **argR autoreg**, not argCBH operon. Fur/ArcA network links may not appear in 1.2 kb window. |
| `ecoli_base_excision_repair` | **RpoN** (repressor, network only); promoter σ³² | PromoterSet RDBECOLIPMC02823 (**sigma32**); NetworkRegulatorGene RpoN→mutM (−, S); **no Confirmed/Strong TF-promoter RI** at mutMp in TF-RISet | **Sigma32 (RpoH) heat-shock promoter**; network lists RpoN repression (σ⁵⁴ TF — mechanism unclear at this promoter) | **Needs biologist review** | RpoH/σ32 (non-standard vs σ70 operator models); any SOS/Ada/OxyR sites if present outside window | Promoter is **sigma32**, not σ70 — decoder uses σ70 geometry. No documented TF binding site at mutMp at Confirmed/Strong in TF-RISet extract. RpoN network entry may be **indirect or mis-assigned** vs σ32 transcription. Repair pathway also has **damage-triggered** layers not in RegulonDB promoter map. |
| `ecoli_catabolite_repression` | **CRP** (dual); **Cra** (activator); **Fis** (repressor) | TF-RISet **RDBECOLIRIC04959** (CRP-cAMP → crpp1, activator, Confirmed); **RDBECOLIRIC04964** (CRP-cAMP repressor); **RDBECOLIRIC01077** (Cra → crpp1, activator); **RDBECOLIRIC04960–04963** (Fis → crpp1, repressor, Confirmed/Strong); NetworkRegulatorGene CRP→crp (−+, C); PromoterSet RDBECOLIPMC03455 | CRP-cAMP: **global activator/repressor** (cAMP effector); Cra: **activator**; Fis: **repressor** (growth-phase architectural) | **TWO-LAYER (partial)** | — (CRP/CAP in JASPAR as MA2303.1 but **cAMP effector** dominates) | CRP binding competence requires **cAMP** (documented as CRP-cyclic-AMP in TF-RISet). JASPAR CAP motif alone insufficient for Class call — explains INSUFFICIENT_EVIDENCE despite known biology. |
| `ecoli_cold_shock_response` | **H-NS** (repressor) | TF-RISet **RDBECOLIRIC01199** (H-NS → cspAp1, repressor, **Confirmed**); RDBECOLIRIC01196–01200 (multiple H-NS sites, Strong/Confirmed); NetworkRegulatorGene H-NS→cspA (−, C); PromoterSet RDBECOLIPMC03679 | H-NS: **repressor** (AT-rich silencing); literature also documents **post-transcriptional** cold-shock control of cspA mRNA | **Needs biologist review** | H-NS (broad silencer; partial JASPAR coverage) | RegulonDB documents **DNA-level H-NS repression** at cspAp1, but cold-shock biology is famously **mixed DNA + mRNA stability/structure**. Do not force single bucket without biologist sign-off. |
| `ecoli_e._coli_osmotic_stress_response` | **OmpR** (activator); **CpxR** (+, network); **IHF** (−); **Lrp** (−); **MicC** (−, sRNA) | TF-RISet **RDBECOLIRIC04112–04114** (OmpR-P → ompCp1, activator, **Confirmed**); NetworkRegulatorGene OmpR→ompC (+, C), CpxR (+, S), IHF (−, C), Lrp (−, S), MicC (−, S); PromoterSet RDBECOLIPMC03385 | OmpR-P: **two-component response regulator** (EnvZ phosphotransfer); MicC: **sRNA post-transcriptional** repression; CpxR: **two-component** (network) | **TWO-LAYER (partial)** | OmpR (EnvZ-phosphorylation not in sequence); CpxR if pursuing dual-TCS | OmpR-P sites at ompCp1 are **Confirmed** — classic osmotic activation — but **phosphorylation by EnvZ** is TWO-LAYER. MicC adds **RNA-layer** repression not captured by FIMO/JASPAR. **Needs biologist review** for weighting DNA vs sRNA control. |

---

## Bucket definitions (Gary's criteria)

| Bucket | Meaning |
|--------|---------|
| **DNA-DECODABLE (PWM-gap)** | Regulator binds a defined operator; binding competence is **fully sequence-determined**; decoder lacks PWM only. |
| **TWO-LAYER (partial)** | Regulator binds a defined operator (RegulonDB-documented), but **activity/competence** requires upstream signal **not in sequence** (ligand, phosphorylation, redox, cAMP, etc.). |
| **PROTEIN-NETWORK / RNA (not DNA-decodable)** | No operative sequence-encoded DNA-binding step; logic in PPI or post-transcriptional/RNA control. |
| **Needs biologist review** | RegulonDB ambiguous, mixed mechanisms, manifest/circuit scope mismatch, or σ-factor / multi-layer biology — **do not force a bucket**. |

---

## Section 1 — Scope

Nine circuits from the 2026-07-04 Jetson batch returned `INSUFFICIENT_EVIDENCE` at the DNA topology layer. This document proposes **why** (PWM gap vs effector-dependent binding vs non-DNA logic) using **only** RegulonDB v14.5.0 flat-file citations. Decoder code, confidence gates, and PWM libraries were not modified.

---

## Section 2 — Summary of proposals (by bucket)

| Bucket | Circuits (count) | Members |
|--------|------------------|---------|
| TWO-LAYER (partial) | 6 | anaerobic respiration (fnr), amino acid biosynthesis (trpR), arginine biosynthesis (argR), antibiotic efflux (soxS), catabolite repression (crp), osmotic stress (ompC) |
| Needs biologist review | 3 | aerobic respiration (cyoA), base excision repair (mutM), cold shock (cspA) |
| DNA-DECODABLE (PWM-gap) alone | 0 | — none proposed as **pure** PWM-gap without effector/two-layer caveat |
| PROTEIN-NETWORK / RNA alone | 0 | MicC (ompC) flagged as **secondary RNA layer** within TWO-LAYER / review row |

**Note:** Several TWO-LAYER rows also list PWM gaps (TrpR, ArgR, SoxS, FNR, OmpR). Gary's criterion treats effector/phosphorylation dependence as primary; PWM build alone would not yield biologically complete topology class without two-layer schema.

---

## Section 3 — Cross-cutting patterns

1. **Effector-dependent TFs dominate:** CRP-cAMP, TrpR-Trp, ArgR-Arg, FNR-redox, SoxR-redox, OmpR-P — all documented in TF-RISet with ligand/phosphorylated conformation names.
2. **Autoreg promoter anchors:** Several manifests window **TF genes** (trpR, argR, crp, fnr, soxS) rather than effector operons — decode tests autoregulation, not full pathway output.
3. **JASPAR prokaryotic gap:** Even when RegulonDB documents operators (H-NS, IHF, Fis, SoxS), JASPAR CORE lacks matrices → INSUFFICIENT_EVIDENCE unless custom PWM + confidence rules (cf. LexA success on circuit 10).
4. **σ-factor mismatch:** mutMp is **sigma32** (PromoterSet); decoder assumes σ70 −35/−10 geometry.
5. **Multi-layer biology:** cspA (mRNA), ompC (MicC sRNA), cyoA (execution vs regulation scope) — RegulonDB alone insufficient to settle decodability class.

---

## Section 4 — Recommended next steps (for review, not execution)

1. **Biologist review** of the three “needs review” rows and manifest scope (execution gene vs regulon head vs autoreg TF).
2. **Prioritize PWM builds** only where TWO-LAYER schema will also be applied (OmpR, ArgR, SoxS, FNR) — not as sole fix.
3. **Re-anchor manifests** where decode intent is operon-level (e.g. trpEDCBA, argCBH) vs TF autoreg.
4. **Document two-layer Firestore fields** for effector-dependent circuits (pattern established for yeast GAL).
5. **Do not lower confidence gates** to force Class calls from weak JASPAR hits.

---

*Generated 2026-07-04. RegulonDB v14.5.0 files: `gs://regal-scholar-453620-r7-podcast-storage/validation/regulondb-v14/`.*
