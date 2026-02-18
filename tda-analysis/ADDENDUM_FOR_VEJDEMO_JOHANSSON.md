# Addendum: TDA Analysis of GLMP Biological Processes

## Methods

**Data:** 108 genetic regulatory processes from the Genome Logic Modeling Project (GLMP), spanning E. coli (66), S. cerevisiae (38), and Bacillus subtilis (4).

**Features:** Each process is represented by 5 numerical features: node count, conditional count, OR gates, AND gates, and NOT gates. Features were standardized (zero mean, unit variance) before computing persistent homology.

**TDA:** Vietoris-Rips filtration via Ripser (maxdim=2), Euclidean distance on the feature space.

---

## Most Persistent Homology Features

### H1 (Loops) - Top 5 by persistence

- Rank 1: birth=1.148, death=1.478, persistence=0.330
- Rank 2: birth=1.537, death=1.845, persistence=0.308
- Rank 3: birth=1.114, death=1.416, persistence=0.302
- Rank 4: birth=1.186, death=1.469, persistence=0.283
- Rank 5: birth=1.293, death=1.524, persistence=0.231

### H2 (Voids) - All 4 features

- birth=1.668, death=1.760, persistence=0.092
- birth=1.453, death=1.500, persistence=0.047
- birth=1.555, death=1.587, persistence=0.032
- birth=1.703, death=1.704, persistence=0.002

---

## Questions for Discussion

1. **Biological interpretation of H1:** Do any of these persistent loops correspond to known feedback structures (e.g., lac operon, SOS response, two-component signaling)? How might we map specific processes to the most persistent H1 features?

2. **Feature selection:** We used structural counts (nodes, gates). Would graph-based features (cycles, path lengths, clustering) or a different encoding improve biological interpretability?

3. **Next steps:** Would Mapper, persistent cohomology, or bottleneck/Wasserstein distances between organism or category subgroups be natural extensions to explore?
