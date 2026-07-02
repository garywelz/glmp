# GLMP — From Square One
**Gary Welz · CUNY Graduate Center / New Media Lab · July 2026**
*Prepared for collaborators and students coming in fresh*
*Methods paper: https://doi.org/10.5281/zenodo.20831780*

---

## The core idea in one sentence

The DNA that controls when genes turn on and off can be read like a
computer program — the spatial arrangement of protein binding sites
encodes logical operations (AND, OR, NOT) that we can extract and
formalize computationally.

This approach is the inverse of synthetic biology work by Voigt et al.
(Science 2016), which compiles human-readable logic programs *into*
novel DNA sequences. GLMP reads the logic that evolution has already
written *into* natural regulatory DNA. The two share a grammar;
they differ in direction.

---

## What a GLMP flowchart looks like

The project began with a picture. Before any decoder, any database,
any classification system — a flowchart representing a molecular
regulatory process as a logical circuit.

The lac operon in *E. coli* is the first worked example and the
anchor for everything that follows. Its flowchart (rendered in the
HTML version of this document) shows:

- **Orange nodes** — gene expression sources (the lacI gene producing
  LacI repressor)
- **Purple diamonds** — logic gate decision points (AND, OR, NOT)
- **Green nodes** — active transcription output
- **Red nodes** — repression or NOT gate outcomes
- **Blue nodes** — environmental inputs (lactose signal, glucose/cAMP state)

The entire regulatory logic of the lac operon — one of the most studied
systems in molecular biology — is captured in this one diagram. This is
what GLMP is formalizing at scale.

*See the HTML version of this document for the rendered interactive
flowchart: glmp-from-square-one-v2.html*

---

## The five-step research process

GLMP proceeds in five steps. Steps 3 through 5 are contingent on
step 2 being answered in the affirmative. That is not a weakness —
it is how science works.

**Step 1 — Have LLMs generate flowcharts of molecular processes**

We use large language models to produce Mermaid logic-gate flowcharts
for regulatory circuits across multiple organisms and disciplines.
Each flowchart assigns gate types (AND, OR, NOT) to transcription
factor binding relationships and classifies the circuit by complexity
class (I–V). We currently have 217 processes in a structured catalog
and are actively scaling toward a target of 1,000+ circuits. Batch
flowchart generation runs automatically overnight on dedicated compute
hardware, adding new circuits continuously. In parallel, a curated
collection of embedded research papers is being built to ground each
circuit in the primary literature.

*Status: active and scaling — 217 circuits today, targeting 1,000+.*

---

**Step 2 — Have human biologists validate the faithfulness of these charts ← PIVOTAL**

A subject matter expert reviews the flowcharts and annotations against
the primary literature and curated databases, confirming that the logic
gate assignments accurately reflect observed molecular behavior.

This is what we still have not accomplished — and it is what we are
asking you and your student to help us do. All of our current and
planned work in steps 3–5 rests on this assumption being answered
in the affirmative.

*Status: open — this is the pivotal question.*

---

**Step 3 — Apply computer-assisted methods to extract the circuit logic from DNA**

Assuming the flowcharts are valid representations of real biology,
we undertake computational methods for verifying, extracting, and
teasing out the logical structure directly from DNA sequences — using
motif scanning (FIMO/JASPAR), custom binding site matrices, and a
logic parser that classifies circuits by their DNA-level topology.

This is what Gary, Krampis, and our AI collaborators are engaged in now.

*Status: active — pipeline built, first circuits decoded.*

---

**Step 4 — Publish results and scale to advanced validation methods**

If step 2 confirms the flowcharts are biologically faithful, and
step 3 produces credible and publishable results, we will write up
our findings and advance to higher-level validation — including
cross-validation against foundation models trained on genomic sequences
(such as Evo 2 from the Arc Institute) and integration with single-cell
regulatory inference tools such as RegVelo.

*Status: methods paper in preparation.*

---

**Step 5 — If accomplished at scale, proceed to the Big Picture Goals**

If steps 1 through 4 are completed at scale across hundreds or
thousands of regulatory circuits, we can consider the core theory
plausibly correct and proceed with confidence to the Big Picture
Goals — which we will describe in a future conversation once the
foundation is established.

---

## The circuit complexity classes

GLMP classifies regulatory circuits into five classes:

| Class | Structure | Biological example |
|---|---|---|
| I | Feed-forward, no feedback | Simple inducible promoter |
| II | Single negative feedback | trp operon (TrpR end-product repression) |
| III | Bistable / positive feedback | ara operon (AraC positive autoregulation) |
| IV | Oscillatory | Circadian clock (CLOCK/BMAL1) |
| V | Self-modifying | DNMT3A self-methylation |

Class III circuits are empirically harder for AI perturbation models
to predict — a finding with direct implications for the RegVelo and
K562 collaboration work.

---

## Where the decoder stands today

| Circuit | DNA topology | Biological class | Status |
|---|---|---|---|
| lac operon | Class II | Class II* | Pending validation |
| ara operon | Insufficient evidence† | Class III | Pending validation |
| trp operon | Class I/II | Class II | Pending validation |
| GAL system (yeast) | Partial | Class III/IIIa | Two-layer (protein network) |
| SOS regulon (recA) | Class II | Class II | Pending validation |
| SOS regulon (lexA) | Class II | Class II | Pending validation |

*lac Class II vs III is an open question the validation team is
asked to weigh in on.
†AraC absent from JASPAR; custom PWM in development.

---

## What we are asking from the collaboration

**Biology track:** Review lac/ara/trp flowchart annotations against
primary literature and curated databases; confirm or flag each logic
gate assignment. ~3 weeks, ~8 hours.

**Computation track:** Cross-reference FIMO-predicted binding sites
against RegulonDB gold-standard data; produce overlap statistics and
discrepancy report. ~3 weeks, ~10 hours.

A self-contained validation package — including all data files, the
annotation review document, and a detailed task brief — is available
for download. No credentials or database access required.

Expert biological reviewers are also being engaged independently.
The student's work and the expert review are complementary layers,
not redundant.

Contributions will be acknowledged in the methods paper. Co-authorship
is on the table depending on the significance of the contribution.

---

## Resources

- Methods paper: https://doi.org/10.5281/zenodo.20831780
- GitHub: https://github.com/garywelz/glmp
- Contact: gwelz@gc.cuny.edu · ORCID: 0009-0005-7806-0892
