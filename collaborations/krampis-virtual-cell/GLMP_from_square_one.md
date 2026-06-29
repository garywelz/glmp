# GLMP From Square One
**Gary Welz · CUNY Graduate Center · June 2026**  
*Prepared for the Krampis meeting — for collaborators and students*

---

## The core idea in one sentence

DNA contains not just the recipes for proteins, but the **logic** that controls when and where those recipes are used — and we can read that logic computationally, the same way a compiler reads a program.

---

## The problem GLMP solves

Biologists have spent decades identifying individual transcription factors and their binding sites. But the field lacks a systematic way to represent the **logical relationships** between them — the AND gates, OR gates, feedback loops, and conditional switches that make a cell respond intelligently to its environment.

GLMP proposes that regulatory DNA has a **grammar**: transcription factor binding motifs are the alphabet, their spatial arrangement is the syntax, and the logical operations (AND / OR / NOT / IF-THEN) are the semantics. If that's right, we can read any regulatory sequence as a logical formula.

---

## The five-class complexity ladder

GLMP organizes regulatory circuits into five classes of increasing complexity:

| Class | Structure | Example |
|---|---|---|
| I | Feed-forward, no feedback | Simple activation cascade |
| II | Single feedback loop | lac operon (repressor + activator) |
| III | Multi-regulator with repressor titration | yeast GAL system |
| IV | Bistable switch | Phage lambda lysis/lysogeny |
| V | Oscillator | Circadian clock |

This ladder is the backbone of the GLMP corpus — every decoded circuit gets classified here.

---

## The DNA Decoder (what we just built)

The Decoder is a software pipeline that takes a DNA promoter sequence and produces a typed logical flowchart:

```
DNA sequence (FASTA)
        ↓
FIMO motif scanner
(finds transcription factor binding sites using JASPAR 2024 motif database)
        ↓
GLMP Logic Parser
(interprets spatial arrangement as AND/OR/NOT logic)
        ↓
Mermaid flowchart + GLMP class assignment
```

**Current status:** Successfully decoding three E. coli circuits — lac operon, ara operon, trp operon. Next target: yeast GAL system (first eukaryotic circuit, Class III).

---

## What we need from biology collaborators

The Decoder produces logical annotations automatically. What it cannot do is verify whether those annotations are **biologically correct**. That requires:

1. **Binding site review** — do the FIMO hits correspond to experimentally validated sites in the literature?
2. **Topology check** — does the flowchart topology match what is known about the circuit's actual regulatory logic?
3. **Class assignment validation** — is our complexity classification consistent with the biological evidence?

This is the role we are inviting the Krampis lab to play — and where a student collaborator could make a direct, meaningful contribution starting immediately.

---

## The immediate student task

The lac operon annotation is the first validation target. It is the best-studied regulatory circuit in biology, with decades of experimental literature. A student reviewer would:

- Compare FIMO-detected binding sites against RegulonDB (the curated E. coli regulatory database)
- Flag any sites that are missing, misplaced, or incorrectly classified as activator vs. repressor
- Confirm the logical topology (LacI represses, CRP activates, both required for full induction)

This is a well-scoped, learnable task with clear success criteria — ideal for a summer project.

---

## The bigger picture

GLMP is building a training corpus of decoded regulatory circuits that could eventually be used to train a model capable of reading any regulatory sequence as a logical formula — in any organism. The decoder running today on E. coli is the proof of concept. The yeast GAL system is the first step toward generalization. The goal is a grammar of life's control layer.

---

## Links

- GitHub: github.com/garywelz/glmp
- GitHub Pages (annotated lac operon): garywelz.github.io/glmp
- Methods paper (Zenodo): doi.org/10.5281/zenodo.20831780
- Contact: gwelz@gc.cuny.edu · ORCID: 0009-0005-7806-0892
