
# ProcessDSL + FlowCell-10 Proposal

This proposal outlines a pilot initiative to integrate the **"genome as program"** concept and **cellular process flowcharting** into the Virtual Cell project.  
The goal is to formalize biological processes as executable, interpretable programs that can be learned, simulated, and manipulated by AI.

---

## 1. ProcessDSL Specification

**ProcessDSL** is a domain-specific language for representing cellular processes.  
It compiles human-readable flowcharts into machine-executable forms such as stochastic rule systems, Petri nets, or hybrid ODE/event simulators.

**Key features:**
- Reactions as rules with explicit guards and rate constants.
- Conditional logic (`IF/ELSE`) for regulation.
- Iterative loops (`WHILE`) for cyclic processes.
- Event triggers for environmental or signaling changes.
- Support for compartments (nucleus, cytosol, organelles).

---

## 2. FlowCell-10 Pilot Dataset

**FlowCell-10** is a curated set of ten well-characterized yeast pathways, each represented as:
1. A canonical flowchart  
2. A ProcessDSL file  
3. Reference simulation outputs from literature data  

**Example pathways:**
1. Glycolysis
2. TOR nutrient sensing pathway
3. Heat shock response
4. Autophagy initiation
5. Unfolded protein response (UPR)
6. Cell cycle G1/S transition
7. Mitochondrial respiration control
8. Amino acid biosynthesis regulation
9. Gluconeogenesis
10. Alcoholic fermentation

---

## 3. Example ProcessDSL (Glycolysis)

```text
process Glycolysis in Cytosol:
  state: [Glucose, G6P, F6P, F16BP, G3P, DHAP, PEP, Pyruvate, ATP, ADP, NAD+, NADH]
  rule Hexokinase: Glucose + ATP -> G6P + ADP  [guard: ATP>θ1]
  rule PFK: F6P + ATP -> F16BP + ADP           [guard: ATP<θ2 & AMP>θ3]
  rule Aldolase: F16BP -> G3P + DHAP
  rule TPI: DHAP <-> G3P
  rule PyruvateKinase: PEP + ADP -> Pyruvate + ATP [allosteric: F16BP activates]
  event GlucosePulse(t=0..T): inflow rate r_in
```

---

## 4. Glycolysis Flowchart (Mermaid)

```mermaid
flowchart TD
    A[Glucose Uptake<br/>(Transport into cell)]
      --> B[Hexokinase<br/>Glucose → G6P]
    B --> C[Isomerase<br/>G6P → F6P]
    C --> D[Phosphofructokinase (PFK)<br/>F6P → F1,6BP]
    D --> E1[DHAP<br/>(Dihydroxyacetone phosphate)]
    D --> E2[G3P<br/>(Glyceraldehyde‑3‑phosphate)]
    E1 -- TPI forward --> E2
    E2 -- TPI reverse --> E1
    E2 --> F[G3P Oxidation & Phosphorylation<br/>(NADH + ATP yield)]
    F --> G[Phosphoglycerate Mutase & Enolase<br/>→ PEP]
    G --> H[Pyruvate Kinase<br/>PEP → Pyruvate + ATP]
    H --> I[End Product:<br/>2 Pyruvate Molecules]
```

---

## 5. TORC1 Nutrient Sensing Pathway

This diagram shows the TORC1 pathway in *Saccharomyces cerevisiae*, including nutrient signal integration, bifurcated signaling, and autophagy suppression vs activation under stress conditions.

![TORC1 Flowchart](torc1.png)

---

## 6. Deliverables

- ProcessDSL specification and parser.
- FlowCell-10 diagrams, DSL files, and simulation benchmarks.
- Jupyter notebook demo: diagram → ProcessDSL → simulation → data comparison.
- Documentation for extending the dataset.

---

## 7. Benefits to the Virtual Cell Project

- Provides an interpretable, executable representation of cellular processes.
- Bridges molecular prediction tools (e.g., AlphaFold 3) to systems-level dynamics.
- Enables counterfactual simulations and intervention planning.
- Creates training data for AI models to learn biological program induction.

---

## 8. Suggested DeepMind Contacts

1. **Demis Hassabis** – CEO, DeepMind (vision for Virtual Cell)  
2. **Pushmeet Kohli** – Head of AI for Science, DeepMind  
3. **John Jumper** – Lead researcher on AlphaFold  
4. **Kathryn Tunyasuvunakool** – Research scientist, AlphaFold/biology modeling  
5. **Alexander Zisserman** – Research scientist, graph and vision integration  
