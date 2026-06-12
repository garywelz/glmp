# Cursor Handoff — GLMP GitHub Repository Tasks
**Date:** June 2026
**Repository:** https://github.com/garywelz/glmp
**Working directory:** `collaborations/krampis-virtual-cell/`

---

## Context

This handoff covers a set of file operations needed to prepare the GLMP GitHub repository for sharing with collaborator Prof. Konstantinos Krampis (Hunter College / CUNY) ahead of a working call on Thursday June 19, 2026. The tasks are:

1. Rename five existing working paper files to a consistent naming convention
2. Add two new files (collaboration plan and updated README)
3. Verify the result looks correct before the Tuesday document send

No code changes. No changes to any other part of the repository. All work is confined to `collaborations/krampis-virtual-cell/`.

---

## Task 1 — Rename existing working paper files

The current filenames are long descriptive slugs that don't match the paper labels used on the GCS public site or in the collaboration plan document. Rename them to the short convention below using `git mv` so Git tracks the renames (not delete + add).

**Run from the repository root:**

```bash
cd collaborations/krampis-virtual-cell

git mv primitive-relations-genomic-computational-class.md paper-I-foundational-typology.md
git mv genome-as-computer.md paper-II-genome-as-computer.md
git mv circuit-class-predicts-virtual-cell-model-accuracy.md paper-III-empirical-sequel.md
git mv glmp-genomic-complexity-synthesis.md synthesis-biorxiv.md
git mv mermaid-flowcharts-smarter-perturbation-design.md methods-mermaid-perturbation-design.md
```

**Verify the renames:**
```bash
ls -la
```

Expected files after rename:
- `paper-I-foundational-typology.md`
- `paper-II-genome-as-computer.md`
- `paper-III-empirical-sequel.md`
- `synthesis-biorxiv.md`
- `methods-mermaid-perturbation-design.md`
- `teaching-deck-krampis-biochemical-process-modeling.md` *(unchanged)*
- `.gitkeep` *(unchanged)*

**Do NOT rename** `teaching-deck-krampis-biochemical-process-modeling.md` — it doesn't have a GCS counterpart and its current name is fine.

---

## Task 2 — Add two new files

Two new files were generated in this session and need to be added to the same directory. They are in your outputs folder from this Claude session.

**File 1: Updated README**
- Source: `GLMP_Krampis_Plan` outputs — the file named `README.md`
- Destination: `collaborations/krampis-virtual-cell/README.md`
- Action: **Replace** the existing README.md with this new version

```bash
# From repo root, assuming you've copied the file here:
cp /path/to/new/README.md collaborations/krampis-virtual-cell/README.md
```

The new README includes:
- Big Picture Goal framing
- Updated Contents table using the new filenames from Task 1
- Krampis fork/pull-request workflow instructions
- Draft status guidance
- Note that methods paper is under active revision

**File 2: Collaboration plan**
- Source: outputs file named `GLMP_Krampis_Plan.md`
- Destination: `collaborations/krampis-virtual-cell/glmp-collaboration-plan-2026.md`
- Action: **New file** — does not exist in the repo yet

```bash
cp /path/to/GLMP_Krampis_Plan.md collaborations/krampis-virtual-cell/glmp-collaboration-plan-2026.md
```

---

## Task 3 — Commit and push everything

```bash
cd collaborations/krampis-virtual-cell

git add -A
git status
```

Review the status output. You should see:
- 5 renames (old filename → new filename)
- 1 modified file (README.md)
- 1 new file (glmp-collaboration-plan-2026.md)

Nothing else should appear in the diff. If anything unexpected shows up, stop and check before committing.

```bash
git commit -m "Rename working papers to match GCS labels; add collaboration plan and updated README

- primitive-relations... → paper-I-foundational-typology.md
- genome-as-computer → paper-II-genome-as-computer.md
- circuit-class-predicts... → paper-III-empirical-sequel.md
- glmp-genomic-complexity-synthesis → synthesis-biorxiv.md
- mermaid-flowcharts... → methods-mermaid-perturbation-design.md
- Add glmp-collaboration-plan-2026.md
- Update README with new filenames, Big Picture Goal, and Krampis workflow"

git push
```

---

## Task 4 — Verify on GitHub

After pushing, open the repository in your browser:
https://github.com/garywelz/glmp/tree/main/collaborations/krampis-virtual-cell

Confirm:
- [ ] Five papers appear with new short filenames
- [ ] `glmp-collaboration-plan-2026.md` appears
- [ ] README renders correctly at the bottom of the page with updated contents table
- [ ] No old long filenames remain
- [ ] `teaching-deck-krampis-biochemical-process-modeling.md` still present unchanged

---

## Task 5 — Also add to HuggingFace space (optional, lower priority)

The GLMP HuggingFace space at https://huggingface.co/spaces/garywelz/glmp should eventually mirror the GitHub paper links. This is lower priority than the GitHub tasks above — do it after the Thursday call if Krampis confirms the collaboration is moving forward. The specific change needed is updating the space description metadata to reference the Big Picture Goal and link to the GitHub repo.

---

## Files delivered this session

All of the following were generated in this Claude session and should be in your downloads or outputs:

| Filename | Destination | Action |
|---|---|---|
| `GLMP_Krampis_Plan.md` | `collaborations/krampis-virtual-cell/glmp-collaboration-plan-2026.md` | New file |
| `README.md` | `collaborations/krampis-virtual-cell/README.md` | Replace existing |

---

## Sending to Krampis — Tuesday or Wednesday

Once the GitHub tasks above are done and you've verified the repo looks correct, send Krampis a short email (Tuesday or Wednesday) with a direct link to the plan file:

**Subject:** GLMP collaboration — plan document ahead of Thursday

> Hi Konstantinos,
>
> Looking forward to Thursday. Here's the collaboration plan I mentioned — easiest to read directly on GitHub:
> https://github.com/garywelz/glmp/blob/main/collaborations/krampis-virtual-cell/glmp-collaboration-plan-2026.md
>
> The other working papers are in the same folder if you want to browse. Looking forward to the call.
>
> Gary

---

## What is NOT in scope for this Cursor session

The following are separate tasks discussed in the collaboration plan but not part of this GitHub handoff:

- Firestore `glmp_relevant` backfill script (separate GCP/Python task)
- `flowchart-source-papers.tsv` manifest (new file, content TBD)
- Methods paper revision (editorial task in Claude, not Cursor)
- RPE1 data download and classification script (computational biology task)
- GitHub Pages project home page (`docs/index.html`) — planned but not urgent before Thursday call
- HuggingFace space description update — lower priority, after Thursday call

---

*Generated June 11, 2026 · GLMP / Welz–Krampis collaboration preparation*
