# Deployment Instructions - Version 3 (9 Processes)

## ✅ What's Ready to Deploy

### **NEW - 5 E. coli Regulation & Signaling Processes:**

1. **Two-Component Signaling (EnvZ-OmpR)** - 35 nodes, 3 logic gates
2. **SOS Response to DNA Damage** - 42 nodes, 4 logic gates  
3. **Heat Shock Response (σ32)** - 38 nodes, 4 logic gates
4. **Catabolite Repression (cAMP-CRP)** - 33 nodes, 4 logic gates
5. **Stringent Response (ppGpp)** - 40 nodes, 4 logic gates

### **FIXED - Yeast Cell Cycle:**
- StartCheck diamond now **ORANGE** (OR gate), not lavender

### **Total Collection:**
- **9 processes** (8 E. coli, 1 yeast)
- **7 categories**
- **38 citations**
- **All verified**

---

## 🚀 Deploy Commands

```bash
cd ~/glmp-clean/glmp-v2
git pull origin main
./DEPLOY_TO_GCS.sh
```

---

## 🔍 Verification URLs

### **Main Viewer:**
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html

### **Updated Process:**
- **Yeast Cell Cycle** (StartCheck now orange):
  https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=yeast_cell_cycle_control

### **NEW Processes:**

1. **Two-Component Signaling:**
   https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_two_component_signaling

2. **SOS Response:**
   https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_sos_response

3. **Heat Shock:**
   https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_heat_shock_response

4. **Catabolite Repression:**
   https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_catabolite_repression

5. **Stringent Response:**
   https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_stringent_response

---

## ✓ Expected Results

### **Yeast Cell Cycle:**
- ✅ 3 **ORANGE** diamonds (StartCheck, SCheckpoint, SpindleCheck)
- ✅ No lavender diamonds
- ✅ All phase rectangles blue

### **New Processes - Color Coding:**
- 🔴 Red: Environmental triggers (heat, DNA damage, starvation, osmotic stress)
- 🟡 Yellow: Proteins (sigma factors, chaperones, regulators, kinases)
- 🟢 Green: Operations (transcription, repair, signaling, synthesis)
- 🔵 Blue: Intermediates (mRNA, modified proteins, signaling molecules)
- 🟠 Orange: OR logic gates (binary decisions)
- 🟣 Lavender: AND logic gates (multi-input convergence)
- 🟣 Violet: Final outputs (survival, adaptation, metabolic shifts)

### **Logic Gate Distribution:**

| Process | OR Gates | AND Gates | Total |
|---------|----------|-----------|-------|
| Lac Operon | 5 | 2 | 7 |
| DNA Replication | 1 | 0 | 1 |
| Transcription | 2 | 0 | 2 |
| Yeast Cell Cycle | 3 | 0 | 3 |
| Two-Component | 2 | 1 | 3 |
| SOS Response | 3 | 1 | 4 |
| Heat Shock | 2 | 2 | 4 |
| Catabolite Repression | 2 | 2 | 4 |
| Stringent Response | 2 | 2 | 4 |
| **TOTAL** | **22** | **10** | **32** |

---

## 🎨 Lavender Color Verification

**Lavender hex:** `#b4b4dc` (blue-gray, distinct from violet)  
**Violet hex:** `#b197fc` (purple)

**Processes with lavender AND gates:**
1. Lac Operon (2)
2. Two-Component Signaling (1)
3. SOS Response (1)
4. Heat Shock (2)
5. Catabolite Repression (2)
6. Stringent Response (2)

---

## 🔧 Troubleshooting

### If browser shows old version:
```bash
# Hard refresh
Ctrl+Shift+R (Windows/Linux)
Cmd+Shift+R (Mac)

# Or use cache-busting URL
?v=3&t=1696800000
```

### If Yeast StartCheck still shows lavender:
```bash
# Verify deployed file
gsutil cat gs://regal-scholar-453620-r7-podcast-storage/glmp-v2/processes/yeast/yeast_cell_cycle_control.json | grep "StartCheck fill"

# Should show: style StartCheck fill:#ff9f43
```

---

## 📊 Collection Summary

**9 Processes:**
- Gene Regulation: 1
- DNA Replication: 1
- Gene Expression: 1
- Cell Cycle: 1
- Signal Transduction: 1
- Stress Response: 3
- Metabolic Regulation: 1

**Total Nodes:** 303 (across all 9 processes)  
**Total Logic Gates:** 32  
**Total Citations:** 38  
**Organisms:** E. coli (8), S. cerevisiae (1)

---

**Deploy date:** 2025-10-08  
**Commit:** Latest on `main` branch  
**Status:** Ready for production
