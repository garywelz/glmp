# GLMP Logic Gate Rules & Standards

**Version:** 1.0  
**Date:** 2025-10-08  
**Status:** Official Standard for All Processes

---

## Core Principle

**Logic gates represent DECISIONS and CONDITIONAL BRANCHING, not parallel production or simultaneous processes.**

---

## Rule 1: Rectangles vs Diamonds

### RECTANGLES (Process Nodes)
**Use when:** A process produces multiple outputs **simultaneously** or **in parallel**

**Characteristics:**
- All outputs occur together
- No decision/choice involved
- Represents biological parallelism
- Multiple arrows = multiple products, not alternatives

**Color:** 🟢 Green (Processing & Operations)

**Examples:**
```
✅ CORRECT:
FF[Strong Transcription] --> II[lacZ mRNA Synthesis]
FF --> JJ[lacY mRNA Synthesis]
FF --> KK[lacA mRNA Synthesis]

Rationale: One transcription event produces ALL THREE mRNAs simultaneously.
This is PARALLEL PRODUCTION, not a decision.
```

```
✅ CORRECT:
OO[Beta-Galactosidase] --> RR[Lactose Hydrolysis]
                      --> UU[Allolactose Formation]

Rationale: The enzyme catalyzes both reactions in parallel.
```

---

### DIAMONDS (Decision Nodes / Logic Gates)

**Use when:** A decision point leads to **alternative** or **mutually exclusive** branches

**Characteristics:**
- Represents a conditional evaluation
- Branches are alternatives (this OR that)
- Only ONE path is taken based on condition
- Labels on branches (Yes/No, High/Low, etc.)

**Colors:**
- 🟠 Orange: OR gates (single condition, binary branches)
- 💜 Lavender: AND gates (multiple conditions required)

**Examples:**
```
✅ CORRECT:
M{Is Lactose Present?}
  -->|Yes| Q[Lac Repressor Inactive]
  -->|No| P[Lac Repressor Active]

Rationale: This is a DECISION. Only ONE path is taken.
```

```
✅ CORRECT:
ANDGATE1{Low Energy AND No Glucose?}
  -->|Yes| W[High cAMP Levels]
  -->|No| V[Low cAMP Levels]

Rationale: Evaluates TWO conditions, then branches to alternatives.
```

---

## Rule 2: OR Gates (Orange Diamonds 🟠)

### Definition
**Binary decision points** based on a **single condition** that leads to **alternative outcomes**.

### Characteristics:
- One input condition
- Two or more alternative outputs
- Mutually exclusive branches
- Yes/No, Present/Absent, High/Low labeling

### Color: `#ff9f43` (Orange)

### Pattern:
```
[Condition State] --> {Decision Question?}
                        -->|Yes| [Path A]
                        -->|No| [Path B]
```

### Examples from Lac Operon:
```
M{Is Lactose Present?}
N{Is Glucose Present?}
O{Is Energy Low?}
BB{Operator Free?}
CC{CAP Bound?}
```

---

## Rule 3: AND Gates (Lavender Diamonds 💜)

### Definition
**Multi-condition decision points** that require **multiple conditions to be satisfied simultaneously** before branching.

### Characteristics:
- Multiple input conditions (2 or more)
- All conditions must be met for "Yes" path
- Represents biological signal integration
- Convergence point for multiple regulatory signals

### Color: `#c3a6ff` (Lavender)

### Pattern:
```
[Condition A] --> {Condition A AND Condition B?}
[Condition B] -->
                  -->|Yes| [Both conditions met]
                  -->|No| [One or both conditions not met]
```

### Examples from Lac Operon:
```
ANDGATE1{Low Energy AND No Glucose?}
  Inputs: O{Is Energy Low?} --Yes-->
          N{Is Glucose Present?} --No-->
  Outputs: Yes → W[High cAMP Levels]
           No → V[Low cAMP Levels]

ANDGATE2{Operator Free AND CAP Bound?}
  Inputs: U[Operator Free]
          Z[CAP Binds Promoter]
  Outputs: Yes → FF[Strong Transcription]
           No → GG[Weak/No Transcription]
```

---

## Rule 4: AND-then-OR Compound Logic

### Question Addressed:
**When an AND gate has Yes/No branches, does this represent compound AND-then-OR logic?**

### DECISION: **Keep as-is (implicit OR is acceptable)**

### Rationale:
1. **Natural biological logic:** AND evaluation naturally produces a binary result (true/false)
2. **Visual clarity:** Separating into AND → intermediate → OR adds unnecessary nodes
3. **Standard interpretation:** Yes/No branches from an AND gate are understood as:
   - "Yes" = All conditions met → proceed to outcome A
   - "No" = One or more conditions not met → proceed to outcome B

### Pattern (ACCEPTED):
```
✅ ACCEPTABLE:
ANDGATE{Condition A AND Condition B?}
  -->|Yes| [Outcome when both conditions met]
  -->|No| [Outcome when conditions not met]
```

### Pattern (NOT REQUIRED):
```
❌ NOT NECESSARY (too verbose):
ANDGATE{Condition A AND Condition B?} --> RESULT[Evaluation Result]
RESULT --> ORGATE{Result?}
  -->|Yes| [Outcome A]
  -->|No| [Outcome B]
```

### Key Point:
**The Yes/No branching from an AND gate is implicit OR logic, and that's acceptable.**
- It represents the natural binary outcome of the AND evaluation
- Separating it adds complexity without educational benefit
- The lavender color makes it clear this is an AND gate
- The Yes/No labels make the branching clear

---

## Rule 5: Parallel Production vs Decision Branching

### PARALLEL PRODUCTION (Rectangles)
**When to use:**
- One process → multiple simultaneous products
- All outputs occur together
- No decision/choice involved

**Examples:**
```
✅ Transcription → multiple mRNAs (all produced together)
✅ Enzyme → multiple products (parallel reactions)
✅ Signal → multiple downstream pathways (all activated)
```

### DECISION BRANCHING (Diamonds)
**When to use:**
- Conditional evaluation → alternative paths
- Only ONE path taken
- Mutually exclusive outcomes

**Examples:**
```
✅ Is condition met? → Yes path OR No path (one or the other)
✅ Signal present? → Activate pathway A OR pathway B
✅ Resource available? → Use resource OR alternative pathway
```

---

## Rule 6: When Rectangles Can Have Multiple Outputs

### ALLOWED:
✅ **Parallel production** (all outputs simultaneous)
```
[Transcription] → [mRNA1], [mRNA2], [mRNA3]
[Enzyme] → [Product A], [Product B]
```

✅ **Broadcast signals** (signal activates multiple pathways)
```
[Signal Received] → [Pathway 1], [Pathway 2], [Pathway 3]
```

✅ **Complex formation** (one input, multiple components produced)
```
[Assembly Process] → [Component A], [Component B], [Component C]
```

### NOT ALLOWED:
❌ **Alternative outcomes** (use diamond instead)
```
BAD: [Condition] → [Option A], [Option B]
GOOD: {Condition?} →|Yes| [Option A]
                    →|No| [Option B]
```

---

## Rule 7: Node Type Decision Tree

**Use this decision tree to choose node type:**

```
Does the node represent a DECISION or CONDITIONAL EVALUATION?
├─ YES → Use DIAMOND
│   │
│   └─ Is it based on ONE condition?
│       ├─ YES → Use ORANGE diamond (OR gate)
│       └─ NO (multiple conditions) → Use LAVENDER diamond (AND gate)
│
└─ NO → Use RECTANGLE
    │
    └─ Does it produce multiple outputs?
        ├─ YES → Are they simultaneous/parallel?
        │   ├─ YES → Rectangle is correct (parallel production)
        │   └─ NO (alternatives) → Should be diamond, not rectangle
        │
        └─ NO → Rectangle with single output
```

---

## Summary Table

| Node Type | Shape | Color | Use Case | Multiple Outputs? |
|-----------|-------|-------|----------|-------------------|
| **Process** | Rectangle | 🟢 Green | Actions, transformations, parallel production | Yes (if simultaneous) |
| **OR Gate** | Diamond | 🟠 Orange | Single condition → binary decision | Yes (alternatives) |
| **AND Gate** | Diamond | 💜 Lavender | Multiple conditions → binary decision | Yes (alternatives) |
| **State** | Rectangle | 🔵 Blue | Conditions, intermediate states | Rarely |
| **Trigger** | Rectangle | 🔴 Red | External inputs | Usually no |
| **Structure** | Rectangle | 🟡 Yellow | Proteins, enzymes, complexes | Usually no |
| **Output** | Rectangle | 🟣 Violet | Final products, outcomes | Usually no |

---

## Examples from Lac Operon

### ✅ CORRECT Examples:

**1. Parallel Production (Rectangle):**
```
FF[Strong Transcription] --> II[lacZ mRNA Synthesis]
                        --> JJ[lacY mRNA Synthesis]
                        --> KK[lacA mRNA Synthesis]
```
✓ One transcription event produces all three mRNAs simultaneously

**2. OR Gate (Orange Diamond):**
```
M{Is Lactose Present?} -->|Yes| Q[Lac Repressor Inactive]
                      -->|No| P[Lac Repressor Active]
```
✓ Single condition, two alternative outcomes

**3. AND Gate (Lavender Diamond):**
```
ANDGATE1{Low Energy AND No Glucose?} -->|Yes| W[High cAMP Levels]
                                     -->|No| V[Low cAMP Levels]
```
✓ Multiple conditions evaluated, then binary outcome

**4. AND Gate with Yes/No Branching (Acceptable):**
```
ANDGATE2{Operator Free AND CAP Bound?} -->|Yes| FF[Strong Transcription]
                                       -->|No| GG[Weak/No Transcription]
```
✓ AND evaluation naturally produces binary result (implicit OR)

---

## Application to Collection

### All 4 processes must follow these rules:

1. **ecoli_lac_operon.json** ✅ Already compliant
2. **ecoli_dna_replication_initiation.json** - Needs review
3. **ecoli_transcription_regulation.json** - Needs review
4. **yeast_cell_cycle_control.json** - Needs review

### Upgrade Process:
1. Review each process for logic gates
2. Identify all decision points
3. Classify as OR (orange) or AND (lavender)
4. Verify rectangles with multiple outputs are parallel production
5. Apply consistent colors and labels

---

## Validation Checklist

For each process, verify:

- [ ] All decision points use diamonds
- [ ] Single-condition decisions use orange diamonds
- [ ] Multi-condition decisions use lavender diamonds
- [ ] Rectangles with multiple outputs are parallel production
- [ ] All logic gates have clear Yes/No or condition labels
- [ ] Colors match the 7-color scheme
- [ ] Node IDs are unique (A-ZZZ pattern)

---

## Future Considerations

### Potential Advanced Patterns:
- **XOR gates** (exclusive OR: exactly one condition)
- **NAND/NOR gates** (negated logic)
- **Threshold gates** (requires N of M conditions)

**Decision:** Not needed yet. Start with OR and AND gates only.

---

## Version History

- **v1.0 (2025-10-08):** Initial rules established
  - OR gates (orange) for single-condition decisions
  - AND gates (lavender) for multi-condition decisions
  - Rectangles allowed for parallel production
  - AND-then-OR kept as implicit (no separation required)

---

**Status:** ✅ APPROVED - Ready to apply to all processes
