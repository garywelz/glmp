# TDA Analysis of GLMP Biological Processes — One-Page Summary

**Prepared for:** Dr. Mikael Vejdemo-Johansson  
**From:** Gary Welz  
**Date:** February 2026  

---

## What We Did

We applied topological data analysis (TDA) to 108 genetic regulatory circuits from the Genome Logic Modeling Project (GLMP). Each circuit is represented as a Mermaid flowchart with nodes, conditionals, and logic gates (OR, AND, NOT). We extracted 5 features per process, standardized them, and computed persistent homology (Vietoris-Rips, Ripser, maxdim=2).

## Main Results

| Homology | Count | Interpretation |
|----------|-------|----------------|
| H0 (components) | 108 | One per process |
| **H1 (loops)** | **33** | Potential feedback/cyclic structure |
| **H2 (voids)** | **4** | Higher-dimensional cavities |

The 33 H1 features and 4 H2 features indicate nontrivial topological structure in the process space.

## Why This Might Be Interesting

- **Domain:** Genetic circuits have inherent topology (feedback loops, regulatory cascades). TDA may reveal structure that correlates with known biology.
- **H1 peaks:** The 5 most persistent H1 features have persistence 0.23-0.33 (birth ~1.1-1.5, death ~1.4-1.8). These could correspond to circuits with distinct feedback architectures.
- **Collaboration angle:** I bring domain knowledge (which circuits have feedback vs feedforward); you bring TDA methods. The diagrams are a shared object for interpretation.

## Attachments

1. **glmp_persistence_diagram.png** - Persistence diagram (H0, H1, H2)
2. **glmp_tda_report.html** — Full report with feature statistics
3. **glmp_features.csv** — Raw feature data (108 rows × 10 columns)
4. **ADDENDUM_FOR_VEJDEMO_JOHANSSON.md** — Methods, key persistence values, discussion questions

## Questions I’d Like to Explore

1. Do any persistent H1 loops correspond to known feedback circuits?
2. Would graph-based or alternative features improve interpretability?
3. Would Mapper, persistent cohomology, or subgroup comparisons be natural next steps?
