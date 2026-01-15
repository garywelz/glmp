# 📋 FOR DESKTOP AGENT: 36 New Processes List

**From:** Cursor.com Background Agent  
**To:** Desktop Agent  
**Date:** October 15, 2025  
**Subject:** Proposed 36 new processes for GLMP expansion

---

## 🎯 OVERVIEW

User has approved expansion from 108→144 processes to achieve:
- **70 E. coli** (current: 66, add: 4)
- **70 Yeast** (current: 38, add: 32)

Background agent (cursor.com) will generate all 36 processes in 5 batches.

---

## 📋 COMPLETE LIST (Numbered 1-36)

### E. COLI (4 processes)

1. **Pentose Phosphate Pathway** - Metabolic, ~70 nodes, 5 OR, 4 AND, 1 NOT
2. **Iron Uptake & Fur Regulon** - Nutrient/Regulation, ~80 nodes, 6 OR, 3 AND, 3 NOT
3. **Fatty Acid Biosynthesis** - Metabolic, ~90 nodes, 4 OR, 5 AND, 2 NOT
4. **Oxidative Stress Response (OxyR/SoxRS)** - Stress, ~80 nodes, 7 OR, 3 AND, 2 NOT

### YEAST (32 processes)

#### Metabolic Pathways (8):
5. Pentose Phosphate Pathway
6. Fatty Acid Synthesis (Type I FAS)
7. Fatty Acid β-Oxidation
8. Sphingolipid Biosynthesis
9. Purine Biosynthesis (De Novo)
10. Pyrimidine Biosynthesis (De Novo)
11. One-Carbon Metabolism (Folate & Methionine)
12. TCA Cycle Regulation

#### Gene Regulation (6):
13. GAL Gene Regulation (Galactose)
14. PHO Gene Regulation (Phosphate)
15. Nitrogen Catabolite Repression (NCR)
16. General Amino Acid Control (GCN4)
17. Heat Shock Response (HSF1)
18. Unfolded Protein Response (UPR)

#### Cell Cycle & Division (5):
19. Spindle Assembly Checkpoint (SAC)
20. DNA Damage Checkpoint (Rad53/Mec1)
21. Cytokinesis and Septation
22. Bud Site Selection
23. Mitotic Exit Network (MEN)

#### DNA & Chromatin (5):
24. Chromatin Remodeling (SWI/SNF)
25. Histone Acetylation & Deacetylation
26. Telomere Maintenance & Length Regulation
27. Base Excision Repair (BER)
28. Meiotic Recombination

#### Protein Quality Control (4):
29. Ubiquitin-Proteasome System
30. Autophagy (Macro & Selective)
31. ER-Associated Degradation (ERAD)
32. Chaperone Network (Hsp70/Hsp90)

#### Secretion & Trafficking (3):
33. ER to Golgi Transport (COPII)
34. Endocytosis (Clathrin-Mediated)
35. Vacuolar Protein Sorting

#### Signal Transduction (1):
36. TOR Signaling Pathway

---

## 📊 EXPECTED FINAL STATS

- **Total Processes:** 144
- **E. coli:** 70
- **Yeast:** 70
- **Total Nodes:** ~9,500
- **Total Logic Gates:** ~370
- **OR:AND Ratio:** ~1.5:1 (validates paper's 100:12:7:2 architecture)

---

## 🔄 GENERATION TIMELINE

**Background agent will generate in 5 batches:**
- Batch 1: 8 processes (E. coli complete + Yeast metabolic start)
- Batch 2: 8 processes (Yeast metabolic + gene regulation)
- Batch 3: 7 processes (Gene regulation + cell cycle)
- Batch 4: 7 processes (DNA + protein QC)
- Batch 5: 6 processes (Protein QC + trafficking + signaling)

**Estimated timeline:** ~2 weeks (1-2 batches per day)

---

## ✅ QUALITY STANDARDS

All 36 processes will include:
- Valid Mermaid syntax
- Phase 2 color scheme (8 colors)
- Logic gates with correct shapes/colors
- 3-5 PubMed citations
- Complete metadata (gates, complexity, architecture)

---

## 📁 FILES FOR DESKTOP AGENT

**Reference documents:**
- `36_NEW_PROCESSES_LIST.md` - Detailed list with expected gates/nodes
- `PROPOSED_36_NEW_PROCESSES.md` - Full rationale and selection criteria
- `FUTURE_PROCESS_GENERATION_PLAN.md` - Original planning document

**All committed to GitHub on branch:**
`cursor/continue-frozen-deploy-glmp-conversation-0c90`

---

## 🚀 NEXT STEPS

1. **User will say "Go"** to background agent
2. **Background agent generates Batch 1** (8 processes)
3. **Desktop agent deploys** to GCS when batches complete
4. **Repeat** for remaining 4 batches

---

## 📞 COORDINATION

Background agent will:
- Generate JSON files with complete metadata
- Update metadata.json after each batch
- Commit to GitHub
- Notify when batch is ready for deployment

Desktop agent will:
- Pull from GitHub
- Deploy to GCS
- Verify deployment
- Confirm batch complete

---

**Status:** Awaiting user "Go" command  
**Ready:** All planning complete, selection finalized  
**Timeline:** ~2 weeks to complete all 36

---

**Background Agent:** Cursor.com (autonomous)  
**Desktop Agent:** Cursor desktop (user-initiated)  
**User:** Gary Welz
