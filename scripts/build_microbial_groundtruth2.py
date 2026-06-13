#!/usr/bin/env python3
"""
Batch 2 of ground-truth microbial circuits (extends build_microbial_groundtruth.py).
Textbook bacterial decision circuits filling ladder gaps in the prokaryotic set.

  bacillus_comk_competence    -> III (IIIa)  ComK competence bistable switch (Maamar & Dubnau 2005)
  bacillus_spo0a_sporulation  -> III          Spo0A phosphorelay sporulation commitment (Hilbert & Piggot 2004)
  ecoli_sos_lexa              -> II           SOS DNA-damage response, LexA/RecA negative feedback (Little & Mount 1982)
  ecoli_flhdc_flagellar       -> I            flagellar FlhDC->FliA->class 3 feed-forward cascade (Kalir et al. 2001)

Files write into glmp-v2/processes/{bacillus,ecoli}/ by id prefix; run
scripts/integrate_microbial_groundtruth2.py afterward to index them.
"""

import json

from build_microbial_groundtruth import make_process, out_dir_for

SPECS = [
    {
        "id": "bacillus_comk_competence",
        "name": "ComK Competence Bistable Switch",
        "organism": "Bacillus subtilis",
        "category": "Developmental Switch / Competence",
        "circuitClass": "III", "circuitSubclass": "IIIa",
        "topologyType": "positive_autoregulation_bistable",
        "rationale": "ComK activates its own promoter (positive autoregulation) while ComS shields ComK from MecA/ClpCP degradation; the positive feedback makes entry into competence a bistable, noise-driven switch so that only a subpopulation becomes competent — a persistent (IIIa) state.",
        "description": "Bacillus subtilis stochastically enters the competence state via the master regulator ComK. ComK activates its own gene (positive autoregulation), and ComS competitively protects ComK from MecA/ClpCP proteolysis. The positive feedback creates bistability: cells that cross a noise-set threshold latch into the competent state, while the rest stay vegetative.",
        "scientificAccuracy": "ComK positive autoregulation, ComS-controlled proteolysis, and the resulting bistable competence are established (Maamar & Dubnau 2005; Süel et al. 2006).",
        "nodes": [
            ("A", "[Stationary phase / quorum signal]", "red"),
            ("B", "[ComS produced]", "yellow"),
            ("C", "[/ComS blocks MecA degradation of ComK/]", "green"),
            ("D", "[ComK accumulates]", "yellow"),
            ("E", "[\\ComK activates its own promoter/]", "green"),
            ("F", "[Competence genes ON]", "green"),
            ("G", "(Bistable competent subpopulation)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", "⊣ MecA"), ("C", "D", ""),
            ("D", "E", ""), ("E", "D", "+"), ("D", "F", ""), ("F", "G", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Bistability in the Bacillus subtilis K-state (competence) system requires a positive feedback loop", "authors": "Maamar H, Dubnau D", "journal": "Molecular Microbiology", "year": 2005, "volume": "56", "pages": "615-624", "pmid": "15819619", "doi": "10.1111/j.1365-2958.2005.04592.x"},
            {"title": "An excitable gene regulatory circuit induces transient cellular differentiation", "authors": "Süel GM, Garcia-Ojalvo J, Liberman LM, Elowitz MB", "journal": "Nature", "year": 2006, "volume": "440", "pages": "545-550", "pmid": "16554821", "doi": "10.1038/nature04588"},
        ],
        "keywords": ["ComK", "ComS", "competence", "bistable", "positive autoregulation", "Bacillus", "Class IIIa", "ground truth"],
        "relatedProcesses": ["bacillus_sporulation", "synthetic_positive_autoregulation"],
        "notes": "Ground-truth Bacillus Class IIIa bistable switch (competence); ComK positive autoregulation + ComS-gated proteolysis.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "comK promoter (K-boxes)", "boundFactor": "ComK (cooperative)", "operator": "IF / positive feedback", "effect": "autoactivation of comK", "sequenceMotif": "AAAA-N5-TTTT (K-box)", "note": "ComS protects ComK from MecA/ClpCP -> bistable"},
            ],
            "derivedLogic": "ComK = IF ComK(t-τ) AND NOT degraded(MecA) -> bistable competence",
            "references": ["Maamar & Dubnau 2005", "Süel et al. 2006"],
        },
    },
    {
        "id": "bacillus_spo0a_sporulation",
        "name": "Spo0A Phosphorelay Sporulation Commitment",
        "organism": "Bacillus subtilis",
        "category": "Developmental Switch / Sporulation",
        "circuitClass": "III",
        "topologyType": "threshold_positive_feedback_bistable_commitment",
        "rationale": "A multi-kinase phosphorelay (KinA→Spo0F→Spo0B→Spo0A) raises Spo0A~P; once Spo0A~P crosses a threshold it activates sporulation sigma factors and feeds back to amplify the relay, producing an essentially irreversible, switch-like commitment to sporulation. Class III.",
        "description": "Starvation drives a phosphorelay that progressively phosphorylates the master regulator Spo0A. Spo0A~P accumulation is gradual until it crosses a threshold, at which point it activates the sporulation sigma-factor cascade and reinforces its own activation — converting a graded starvation signal into a discrete, irreversible commitment to form a spore.",
        "scientificAccuracy": "The Spo0A phosphorelay and threshold/bistable sporulation commitment are established (Burbulys, Trach & Hoch 1991; Hilbert & Piggot 2004).",
        "nodes": [
            ("A", "[Starvation]", "red"),
            ("B", "[KinA phosphorelay]", "green"),
            ("C", "[Spo0A~P rises]", "yellow"),
            ("D", "{Spo0A~P above threshold?}", "blue"),
            ("E", "[\\Activates sporulation sigma factors/]", "green"),
            ("F", "[Positive feedback raises Spo0A~P]", "green"),
            ("G", "(Irreversible sporulation commitment)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", "Yes"), ("E", "F", ""), ("F", "C", "+"), ("E", "G", ""),
        ],
        "gates": (0, 0, 0),
        "sources": [
            {"title": "Initiation of sporulation in B. subtilis is controlled by a multicomponent phosphorelay", "authors": "Burbulys D, Trach KA, Hoch JA", "journal": "Cell", "year": 1991, "volume": "64", "pages": "545-552", "pmid": "1846779", "doi": "10.1016/0092-8674(91)90238-T"},
            {"title": "Compartmentalization of gene expression during Bacillus subtilis spore formation", "authors": "Hilbert DW, Piggot PJ", "journal": "Microbiology and Molecular Biology Reviews", "year": 2004, "volume": "68", "pages": "234-262", "pmid": "15187183", "doi": "10.1128/MMBR.68.2.234-262.2004"},
        ],
        "keywords": ["Spo0A", "sporulation", "phosphorelay", "threshold", "commitment", "Bacillus", "Class III", "ground truth"],
        "relatedProcesses": ["bacillus_comk_competence", "bacillus_sporulation"],
        "notes": "Ground-truth Bacillus Class III commitment switch (sporulation); phosphorelay + threshold positive feedback.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "Spo0A boxes (sporulation promoters)", "boundFactor": "Spo0A~P", "operator": "threshold IF", "effect": "activates sigma-F/sigma-E cascade above threshold", "sequenceMotif": "TGTCGAA (0A box)", "note": "phosphorelay sets Spo0A~P; feedback amplifies"},
            ],
            "derivedLogic": "sporulation = IF Spo0A~P>θ (threshold commitment)",
            "references": ["Burbulys et al. 1991", "Hilbert & Piggot 2004"],
        },
    },
    {
        "id": "ecoli_sos_lexa",
        "name": "SOS DNA-Damage Response (LexA/RecA)",
        "organism": "E. coli",
        "category": "DNA Damage Response",
        "circuitClass": "II",
        "topologyType": "derepression_negative_feedback_homeostat",
        "rationale": "DNA damage generates RecA-ssDNA filaments that stimulate LexA autocleavage, derepressing SOS repair genes; successful repair removes the ssDNA signal so LexA re-accumulates and represses the regulon — a negative-feedback homeostat that turns the response off once damage is fixed. Class II.",
        "description": "The bacterial DNA-damage response. Single-stranded DNA at lesions nucleates RecA filaments (RecA*) that act as a co-protease stimulating LexA self-cleavage; loss of the LexA repressor switches on SOS repair genes. As repair eliminates the ssDNA, RecA* falls, LexA re-accumulates, and the regulon is repressed again — a self-limiting negative-feedback loop.",
        "scientificAccuracy": "RecA-stimulated LexA autocleavage and the self-limiting SOS regulon are textbook (Little & Mount 1982; Friedberg et al.).",
        "nodes": [
            ("A", "[DNA damage: ssDNA]", "red"),
            ("B", "[RecA* filament]", "green"),
            ("C", "[/Stimulates LexA autocleavage/]", "green"),
            ("D", "[SOS repair genes derepressed]", "green"),
            ("E", "[/Repair removes ssDNA signal/]", "green"),
            ("F", "(Damage cleared, LexA re-represses)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", "⊣ LexA off"),
            ("D", "E", ""), ("E", "A", "⊣ feedback"), ("E", "F", ""),
        ],
        "gates": (0, 0, 2),
        "sources": [
            {"title": "The SOS regulatory system of Escherichia coli", "authors": "Little JW, Mount DW", "journal": "Cell", "year": 1982, "volume": "29", "pages": "11-22", "pmid": "7053433", "doi": "10.1016/0092-8674(82)90085-X"},
        ],
        "keywords": ["SOS", "LexA", "RecA", "DNA repair", "derepression", "negative feedback", "Class II", "ground truth"],
        "relatedProcesses": ["human_p53_apoptosis_decision", "ecoli_dna_repair"],
        "notes": "Ground-truth E. coli Class II damage homeostat: RecA-stimulated LexA cleavage, self-limited by repair.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "SOS boxes (recA, lexA, sulA, umuDC promoters)", "boundFactor": "LexA repressor", "operator": "NOT (relieved by RecA*)", "effect": "derepression on damage", "sequenceMotif": "CTGT-N8-ACAG (SOS box)", "note": "repair removes signal -> LexA re-represses"},
            ],
            "derivedLogic": "SOS genes = NOT LexA ; LexA cleaved by RecA*(damage); repair -| damage (negative feedback)",
            "references": ["Little & Mount 1982"],
        },
    },
    {
        "id": "ecoli_flhdc_flagellar",
        "name": "Flagellar Gene Feed-Forward Cascade (FlhDC)",
        "organism": "E. coli",
        "category": "Motility / Transcriptional Cascade",
        "circuitClass": "I",
        "topologyType": "transcriptional_feed_forward_cascade",
        "rationale": "Flagellar biogenesis is a temporally ordered feed-forward cascade: master regulator FlhDC (class 1) activates class-2 genes including the sigma factor FliA, which activates class-3 flagellin genes; an FlgM checkpoint delays FliA until the basal body is built. Pure feed-forward, no regulatory loop. Class I.",
        "description": "Assembly of the flagellum is timed by a transcriptional cascade. FlhDC (class 1) turns on class-2 genes (basal body and the sigma factor FliA); the anti-sigma FlgM holds FliA inactive until the hook-basal-body is complete and FlgM is secreted out, after which FliA fires class-3 flagellin genes. The just-in-time logic is feed-forward.",
        "scientificAccuracy": "The class 1→2→3 flagellar cascade and FlgM/FliA checkpoint are established (Kalir et al. 2001; Chevance & Hughes 2008).",
        "nodes": [
            ("A", "[FlhDC master regulator]", "red"),
            ("B", "[Class 2: basal body + FliA]", "green"),
            ("C", "[/FlgM holds FliA until body built/]", "green"),
            ("D", "[FliA sigma-28 activated]", "yellow"),
            ("E", "[Class 3: flagellin genes]", "green"),
            ("F", "(Assembled motile flagellum)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("B", "D", ""),
            ("C", "D", "⊣ FlgM"), ("D", "E", ""), ("E", "F", ""),
        ],
        "gates": (0, 0, 1),
        "sources": [
            {"title": "Ordering genes in a flagella pathway by analysis of expression kinetics from living bacteria", "authors": "Kalir S, McClure J, Pabbaraju K, et al.", "journal": "Science", "year": 2001, "volume": "292", "pages": "2080-2083", "pmid": "11408658", "doi": "10.1126/science.1058758"},
            {"title": "Coordinating assembly of a bacterial macromolecular machine", "authors": "Chevance FFV, Hughes KT", "journal": "Nature Reviews Microbiology", "year": 2008, "volume": "6", "pages": "455-465", "pmid": "18483484", "doi": "10.1038/nrmicro1887"},
        ],
        "keywords": ["flagella", "FlhDC", "FliA", "FlgM", "feed-forward", "transcriptional cascade", "Class I", "ground truth"],
        "relatedProcesses": ["ecoli_chemotaxis", "synthetic_layered_nor_cascade"],
        "notes": "Ground-truth E. coli Class I feed-forward cascade (flagellar biogenesis); FlgM/FliA timing checkpoint, no feedback loop.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "class-3 promoters (fliC etc.)", "boundFactor": "sigma-28 FliA (gated by FlgM)", "operator": "IF / NOT(FlgM)", "effect": "late flagellin expression", "sequenceMotif": "sigma-28 consensus (TAAAGTTT / GCCGATAA)", "note": "feed-forward timing, no loop"},
            ],
            "derivedLogic": "class3 = FliA AND NOT FlgM ; FlhDC -> FliA -> class3 (cascade)",
            "references": ["Kalir et al. 2001"],
        },
    },
]


def main():
    rows = []
    for spec in SPECS:
        proc = make_process(spec)
        d = out_dir_for(spec["id"])
        d.mkdir(parents=True, exist_ok=True)
        path = d / f"{spec['id']}.json"
        with open(path, "w") as fh:
            json.dump(proc, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        rows.append((proc["id"], proc["organism"], proc["circuitClass"],
                     proc.get("circuitSubclass") or "-", proc["totalNodes"],
                     proc["loops"], proc["logicGates"]))
    print(f"Wrote {len(rows)} microbial ground-truth Batch-2 files\n")
    print(f"{'id':<28} {'organism':<20} {'cls':<4} {'sub':<5} {'nodes':<6} {'loops':<6} gates")
    for r in rows:
        print(f"{r[0]:<28} {r[1]:<20} {r[2]:<4} {r[3]:<5} {r[4]:<6} {r[5]:<6} {r[6]}")


if __name__ == "__main__":
    main()
