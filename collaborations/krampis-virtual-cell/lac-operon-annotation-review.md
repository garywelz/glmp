# Lac Operon Binding Site Annotations — Expert Review Request
**Genome Logic Modeling Project (GLMP)**
**Gary Welz · gwelz@gc.cuny.edu · ORCID: 0009-0005-7806-0892**
**Version: July 2026 (revised — decoder-honesty correction) · Status: Awaiting biological validation**

---

## Purpose of this document

This document presents sequence-level annotations for three nodes in the *Escherichia coli* lac operon (*E. coli* K-12 MG1655), prepared as part of the Genome Logic Modeling Project (GLMP). The annotations are the first ground-truth training entries for the GLMP grammar-decoding corpus — a program to systematically extract logical structure from regulatory DNA sequences.

The GLMP grammar holds that the spatial arrangement of transcription factor binding sites encodes logical operations:
- **AND logic:** cooperative binding sites spaced ~15–50 bp apart
- **OR logic:** independent sites spaced >50 bp apart
- **NOT logic:** repressor binding site overlapping or adjacent to the RNA polymerase binding site, blocking transcription
- **XOR/competitive:** sites within <15 bp that sterically exclude each other

Each annotation entry below states: the binding site DNA sequence, genomic coordinates, inter-site distances, the logical type assigned by the GLMP grammar rules, the confidence level, and the source evidence. The question for the expert reviewer is: **does the logical interpretation accurately reflect the molecular biology?**

---

## Annotation Entry 1 — lacO1 Operator (NOT gate)

**Node name in GLMP flowchart:** `LacI repressor at operator`

**Logical type:** NOT gate
**Logical interpretation:** LacI binding at lacO1 blocks RNA polymerase access to the lac promoter, repressing lacZYA transcription. In the absence of allolactose (the inducer), LacI occupies the operator and transcription is blocked. This is the archetypal NOT gate: the product of LacI binding is the *absence* of transcription.

**Binding site sequence (lacO1):**
```
5'-AATTGTGAGCGGATAACAATT-3'
```
Length: 21 bp
Strand: Non-template strand shown; LacI binds as a dimer recognizing this palindromic sequence.

**Genomic coordinates (E. coli K-12 MG1655, GenBank U00096):**
- Start: 365,906
- End: 365,926
- Strand: −
- Locus context: Overlaps the lac promoter region; positioned between the −10 element and the transcription start site (+1)

**Position weight matrix source:** RegulonDB (regulondb.ccg.unam.mx), LacI binding site collection; JASPAR matrix MA0109 (LacI)

**Evidence class:** High — experimentally validated to nucleotide resolution by DNase I footprinting and chemical modification interference. Gilbert and Maxam (1973) established the sequence; Lewis et al. (1996) resolved the LacI-DNA co-crystal structure.

**GLMP grammar rule applied:** NOT — repressor binding site overlaps RNAP binding site, preventing polymerase engagement. The operator position (between −10 and +1) places LacI directly in the path of RNAP.

**Inter-site distances:**
- Distance from lacO1 to CRP binding site (Entry 2 below): approximately 60 bp upstream (center-to-center)
- Distance from lacO1 to lacO2 (auxiliary operator, not annotated here): approximately 410 bp downstream in lacZ coding sequence
- Distance from lacO1 to lacO3 (auxiliary operator, not annotated here): approximately 92 bp upstream

**Notes for reviewer:**
The GLMP grammar assigns NOT based on the spatial relationship between the repressor binding site and the RNAP binding site — this call is sequence-confirmed and not in question. The ~60 bp distance between lacO1 and the CRP site exceeds the ~50 bp cooperative-spacing threshold, so the decoder cannot type a cooperative AND relationship between them from geometry alone. **Honest decoder read for this circuit: Class I/II** — repression confirmed, activation not sequence-confirmable. Biologically, full induction requires both relief of repression and CRP activation (Class II, the textbook logic), but that is a curated/literature determination, not something the current spacing-based method can confirm from sequence. See Entry 2 for the open question this raises.

**Reviewer validation question:**
Is the lacO1 sequence correct? Are the coordinates accurate for K-12 MG1655? Is the NOT gate assignment — repressor binding blocks RNAP — correctly stated? Is the ~60 bp distance to the CRP site the right figure for the center-to-center measurement?

---

## Annotation Entry 2 — CRP Binding Site (biological activator; not sequence-confirmed as AND)

**Node name in GLMP flowchart:** `cAMP-CAP assists promoter?` (decision diamond)

**Logical type:** Biological activator (curated) — **not** decoder-confirmed as a sequence-level AND gate
**Logical interpretation:** The CRP-cAMP complex (catabolite activator protein bound to cyclic AMP) binds upstream of the lac promoter and makes direct protein-protein contact with the C-terminal domain of the RNA polymerase alpha subunit (αCTD), stimulating open complex formation. Under high glucose conditions, cAMP levels are low and CRP does not productively engage the promoter — transcription is weak even when LacI is off the operator. Biologically, strong induction requires both conditions: operator unoccupied (Entry 1) and CRP productively engaged (this entry) — the textbook Class II logic of the lac operon. **This is well-established biology, not a decoder finding.** The GLMP sequence decoder cannot confirm this AND relationship from spacing alone: *lac* has a single activator (CRP) with no second site to cooperate with, and spacing-based AND detection is structurally unable to type single-activator promoters — it either misses the logic or, as an earlier decoder build did, fabricates an AND call from motif noise (see the honest-status brief for detail). The decoder's honest sequence-level read for this circuit is Class I/II: repression confirmed, activation not sequence-confirmable.

**Binding site sequence (CRP consensus):**
```
5'-TGTGA-N6-TCACA-3'
```
Specific lac promoter CRP site sequence:
```
5'-TGTGTGGAATTGTGAGC-3'  (approximate; see note)
```
Length: ~22 bp (CRP binds as a dimer to a pseudopalindromic sequence)

**Genomic coordinates (E. coli K-12 MG1655):**
- Center of CRP binding site: approximately 365,966 (−61 relative to transcription start +1)
- Strand: CRP binds double-stranded DNA; contact with αCTD is on the upstream face

**Position weight matrix source:** RegulonDB CRP binding site collection; JASPAR matrix MA0334 (CRP/CAP)

**Evidence class:** High — CRP-lac promoter interaction characterized biochemically by Busby and Ebright (1999); structural contacts between CRP and αCTD resolved by Benoff et al. (2002).

**GLMP grammar rule applied:** No AND call is made from sequence for this site. Inter-site distance (~60 bp, exceeding the ~50 bp cooperative-spacing threshold) rules out a sequence-detectable cooperative AND between CRP and LacI. The biological AND (both inputs required for RNAP to form a productive open complex) is asserted from curated literature, not derived from the decoder's spatial-geometry rule.

**Inter-site distances:**
- Distance from CRP site to lacO1: approximately 60 bp (center-to-center); exceeds the cooperative-spacing threshold, so no sequence-level AND is typed
- Distance from CRP site to −35 element: approximately 22 bp upstream contact point for CRP-αCTD interaction

**Notes for reviewer:**
The specific lac promoter CRP site sequence shown above is approximate — the exact sequence depends on the reference strain and numbering convention used. The reviewer is asked to confirm or correct this sequence and the coordinate given. Separately, there is an open modeling question worth the team's judgment: should a promoter be typed as Class II when it carries a confident activator and a confident repressor, even absent cooperative spacing? That may be more principled than the spacing heuristic — but it should be reasoned through with the review team, not adopted just to recover a nicer label.

**Reviewer validation question:**
Is the CRP binding site sequence correct for K-12 MG1655? Is the ~61 bp distance from the transcription start site correct? Is the biological description of CRP's role — required but not sufficient for strong transcription, and mechanistically independent of LacI — accurate? Separately: does a confident activator plus a confident repressor, without cooperative spacing, warrant a Class II call?

---

## Annotation Entry 3 — lacI Gene Locus (repressor source node)

**Node name in GLMP flowchart:** `lacI gene → transcription → LacI protein`

**Logical type:** Source node (gene expression producing the NOT gate regulator)
**Logical interpretation:** The *lacI* gene is transcribed constitutively from its own promoter (Plac I) at a low level, producing approximately 10 LacI repressor molecules per cell under standard conditions. LacI assembles as a tetramer in vivo. The *lacI* gene is upstream of the lac operon and is not regulated by the same two-input logic that controls lacZYA — it has its own promoter and is largely insensitive to catabolite repression. This node matters for perturbation design: tuning *lacI* expression (CRISPRi, promoter replacement, copy number) directly sets the intracellular LacI concentration and thus the threshold for induction.

**Genomic locus:**
- Gene: *lacI*
- Locus tag: b0345 (E. coli K-12 MG1655)
- GenBank coordinates: complement(365,163..366,305)
- Promoter (Plac I): approximately 366,305–366,350 (upstream of *lacI* coding sequence)
- Strand: − (transcribed in reverse complement direction relative to lac operon)

**Expression level:** ~10 LacI monomers per cell (constitutive, low-level expression from Plac I); assembles as a tetramer capable of simultaneously binding lacO1 and one auxiliary operator (loop formation)

**Position weight matrix source:** Not applicable for this node — this is a gene locus, not a TF binding site. The relevant PWM is for LacI binding to *lacO* (Entry 1).

**Evidence class:** High — *lacI* constitutive expression and repressor copy number established by Müller-Hill et al. (1968) and Riggs et al. (1970); loop formation between lacO1 and auxiliary operators by Oehler et al. (1990).

**GLMP grammar rule applied:** Source node — produces the NOT gate regulator. This node has no logical type in itself; its presence in the flowchart is required for the diagram to be perturbation-complete (i.e., to allow an investigator to read off *lacI* expression as an experimental lever).

**Notes for reviewer:**
This entry differs from Entries 1 and 2 in that it does not carry a logical gate assignment — it is a gene expression node, not a binding event. Its inclusion in the hybrid flowchart is motivated by entity completeness: without a first-class *lacI* node, the repressor appears to exist without origin, and perturbations targeting *lacI* expression are invisible in the diagram. The GLMP annotation schema treats gene locus nodes differently from binding site nodes — they carry genomic coordinates and expression level metadata rather than PWM and inter-site distance fields.

**Reviewer validation question:**
Is the *lacI* constitutive expression level (~10 monomers per cell) the right figure to cite, or is there a more current or precise estimate? Are the locus tag and coordinates correct for K-12 MG1655? Is the characterization of Plac I as largely insensitive to catabolite repression accurate, or are there conditions where *lacI* expression is significantly modulated?

---

## Summary table

| Entry | Node | Logical type | Key sequence | Confidence | Primary source |
|---|---|---|---|---|---|
| 1 | lacO1 operator | NOT gate | AATTGTGAGCGGATAACAATT | High | Gilbert & Maxam 1973; Lewis et al. 1996 |
| 2 | CRP binding site | Activator (curated) — not sequence-confirmed as AND | TGTGA-N6-TCACA | High (biology); not sequence-confirmable (AND) | Busby & Ebright 1999; Benoff et al. 2002 |
| 3 | lacI gene locus | Source node | b0345 (locus tag) | High | Müller-Hill et al. 1968; Oehler et al. 1990 |

**Decoder honest read for this circuit: Class I/II** (repression confirmed, cooperative activation not sequence-confirmable). Curated biological class: II. This gap is the open question posed to the review team — not a contradiction to paper over.

---

## References cited in this document

- Benoff B, et al. Structural basis of transcription activation: the CAP-αCTD-DNA complex. *Science*. 2002;297(5586):1562–1566.
- Busby S, Ebright RH. Transcription activation by catabolite activator protein (CAP). *J Mol Biol*. 1999;293(2):199–213.
- Gilbert W, Maxam A. The nucleotide sequence of the lac operator. *Proc Natl Acad Sci USA*. 1973;70(12):3581–3584.
- Lewis M, et al. Crystal structure of the lactose operon repressor and its complexes with DNA and inducer. *Science*. 1996;271(5253):1247–1254.
- Müller-Hill B, Crapo L, Gilbert W. Mutants that make more lac repressor. *Proc Natl Acad Sci USA*. 1968;59(4):1259–1264.
- Oehler S, Eismann ER, Krämer H, Müller-Hill B. The three operators of the lac operon cooperate in repression. *EMBO J*. 1990;9(4):973–979.
- Riggs AD, Bourgeois S, Cohn M. The lac repressor-operator interaction. III. Kinetic studies. *J Mol Biol*. 1970;53(3):401–417.

---

## What the reviewer is being asked to do

For each of the three entries above, please indicate:

1. **Sequence correct / incorrect** — is the binding site sequence accurate for E. coli K-12 MG1655?
2. **Coordinates correct / incorrect** — are the genomic coordinates in the right range?
3. **Logical interpretation correct / incorrect** — does the GLMP logical type assignment (NOT, biological activator, source node) accurately reflect the molecular biology?
4. **Any material omissions** — is there something about the binding event or its regulatory context that the annotation misrepresents or leaves out that would affect the logical interpretation?

Corrections and comments in any format are welcome — annotated PDF, email, or comments in the GitHub repo (https://github.com/garywelz/glmp).

---

*Gary Welz · CUNY Graduate Center / New Media Lab · Genome Logic Modeling Project*
*gwelz@gc.cuny.edu · ORCID: 0009-0005-7806-0892*
*Document version: June 2026*
