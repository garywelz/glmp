# Krampis Virtual Cell Collaboration Drafts

This folder collects Markdown working drafts for a proposed collaboration between Gary Welz and Prof. Konstantinos Krampis on GLMP, perturbation design, genomic circuit complexity, and virtual cell model evaluation.

The Markdown files are intended to be the collaboration source of truth. The public HTML versions on Google Cloud Storage remain useful as readable snapshots, but edits should happen here so changes can be reviewed through GitHub pull requests.

## Contents

| File | Description | Source HTML |
| --- | --- | --- |
| `primitive-relations-genomic-computational-class.md` | Foundational typology paper: primitive relations, computational complexity, and the genomic computational class conjecture. | <https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/mathematics-processes-database/GLMP_Foundational_Typology.html> |
| `genome-as-computer.md` | Companion paper on logical primitives, runtime states, and limits of biological prediction. | <https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/mathematics-processes-database/genome_as_computer_v2.html> |
| `circuit-class-predicts-virtual-cell-model-accuracy.md` | Empirical sequel draft testing whether circuit class predicts virtual cell model accuracy. | <https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/mathematics-processes-database/empirical_sequel_draft.html> |
| `glmp-genomic-complexity-synthesis.md` | Biology-facing synthesis draft for the genomic regulatory complexity argument. | <https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/mathematics-processes-database/GLMP_Genomic_Complexity_Synthesis_bioRxiv.html> |
| `mermaid-flowcharts-smarter-perturbation-design.md` | Methods paper on Mermaid flowcharts and smarter perturbation design. | <https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/mathematics-processes-database/bioRxiv_Mermaid_Flowcharts_Perturbation_Methods_Draft.html> |
| `teaching-deck-krampis-biochemical-process-modeling.md` | Converted Markdown version of the local Krampis-oriented teaching/proposal slide deck available in the repository workspace. | Local source: `nsf-proposal/Biochemical_Process_Modeling_Project_Slides_Krampis_0318.html` |

## Collaboration Workflow

Recommended workflow for Prof. Krampis:

1. Fork the `garywelz/glmp` repository on GitHub.
2. Edit these Markdown files in the fork, either locally or through the GitHub web editor.
3. Open a pull request back to `garywelz/glmp` for review.

This keeps the main repository stable while making it easy to discuss edits line by line.

## Draft Status

These documents are working drafts and collaboration materials, not final peer-reviewed publications. Suggested edits should focus on:

- biological accuracy and terminology,
- single-cell and perturbation-data framing,
- virtual cell model evaluation design,
- claims that need stronger qualification,
- references and datasets suitable for empirical validation.

## Notes

- The HTML-to-Markdown conversion was automated with `pandoc` and lightly cleaned. Some inline HTML may remain where the source documents used styled links or custom layout.
- Mermaid diagrams and code blocks should be preserved as plain text where possible so GitHub can render or display them cleanly.
- If an exact April 2026 course slide deck should replace the included March 18 Krampis deck, add it here as Markdown or HTML and update this README.
