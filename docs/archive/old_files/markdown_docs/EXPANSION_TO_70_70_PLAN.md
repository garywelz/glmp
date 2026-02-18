# GLMP Expansion Plan: 70 E. coli + 70 Yeast = 140 Total

**Current Status:** 66 E. coli + 38 Yeast + 4 Bacillus = 108 processes  
**Goal:** 70 E. coli + 70 Yeast = 140 processes (perfect balance)  
**Needed:** 4 more E. coli + 32 more Yeast

---

## Strategy

**Why 70+70=140?**
- Perfect organism balance for statistical comparisons
- Large enough sample for robust conclusions
- Clean number (not superstitious! 😊)
- The 4 Bacillus processes can remain as supplementary validation

---

## Current Coverage Analysis

### E. coli (Current: 66)

**Well-covered categories:**
- DNA/RNA Processes: 20 processes ✓
- Stress Response: 12 processes ✓
- Metabolism: 10 processes ✓
- Gene Regulation: 8 processes ✓
- Signal Transduction: 6 processes ✓

**Gaps:**
- Cell division/morphogenesis: Limited
- Quorum sensing: Only 1 process
- Biosynthesis: Could add more amino acids
- Motility/chemotaxis: Only 2 processes

---

### Yeast (Current: 38)

**Well-covered categories:**
- Signal Transduction: 10 processes ✓
- Stress Response: 8 processes ✓
- Cell Cycle: 6 processes ✓
- DNA/RNA: 5 processes ✓

**Major Gaps (need filling):**
- **Metabolism:** Only 3-4 processes (need 10-12)
- **Biosynthesis:** Very limited (need 6-8)
- **Mating/Meiosis:** Only 3 (could add 2-3 more)
- **Organelle biogenesis:** Limited mitochondria, need peroxisomes, vacuole
- **Cell wall/membrane:** Only 2 processes

---

## Recommended Additions

### 4 E. coli Processes to Add (to reach 70)

#### High Priority (Classic Systems):

1. **E. coli Fatty Acid Synthesis (FAS-II)**
   - **Why:** Complete the lipid metabolism coverage
   - **Logic Gates:** Multiple regulation points (FabR repressor, feedback inhibition)
   - **Category:** Metabolism
   - **Complexity:** Detailed (~70 nodes)

2. **E. coli Nucleotide Salvage Pathways**
   - **Why:** Complement de novo synthesis, shows recycling logic
   - **Logic Gates:** Multiple substrate alternatives (OR gates)
   - **Category:** Metabolism
   - **Complexity:** Moderate (~50 nodes)

3. **E. coli Cell Division (Min System)**
   - **Why:** Classic spatial regulation, oscillatory dynamics
   - **Logic Gates:** Spatial logic gates, mutual inhibition
   - **Category:** Cell Division
   - **Complexity:** Detailed (~65 nodes)

4. **E. coli Tryptophan Degradation (Kynurenine Pathway)**
   - **Why:** Complements trp synthesis, shows catabolism
   - **Logic Gates:** Conditional degradation, oxygen-dependent
   - **Category:** Metabolism
   - **Complexity:** Moderate (~45 nodes)

---

### 32 Yeast Processes to Add (to reach 70)

#### METABOLISM (12 processes needed)

**Glycolysis & Fermentation:**
1. **Yeast Gluconeogenesis**
   - Reverse of glycolysis, shows metabolic flexibility
   - High OR gates (alternative carbon sources)

2. **Yeast Pentose Phosphate Pathway**
   - NADPH production, nucleotide synthesis
   - Oxidative vs non-oxidative branch (OR logic)

**TCA Cycle & Respiration:**
3. **Yeast TCA Cycle (Krebs Cycle)**
   - Central carbon metabolism
   - Multiple entry/exit points (OR gates)

4. **Yeast Glyoxylate Cycle**
   - Alternative to TCA during acetate growth
   - NOT gates (TCA repressed conditions)

**Lipid Metabolism:**
5. **Yeast Fatty Acid Synthesis**
   - De novo lipogenesis
   - Acetyl-CoA carboxylase regulation (AND gates)

6. **Yeast Fatty Acid β-Oxidation**
   - Peroxisomal pathway
   - Oleate induction, glucose repression

7. **Yeast Sterol Biosynthesis (Ergosterol)**
   - Membrane fluidity regulation
   - Oxygen-dependent steps, heme regulation

8. **Yeast Sphingolipid Metabolism**
   - Signaling molecules, stress response
   - Quality control checkpoints

**Amino Acid Metabolism:**
9. **Yeast Amino Acid Biosynthesis (General)**
   - Focus on branched-chain amino acids
   - Gcn4 regulation, multiple feedback loops

10. **Yeast Amino Acid Catabolism**
    - Nitrogen source utilization
    - Retrograde signaling to nucleus

**Carbohydrate Metabolism:**
11. **Yeast Galactose Metabolism (Beyond GAL Regulation)**
    - Leloir pathway details
    - Gal1, Gal7, Gal10 enzyme cascade

12. **Yeast Trehalose Metabolism**
    - Stress protection, storage carbohydrate
    - Synthesis vs degradation balance

---

#### BIOSYNTHESIS (8 processes needed)

**Nucleotides:**
13. **Yeast Purine Biosynthesis (De Novo)**
    - IMP synthesis pathway
    - PRPP regulation, feedback control

14. **Yeast Pyrimidine Biosynthesis (De Novo)**
    - UTP synthesis
    - CAD complex, aspartate transcarbamoylase

15. **Yeast Nucleotide Salvage**
    - Recycling pathways
    - Hypoxanthine, guanine salvage

**Cofactors:**
16. **Yeast Heme Biosynthesis**
    - Oxygen-sensing regulation
    - Mitochondrial-cytoplasmic coordination

17. **Yeast NAD+ Biosynthesis**
    - De novo and salvage
    - Sirtuins, calorie restriction link

18. **Yeast Thiamine (Vitamin B1) Biosynthesis**
    - Complex multi-step pathway
    - THI regulation

**Other:**
19. **Yeast Aromatic Amino Acid Biosynthesis**
    - Shikimate pathway
    - Phe, Tyr, Trp synthesis

20. **Yeast Cell Wall Biosynthesis (Detailed)**
    - β-glucan, chitin, mannoprotein synthesis
    - Multiple regulation layers

---

#### MATING & DEVELOPMENT (4 processes needed)

21. **Yeast Pseudohyphal Growth**
    - Nutrient limitation response
    - Filamentous growth, cell adhesion

22. **Yeast Sporulation (Meiotic Differentiation)**
    - Beyond meiosis regulation
    - Spore wall assembly, maturation

23. **Yeast Flocculation**
    - Cell-cell adhesion
    - FLO gene regulation

24. **Yeast Invasive Growth**
    - Agar invasion, substrate penetration
    - Related to pathogenic fungi

---

#### ORGANELLE BIOGENESIS (4 processes needed)

25. **Yeast Peroxisome Biogenesis**
    - Pex protein import
    - Proliferation vs degradation

26. **Yeast Vacuole Fusion/Fission**
    - Homotypic fusion
    - Rab GTPases, SNARE complexes

27. **Yeast Endosome Maturation**
    - Early to late endosome transition
    - ESCRT complexes

28. **Yeast Golgi Organization**
    - Cisternal maturation model
    - Retrograde transport

---

#### CELL CYCLE & DIVISION (2 processes needed)

29. **Yeast Cytokinesis (Detailed)**
    - Actomyosin ring contraction
    - Septum formation, cell separation

30. **Yeast Spindle Assembly Checkpoint (SAC)**
    - Metaphase arrest
    - Mad/Bub proteins, APC/C inhibition

---

#### STRESS RESPONSE & QUALITY CONTROL (2 processes needed)

31. **Yeast Replicative Aging**
    - Asymmetric damage segregation
    - ERCs, oxidative damage, sirtuins

32. **Yeast Chronological Aging**
    - Stationary phase survival
    - Calorie restriction, TOR pathway

---

## Priority Ranking

### Tier 1: MUST HAVE (16 processes)
Essential for comprehensive coverage and organism balance:

**Metabolism (8):**
1. Yeast TCA Cycle
2. Yeast Gluconeogenesis  
3. Yeast Pentose Phosphate Pathway
4. Yeast Fatty Acid Synthesis
5. Yeast Fatty Acid β-Oxidation
6. Yeast Sterol Biosynthesis
7. Yeast Amino Acid Biosynthesis
8. Yeast Trehalose Metabolism

**Biosynthesis (4):**
9. Yeast Purine Biosynthesis
10. Yeast Pyrimidine Biosynthesis
11. Yeast Heme Biosynthesis
12. Yeast NAD+ Biosynthesis

**E. coli (4):**
13. E. coli Fatty Acid Synthesis (FAS-II)
14. E. coli Nucleotide Salvage
15. E. coli Cell Division (Min System)
16. E. coli Tryptophan Degradation

### Tier 2: HIGHLY RECOMMENDED (12 processes)
Fill important gaps:

17. Yeast Glyoxylate Cycle
18. Yeast Sphingolipid Metabolism
19. Yeast Amino Acid Catabolism
20. Yeast Galactose Metabolism
21. Yeast Nucleotide Salvage
22. Yeast Thiamine Biosynthesis
23. Yeast Aromatic AA Biosynthesis
24. Yeast Cell Wall Biosynthesis
25. Yeast Peroxisome Biogenesis
26. Yeast Vacuole Fusion
27. Yeast Cytokinesis
28. Yeast SAC

### Tier 3: NICE TO HAVE (8 processes)
Round out coverage:

29. Yeast Pseudohyphal Growth
30. Yeast Sporulation Details
31. Yeast Flocculation
32. Yeast Invasive Growth
33. Yeast Endosome Maturation
34. Yeast Golgi Organization
35. Yeast Replicative Aging
36. Yeast Chronological Aging

---

## Implementation Timeline

**Phase 1 (Week 1): Tier 1 - Core Metabolism (8 yeast + 2 E. coli)**
- Focus: Essential metabolic pathways
- Time: ~20 hours (2 hours per process)
- Result: 108 → 118 processes

**Phase 2 (Week 2): Tier 1 - Biosynthesis (4 yeast + 2 E. coli)**
- Focus: Nucleotide and cofactor synthesis
- Time: ~12 hours
- Result: 118 → 124 processes

**Phase 3 (Week 3): Tier 2 - Gap Filling (12 yeast)**
- Focus: Complete coverage of major categories
- Time: ~24 hours
- Result: 124 → 136 processes

**Phase 4 (Week 4): Tier 3 - Final Push (4 yeast)**
- Focus: Specialty processes for comprehensive coverage
- Time: ~8 hours
- Result: 136 → 140 processes

**Total Time: ~64 hours (~4 weeks at 16 hours/week)**

---

## Automation Strategy

To speed up process creation:

1. **Use existing E. coli processes as templates**
   - Many metabolic pathways are conserved
   - Adapt logic structure, update gene/protein names

2. **Leverage LLM more effectively**
   - Create standardized prompts for each category
   - Use multi-shot examples from best existing processes

3. **Batch similar processes**
   - Do all amino acid biosynthesis together
   - Do all nucleotide pathways together
   - Reuse common regulatory motifs

4. **Quality control checklist**
   - Run syntax validator
   - Run color audit
   - Check logic gate counts
   - Verify citations

---

## Expected Statistics After Expansion

**Current (108 processes):**
- Architecture: 100:12:7:2
- Total nodes: 6,496
- OR gates: 636
- AND gates: 351  
- NOT gates: 127

**Projected (140 processes):**
- Architecture: 100:12:7:2 (should remain stable)
- Total nodes: ~8,430
- OR gates: ~825
- AND gates: ~455
- NOT gates: ~165
- E. coli vs Yeast comparison will be statistically powerful (n=70 each)

---

## Key Benefits of 70+70=140

1. **Perfect statistical balance** for organism comparisons
2. **Comprehensive coverage** of both organisms
3. **Strong validation** of 100:12:7:2 pattern
4. **Publication-ready** sample size
5. **Round number** (140 is 2×70, 4×35, divisible by many factors)
6. **Defensible against reviewers** - shows thoroughness

---

## Next Steps

**Immediate:**
1. ✅ Audit current processes for color errors (DONE - only minor legend issues)
2. ✅ Deploy fixes (DONE)
3. Choose which Tier 1 processes to start with
4. Create first batch (8 metabolic pathways)

**User Decision Needed:**
- Do you want to proceed with this plan?
- Should we start with Tier 1 processes?
- Any specific processes you want prioritized?
- Would you like templates/prompts for faster creation?

---

**End of Expansion Plan**

*This plan will give you a publication-ready dataset with perfect organism balance and comprehensive biological coverage.*

