# Phase 2 Implementation Guide: Semantic Node Recoloring

**Problem:** Phase 1 only updated logic gates and products. Most semantic nodes (triggers, enzymes, processing, intermediates) are unstyled or have old colors.

**Solution:** Complete Phase 2 semantic recoloring for all ~5,000 nodes across 108 processes.

---

## 🎯 Target Color Scheme

| Category      | Current Color | New Color  | Hex       |
|---------------|---------------|------------|-----------|
| Triggers      | Red #ff6b6b   | **Green**  | #51cf66   |
| Enzymes       | Yellow #ffd43b| **Amber**  | #fab005   |
| Processing    | Green #51cf66 | **Sky Blue** | #74c0fc |
| Intermediates | Blue #74c0fc  | **Salmon** | #ffa07a   |
| OR Gates      | Orange #ff9f43| Orange     | #ff9f43   |
| AND Gates     | Purple #7950f2| Purple     | #7950f2   |
| NOT Gates     | Red #e74c3c   | Red        | #e74c3c   |
| Products      | Black #000000 | Black      | #000000   |

---

## ⚠️ Why Phase 2 Is Complex

**Cannot use simple find-replace** because:
1. **Cascading errors:** If you replace all green (#51cf66) nodes, you'll change BOTH:
   - Old "processing" nodes (should become sky blue)
   - New "trigger" nodes (should stay green)
   
2. **Semantic ambiguity:** Each node must be analyzed for its biological function:
   - Is "Glucose Transport" a trigger (green) or processing (sky blue)?
   - Is "ATP" an intermediate (salmon) or energy currency (keep as-is)?
   
3. **5,000+ nodes:** Manual review of each node is impractical

---

## 💡 Recommended Approaches

### Option 1: Node-by-Node Analysis (Most Accurate)
For each process:
1. Read the mermaid code
2. For each node, determine semantic category:
   - **Trigger:** External signal, environmental condition, cell state
   - **Enzyme:** Protein that catalyzes reactions
   - **Processing:** Biochemical operation, transformation
   - **Intermediate:** Metabolite, signaling molecule, temporary state
3. Update style statement with correct color
4. Verify no nodes are left unstyled

**Pros:** Most accurate  
**Cons:** Very time-consuming (hours of work)

### Option 2: AI-Assisted Classification (Recommended)
Use an AI agent to analyze node text and classify:

```python
def classify_node_semantic_type(node_id, node_text, context):
    """
    Classify node by biological function
    
    Returns: 'trigger', 'enzyme', 'processing', 'intermediate', or 'gate'
    """
    
    # Keywords for triggers
    if any(kw in node_text.lower() for kw in [
        'signal', 'stress', 'starvation', 'glucose present', 
        'temperature', 'ph', 'nutrient', 'growth'
    ]):
        return 'trigger'
    
    # Keywords for enzymes (protein names)
    if any(kw in node_text for kw in [
        'ase', 'synthase', 'kinase', 'ligase', 'dehydrogenase',
        'transferase', 'isomerase', 'lyase'
    ]):
        return 'enzyme'
    
    # Keywords for processing
    if any(kw in node_text.lower() for kw in [
        'phosphorylation', 'transcription', 'translation',
        'oxidation', 'reduction', 'binding', 'cleavage'
    ]):
        return 'processing'
    
    # Default to intermediate
    return 'intermediate'
```

**Pros:** Semi-automated, reasonably accurate  
**Cons:** Requires verification of edge cases

### Option 3: Hybrid Approach (Best Balance)
1. Use AI to classify 90% of nodes
2. Manually review ambiguous cases
3. Verify a sample of each category
4. Run full update

---

## 🔧 Implementation Steps

### Step 1: Style All Unstyled Nodes First

Before recoloring, ensure ALL nodes have style statements:

```python
import json
import re
from pathlib import Path

def ensure_all_nodes_styled(json_path):
    """Add default styles to any unstyled nodes"""
    
    data = json.load(open(json_path))
    mermaid = data['mermaid']
    
    # Find all node IDs
    all_nodes = set(re.findall(r'(\w+)[\[\{\(]', mermaid))
    
    # Find styled nodes
    styled_nodes = set(re.findall(r'style (\w+) fill:', mermaid))
    
    # Unstyled nodes
    unstyled = all_nodes - styled_nodes
    
    if unstyled:
        print(f"{json_path.stem}: {len(unstyled)} unstyled nodes")
        
        # Add default style (use intermediate color for now)
        for node_id in sorted(unstyled):
            node_text = get_node_text(node_id, mermaid)
            
            # Classify and add appropriate color
            category = classify_node_semantic_type(node_id, node_text, mermaid)
            color = COLORS[category]
            
            # Add style statement
            mermaid += f"\n    style {node_id} fill:{color['fill']},color:{color['text']}"
        
        data['mermaid'] = mermaid
        json.dump(data, open(json_path, 'w'), indent=2, ensure_ascii=False)
        
        return len(unstyled)
    
    return 0
```

### Step 2: Reclassify Existing Styled Nodes

For nodes that already have styles, update to new colors:

```python
def reclassify_styled_nodes(json_path):
    """Update existing styled nodes to new color scheme"""
    
    data = json.load(open(json_path))
    mermaid = data['mermaid']
    
    # Find all style statements (except gates/products)
    pattern = r'style (\w+) fill:#([0-9a-fA-F]+)'
    
    changes = []
    for match in re.finditer(pattern, mermaid):
        node_id = match.group(1)
        current_color = match.group(2)
        
        # Skip gates and products (already correct)
        if current_color in ['ff9f43', '7950f2', 'e74c3c', '000000']:
            continue
        
        # Get node text and classify
        node_text = get_node_text(node_id, mermaid)
        category = classify_node_semantic_type(node_id, node_text, mermaid)
        new_color = COLORS[category]
        
        # Update style
        old_style = f'style {node_id} fill:#{current_color}'
        new_style = f'style {node_id} fill:{new_color["fill"]}'
        mermaid = mermaid.replace(old_style, new_style, 1)
        
        changes.append(f'{node_id}: {OLD_COLORS[current_color]} → {category}')
    
    if changes:
        data['mermaid'] = mermaid
        json.dump(data, open(json_path, 'w'), indent=2, ensure_ascii=False)
    
    return changes
```

### Step 3: Update Color Legends

Update the `colorScheme` field in each JSON:

```python
NEW_COLOR_SCHEME = {
    "green": {
        "hex": "#51cf66",
        "category": "Triggers & Environmental Signals",
        "description": "External signals, stress conditions, nutrient availability"
    },
    "amber": {
        "hex": "#fab005",
        "category": "Enzymes & Catalysts",
        "description": "Protein enzymes, regulatory complexes, molecular machines"
    },
    "skyblue": {
        "hex": "#74c0fc",
        "category": "Processing & Operations",
        "description": "Biochemical reactions, signal transduction, molecular transformations"
    },
    "salmon": {
        "hex": "#ffa07a",
        "category": "Intermediates & Metabolites",
        "description": "Chemical intermediates, signaling molecules, transient states"
    },
    "orange": {
        "hex": "#ff9f43",
        "category": "OR Logic Gates",
        "description": "Decision points with multiple alternative branches"
    },
    "purple": {
        "hex": "#7950f2",
        "category": "AND Logic Gates",
        "description": "Multi-signal integration requiring all conditions"
    },
    "red": {
        "hex": "#e74c3c",
        "category": "NOT Gates & Repression",
        "description": "Inhibition, blocking, inactivation, repression mechanisms"
    },
    "black": {
        "hex": "#000000",
        "category": "Products & Outcomes",
        "description": "Final products, cellular outcomes, system states"
    }
}

def update_color_scheme(json_path):
    data = json.load(open(json_path))
    data['colorScheme'] = NEW_COLOR_SCHEME
    json.dump(data, open(json_path, 'w'), indent=2, ensure_ascii=False)
```

---

## 🧪 Testing Strategy

### Test on Sample Processes First

1. **Lac Operon** (has all gate types)
2. **Amino Acid Biosynthesis** (many unstyled nodes)
3. **Glycolysis** (mostly styled, good baseline)

### Verification Checklist

For each test process:
- [ ] All nodes have style statements (no lavender defaults)
- [ ] Triggers are green
- [ ] Enzymes are amber/gold
- [ ] Processing is sky blue
- [ ] Intermediates are salmon
- [ ] Logic gates unchanged (orange, purple, red)
- [ ] Products are black
- [ ] Color legend updated
- [ ] Renders correctly in viewer

---

## 📊 Expected Results

After Phase 2:
- **100% of nodes styled** (no lavender defaults)
- **Semantic clarity improved** (colors match biological function)
- **Color legend accurate** (reflects new scheme)
- **Triggers stand out** (green = "go" signal intuitive)
- **Gates visually distinct** (shape + color redundancy)

---

## ⏱️ Time Estimate

- **Option 1 (Manual):** 8-12 hours
- **Option 2 (AI-assisted):** 2-4 hours + 1-2 hours verification
- **Option 3 (Hybrid):** 3-5 hours total

---

## 🚨 Pitfalls to Avoid

1. **Don't use global find-replace** - will cause cascading errors
2. **Classify nodes semantically, not by current color** - old colors are inconsistent
3. **Test incrementally** - don't update all 108 processes at once
4. **Preserve logic gate styles** - don't accidentally change gates
5. **Check for unstyled nodes** - they'll default to lavender

---

## 💡 Quick Fix for User (Temporary)

If you want a quick improvement while working on full Phase 2:

### Fix 1: Style All Unstyled Nodes as Intermediates

```python
# For amino acid biosynthesis: add 59 missing styles
for node_id in unstyled_nodes:
    mermaid += f"\n    style {node_id} fill:#ffa07a,color:#000"  # Salmon
```

This eliminates lavender defaults immediately.

### Fix 2: Update Color Legend

Update JSON `colorScheme` to reflect current state (not ideal state):

```json
"colorScheme": {
  "note": "Phase 1 complete (gates + products). Phase 2 in progress (semantic recoloring)."
}
```

---

## 📋 Summary for Desktop Agent

**Phase 2 Tasks:**
1. ✅ Classify all 5,000+ nodes by semantic type
2. ✅ Add style statements to unstyled nodes
3. ✅ Update existing styles to new colors
4. ✅ Update color legends in all JSON files
5. ✅ Test on sample processes
6. ✅ Deploy full update

**Priority:**
- **High:** Fix unstyled nodes (eliminate lavender defaults)
- **Medium:** Reclassify existing nodes (new colors)
- **Low:** Update color legends (documentation)

**Estimated Effort:** 3-5 hours with AI assistance

---

*This guide prepared by background agent for desktop agent*  
*Date: 2025-10-20*
