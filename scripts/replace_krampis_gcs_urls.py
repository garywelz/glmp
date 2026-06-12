#!/usr/bin/env python3
"""Replace canonical GCS paper URLs with GitHub blob URLs under collaborations/krampis-virtual-cell."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
folder = REPO_ROOT / "collaborations" / "krampis-virtual-cell"

replacements = {
    "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/mathematics-processes-database/GLMP_Foundational_Typology.html":
        "https://github.com/garywelz/glmp/blob/main/collaborations/krampis-virtual-cell/primitive-relations-genomic-computational-class.md",
    "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/mathematics-processes-database/genome_as_computer_v2.html":
        "https://github.com/garywelz/glmp/blob/main/collaborations/krampis-virtual-cell/genome-as-computer.md",
    "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/mathematics-processes-database/empirical_sequel_draft.html":
        "https://github.com/garywelz/glmp/blob/main/collaborations/krampis-virtual-cell/circuit-class-predicts-virtual-cell-model-accuracy.md",
    "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/mathematics-processes-database/bioRxiv_Mermaid_Flowcharts_Perturbation_Methods_Draft.html":
        "https://github.com/garywelz/glmp/blob/main/collaborations/krampis-virtual-cell/mermaid-flowcharts-smarter-perturbation-design.md",
    "https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/mathematics-processes-database/GLMP_Genomic_Complexity_Synthesis_bioRxiv.html":
        "https://github.com/garywelz/glmp/blob/main/collaborations/krampis-virtual-cell/glmp-genomic-complexity-synthesis.md",
}


def main() -> None:
    if not folder.is_dir():
        print(f"ERROR: folder missing: {folder}")
        raise SystemExit(1)
    for path in sorted(folder.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        original = content
        for old, new in replacements.items():
            content = content.replace(old, new)
        if content != original:
            path.write_text(content, encoding="utf-8")
            print(f"Updated: {path.name}")
        else:
            print(f"No changes: {path.name}")


if __name__ == "__main__":
    main()
