# Color Scheme Update - Logic Gates

## Expanded 7-Color Programming Framework

### Previous 5-Color Scheme:
1. 🔴 Red (#ff6b6b) - Triggers & Inputs
2. 🟡 Yellow (#ffd43b) - Structures & Objects
3. 🟢 Green (#51cf66) - Processing & Operations
4. 🔵 Blue (#74c0fc) - Intermediates & States
5. 🟣 Violet (#b197fc) - Products & Outputs

### NEW 7-Color Scheme:
1. 🔴 Red (#ff6b6b) - Triggers & Inputs
2. 🟡 Yellow (#ffd43b) - Structures & Objects  
3. 🟢 Green (#51cf66) - Processing & Operations
4. 🔵 Blue (#74c0fc) - Intermediates & States
5. 🟠 **Orange (#ff9f43) - OR Logic Gates** ⭐ NEW
6. 💜 **Lavender (#c3a6ff) - AND Logic Gates** ⭐ NEW
7. 🟣 Violet (#b197fc) - Products & Outputs

---

## Rationale

**Problem:** Diamond-shaped decision nodes were classified as "outputs" (violet), but they're actually logic gates.

**Solution:** Dedicated colors for logic operations:
- **OR gates** = Orange (one path OR another)
- **AND gates** = Lavender (requires multiple conditions)

---

## Lac Operon Analysis

### Current Diamond Nodes:
- M: `{Is Lactose Present?}` - **OR gate** → Orange
- N: `{Is Glucose Present?}` - **OR gate** → Orange
- O: `{Is Energy Low?}` - **OR gate** → Orange
- BB: `{Operator Free?}` - **OR gate** → Orange
- CC: `{CAP Bound?}` - **OR gate** (could be AND) → Orange

### Total Logic Gates:
- **OR gates: 5** (M, N, O, BB, CC)
- **AND gates: 0 explicit** (some implicit convergence)

### Nodes to Keep Violet (Actual Outputs):
- EE: `[Transcription Blocked]` - Result/outcome
- GG: `[Weak Transcription]` - Result/outcome

---

## Implementation Plan

1. ✅ Add orange and lavender to colorScheme
2. ✅ Update Mermaid styling for M, N, O, BB, CC → orange
3. ✅ Keep EE, GG as violet (they're results, not gates)
4. ✅ Update color legend to show 7 colors
5. ✅ Update viewer.js to handle 7 colors
6. ✅ Redeploy

---

## Color Hex Values

```json
"orange": {
  "hex": "#ff9f43",
  "category": "OR Logic Gates",
  "description": "Decision points with binary branches (yes/no, true/false)"
},
"lavender": {
  "hex": "#c3a6ff", 
  "category": "AND Logic Gates",
  "description": "Decision points requiring multiple conditions to be satisfied"
}
```

---

## Benefits

1. **Quantifiable Logic** - Easy to count OR and AND gates
2. **Visual Clarity** - Logic operations distinct from outputs
3. **Programming Analogy** - Matches if/else (OR) and && (AND) in code
4. **Scientific Accuracy** - Properly represents regulatory logic

---

## Next Steps

Update all 4 processes with new color scheme for consistency.
