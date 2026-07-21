# Shared diagrams — GLMP / lac–ara–trp (for Prof. Lents)

Two layers, on purpose.

- **Layer 1 — simplified teaching views** (below): my distilled models, built to make *one* idea unmissable — where sequence-readable logic ends. These are my simplifications; treat them as "my model, please correct."
- **Layer 2 — canonical database entries**: the full, cited flowcharts (50–70 nodes each) with a built-in "Improve this process" form. These are the authoritative record.

Neither replaces the other: the teaching views give the idea in a glance; the canonical entries give the whole truth.

## Color legend

| Color | Meaning |
|---|---|
| 🟪 Purple diamond | logic gate / decision (AND, NOT). **A coral outline marks a Tier-3 gate** — real logic, not readable from sequence. |
| 🟩 Green | expression output — and **readable from sequence** (Tier 1) |
| 🟨 Yellow | input signal — and **permitted / geometrically possible** (Tier 2) |
| 🟥 Coral | repression / off — and **requires the living cell** (Tier 3) |
| 🟦 Blue | CRP / CAP activation |
| 🟧 Orange | gene → protein / regulator entity |

---

# Layer 1 — Simplified teaching views (my models — please correct)

## The tiering method (our shared tool)

```mermaid
flowchart TD
    F["A regulatory feature<br/>(a site, a spacing, a bend)"] --> Q{"How is it settled?"}
    Q -->|"read directly from sequence"| T1["Readable — Tier 1<br/>site identity, repression / NOT"]
    Q -->|"sequence shows it's possible"| T2["Permitted — Tier 2<br/>looping geometrically feasible"]
    Q -->|"only the living system tells us"| T3["Needs the cell — Tier 3<br/>real cooperativity, the AND, bistability"]
    subgraph KEY[" key "]
      direction LR
      kQ["decision / gate"]
      k1["readable (T1)"]
      k2["permitted (T2)"]
      k3["needs the cell (T3)"]
    end
    style F fill:#eceff1,stroke:#607d8b,color:#000
    style Q fill:#e1bee7,stroke:#4a148c,stroke-width:2px,color:#000
    style T1 fill:#c8e6c9,stroke:#1b5e20,stroke-width:2px,color:#000
    style T2 fill:#fff9c4,stroke:#f57f17,stroke-width:2px,color:#000
    style T3 fill:#ffccbc,stroke:#bf360c,stroke-width:2px,color:#000
    style kQ fill:#e1bee7,stroke:#4a148c,color:#000
    style k1 fill:#c8e6c9,stroke:#1b5e20,color:#000
    style k2 fill:#fff9c4,stroke:#f57f17,color:#000
    style k3 fill:#ffccbc,stroke:#bf360c,color:#000
```

## lac — Tier-3 AND via DNA looping

```mermaid
flowchart TD
    GL["glucose low → cAMP high"] --> CRP["CRP–cAMP active (activator)"]
    LAC["lactose present → allolactose"] --> REL["LacI released from operators"]
    CRP --> AND{"AND — Tier 3<br/>realized via 3-D looping,<br/>not readable from sequence"}
    REL --> AND
    AND -->|both true| EXP["operon strongly expressed"]
    AND -->|either false| OFF["repressed / basal"]
    CRP -. "CRP bend also assists the LacI O1–O3 loop —<br/>this coupling is what makes it a genuine<br/>cooperative AND (Ω ≈ 10)" .-> AND
    subgraph KEY[" key "]
      direction LR
      kI["input"]
      kC["CRP / activation"]
      kR2["repressor entity"]
      kG["logic gate"]
      kE["expression"]
      kO["off"]
    end
    style GL fill:#fff9c4,stroke:#f57f17,color:#000
    style LAC fill:#fff9c4,stroke:#f57f17,color:#000
    style CRP fill:#b3e5fc,stroke:#01579b,stroke-width:2px,color:#000
    style REL fill:#ffb74d,stroke:#e65100,stroke-width:2px,color:#000
    style AND fill:#e1bee7,stroke:#bf360c,stroke-width:3px,color:#000
    style EXP fill:#c8e6c9,stroke:#1b5e20,stroke-width:2px,color:#000
    style OFF fill:#ffccbc,stroke:#bf360c,color:#000
    style kI fill:#fff9c4,stroke:#f57f17,color:#000
    style kC fill:#b3e5fc,stroke:#01579b,color:#000
    style kR2 fill:#ffb74d,stroke:#e65100,color:#000
    style kG fill:#e1bee7,stroke:#4a148c,color:#000
    style kE fill:#c8e6c9,stroke:#1b5e20,color:#000
    style kO fill:#ffccbc,stroke:#bf360c,color:#000
```

## ara — Tier-3 AND via the AraC loop switch

```mermaid
flowchart TD
    NOARA["arabinose absent"] --> LOOP["AraC loops araO2–araI1 (~210 bp)"]
    LOOP --> REP["araBAD repressed"]
    ARA["arabinose present"] --> BREAK["loop breaks; AraC → araI1–araI2"]
    GL["glucose low → cAMP high"] --> CRP["CRP–cAMP active"]
    BREAK --> AND{"AND — Tier 3<br/>needs arabinose + cAMP/CRP;<br/>the loop is 3-D, not sequence-readable"}
    CRP --> AND
    AND -->|both true| EXP["araBAD expressed"]
    AND -->|not both| OFF["off / basal"]
    subgraph KEY[" key "]
      direction LR
      kI["input"]
      kC["CRP / activation"]
      kL["loop / entity"]
      kG["logic gate"]
      kE["expression"]
      kO["off"]
    end
    style NOARA fill:#fff9c4,stroke:#f57f17,color:#000
    style ARA fill:#fff9c4,stroke:#f57f17,color:#000
    style GL fill:#fff9c4,stroke:#f57f17,color:#000
    style CRP fill:#b3e5fc,stroke:#01579b,stroke-width:2px,color:#000
    style LOOP fill:#ffb74d,stroke:#e65100,stroke-width:2px,color:#000
    style BREAK fill:#ffb74d,stroke:#e65100,color:#000
    style AND fill:#e1bee7,stroke:#bf360c,stroke-width:3px,color:#000
    style EXP fill:#c8e6c9,stroke:#1b5e20,stroke-width:2px,color:#000
    style REP fill:#ffccbc,stroke:#bf360c,color:#000
    style OFF fill:#ffccbc,stroke:#bf360c,color:#000
    style kI fill:#fff9c4,stroke:#f57f17,color:#000
    style kC fill:#b3e5fc,stroke:#01579b,color:#000
    style kL fill:#ffb74d,stroke:#e65100,color:#000
    style kG fill:#e1bee7,stroke:#4a148c,color:#000
    style kE fill:#c8e6c9,stroke:#1b5e20,color:#000
    style kO fill:#ffccbc,stroke:#bf360c,color:#000
```

## trp — Tier-3 crossing via attenuation (a *different* mechanism)

trp's repression is a clean Tier-1 NOT. But its second layer, attenuation, crosses the same boundary a different way: the trpL hairpin *geometry* is sequence-permitted (Tier 2), while *which* hairpin forms — terminator vs antiterminator — is set by ribosome speed and tRNA charging (Tier 3). Two unrelated mechanisms, one boundary.

```mermaid
flowchart TD
    LO["tryptophan scarce"] --> INACT["TrpR inactive → operator free"]
    HI["tryptophan abundant"] --> ACT["TrpR + trp → represses"]
    ACT --> NOT{"NOT — Tier 1<br/>repression, readable from sequence"}
    INACT --> NOT
    NOT -->|repressed| OFF1["operon off"]
    NOT -->|operator free| HAIR["trpL hairpin geometry<br/>Tier 2 — sequence-permitted"]
    HAIR --> DEC{"terminator or antiterminator?<br/>Tier 3 — set by ribosome speed / tRNA,<br/>not readable from sequence"}
    DEC -->|antiterminator| EXP["trpEDCBA expressed"]
    DEC -->|terminator| OFF2["premature termination"]
    subgraph KEY[" key "]
      direction LR
      kI["input"]
      kR2["repressor entity"]
      k2["Tier 2 permitted"]
      kG["Tier-1 gate"]
      kT3["Tier-3 gate (coral outline)"]
      kE["expression"]
      kO["off"]
    end
    style LO fill:#fff9c4,stroke:#f57f17,color:#000
    style HI fill:#fff9c4,stroke:#f57f17,color:#000
    style ACT fill:#ffb74d,stroke:#e65100,stroke-width:2px,color:#000
    style INACT fill:#ffb74d,stroke:#e65100,color:#000
    style NOT fill:#e1bee7,stroke:#4a148c,stroke-width:2px,color:#000
    style HAIR fill:#fff9c4,stroke:#f57f17,stroke-width:2px,color:#000
    style DEC fill:#e1bee7,stroke:#bf360c,stroke-width:3px,color:#000
    style EXP fill:#c8e6c9,stroke:#1b5e20,stroke-width:2px,color:#000
    style OFF1 fill:#ffccbc,stroke:#bf360c,color:#000
    style OFF2 fill:#ffccbc,stroke:#bf360c,color:#000
    style kI fill:#fff9c4,stroke:#f57f17,color:#000
    style kR2 fill:#ffb74d,stroke:#e65100,color:#000
    style k2 fill:#fff9c4,stroke:#f57f17,color:#000
    style kG fill:#e1bee7,stroke:#4a148c,color:#000
    style kT3 fill:#e1bee7,stroke:#bf360c,stroke-width:3px,color:#000
    style kE fill:#c8e6c9,stroke:#1b5e20,color:#000
    style kO fill:#ffccbc,stroke:#bf360c,color:#000
```

---

# Layer 2 — Canonical database entries (full models + feedback form)

Each is the complete, cited model with an "Improve this process" form. In each, the Tier-3 point currently lives in the *text* (the derived-logic line and the sequence-annotation table) — the *diagram* still shows a plain AND/decision node. Making that node **visually** Tier-3 (a distinct color or shape, as in the teaching views above) is a proposed edit I'd value your call on; the form (tap the node, add a note or PMID) is the channel for it.

- **lac** — https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_lac_operon
- **ara** — https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_ara_operon
- **trp** — https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_trp_operon

*(trp link is `ecoli_trp_operon`, the regulatory operon with attenuation — not `ecoli_tryptophan_biosynthesis`, which is the metabolic pathway.)*

---

*Sharing note: the Mermaid teaching views render as diagrams in GitHub and the repo; if sending by email, export them as images. The canonical links open the live interactive viewer.*
