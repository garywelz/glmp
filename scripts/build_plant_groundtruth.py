#!/usr/bin/env python3
"""
Ground-truth plant circuits (Arabidopsis thaliana) — extends the collection beyond
microbes, yeast, human and synthetic with a new model organism.

  arabidopsis_circadian_clock   -> IV   CCA1/LHY <-> TOC1 transcriptional oscillator (Alabadí et al. 2001)
  arabidopsis_flc_vernalization -> V    FLC Polycomb epigenetic winter memory (Bastow et al. 2004)
  arabidopsis_aba_guard_cell    -> II   ABA stomatal-closure water homeostat (Cutler et al. 2010)

Writes to glmp-v2/processes/arabidopsis/. Run scripts/integrate_plant_groundtruth.py after.
Note: adds the organism "Arabidopsis thaliana"; the viewer (processLoader.js) and the
database table (glmp-database-table.html) are updated to recognize the arabidopsis_ prefix.
"""

import json
from pathlib import Path

from build_microbial_groundtruth import make_process

OUT_DIR = Path("glmp-v2/processes/arabidopsis")

SPECS = [
    {
        "id": "arabidopsis_circadian_clock",
        "name": "Arabidopsis Circadian Clock (CCA1/LHY–TOC1)",
        "organism": "Arabidopsis thaliana",
        "category": "Circadian Rhythm",
        "circuitClass": "IV",
        "topologyType": "delayed_negative_feedback_oscillator",
        "rationale": "Morning factors CCA1/LHY repress the evening gene TOC1, and the evening complex in turn represses CCA1/LHY; the interlocked delayed repression generates a ~24 h transcriptional oscillation entrained by light. Class IV oscillator.",
        "description": "The plant circadian clock. At dawn, light induces the morning Myb factors CCA1 and LHY, which repress evening genes including TOC1; as CCA1/LHY decay through the day, the evening complex (TOC1/PRRs) accumulates and represses CCA1/LHY. The mutual, time-delayed repression sustains a self-running ~24 h rhythm.",
        "scientificAccuracy": "The reciprocal CCA1/LHY–TOC1 regulation underlying the ~24 h clock is established (Alabadí et al. 2001).",
        "nodes": [
            ("A", "[Dawn light]", "red"),
            ("B", "[CCA1/LHY morning factors]", "yellow"),
            ("C", "[/Repress evening gene TOC1/]", "green"),
            ("D", "[TOC1 / evening complex]", "yellow"),
            ("E", "[/Represses CCA1/LHY/]", "green"),
            ("F", "(~24 h circadian oscillation)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", "⊣"),
            ("D", "E", ""), ("E", "B", "⊣ delayed"), ("B", "F", ""),
        ],
        "gates": (0, 0, 2),
        "sources": [
            {"title": "Reciprocal regulation between TOC1 and LHY/CCA1 within the Arabidopsis circadian clock", "authors": "Alabadí D, Oyama T, Yanovsky MJ, Harmon FG, Más P, Kay SA", "journal": "Science", "year": 2001, "volume": "293", "pages": "880-883", "pmid": "11486091", "doi": "10.1126/science.1061320"},
        ],
        "keywords": ["circadian", "CCA1", "LHY", "TOC1", "oscillator", "Arabidopsis", "Class IV", "ground truth"],
        "relatedProcesses": ["human_circadian_clock", "synthetic_repressilator"],
        "notes": "Ground-truth plant Class IV oscillator: interlocked CCA1/LHY–TOC1 delayed repression.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "Evening Element (TOC1 promoter)", "boundFactor": "CCA1/LHY", "operator": "NOT", "effect": "morning repression of TOC1", "sequenceMotif": "AAAATATCT (Evening Element)", "note": "TOC1/PRRs reciprocally repress CCA1/LHY -> oscillation"},
            ],
            "derivedLogic": "TOC1 = NOT CCA1/LHY ; CCA1/LHY = NOT evening-complex (delayed) -> ~24h cycle",
            "references": ["Alabadí et al. 2001"],
        },
    },
    {
        "id": "arabidopsis_flc_vernalization",
        "name": "FLC Vernalization Epigenetic Memory",
        "organism": "Arabidopsis thaliana",
        "category": "Epigenetic Inheritance / Flowering",
        "circuitClass": "V",
        "topologyType": "self_maintaining_polycomb_chromatin_memory",
        "rationale": "Prolonged cold induces VIN3 and PRC2 to deposit H3K27me3 across the floral repressor FLC, switching it to a silenced chromatin state that is self-maintained and mitotically heritable after cold ends — a cis-acting, self-modifying chromatin memory of winter. Class V.",
        "description": "How plants remember winter. The floral repressor FLC blocks flowering; prolonged cold induces VIN3 and the Polycomb PRC2 complex to nucleate and spread the repressive mark H3K27me3 over the FLC locus. The silenced state is then self-propagated through cell division so that, after winter, FLC stays off and the plant can flower — a heritable, chromatin-encoded epigenetic switch.",
        "scientificAccuracy": "Cold-induced, PRC2/H3K27me3-based heritable silencing of FLC is established (Bastow et al. 2004; Angel et al. 2011).",
        "nodes": [
            ("A", "[Prolonged cold winter]", "red"),
            ("B", "[VIN3 induced]", "green"),
            ("C", "[\\PRC2 deposits H3K27me3 at FLC/]", "green"),
            ("D", "[FLC epigenetically silenced]", "blue"),
            ("E", "[Silenced state mitotically inherited]", "green"),
            ("F", "(Heritable vernalized state, flowering enabled)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "C", "+ self-maintain"), ("D", "F", ""),
        ],
        "gates": (0, 0, 0),
        "sources": [
            {"title": "Vernalization requires epigenetic silencing of FLC by histone methylation", "authors": "Bastow R, Mylne JS, Lister C, Lippman Z, Martienssen RA, Dean C", "journal": "Nature", "year": 2004, "volume": "427", "pages": "164-167", "pmid": "14712277", "doi": "10.1038/nature02269"},
            {"title": "A Polycomb-based switch underlying quantitative epigenetic memory", "authors": "Angel A, Song J, Dean C, Howard M", "journal": "Nature", "year": 2011, "volume": "476", "pages": "105-108", "pmid": "21785438", "doi": "10.1038/nature10241"},
        ],
        "keywords": ["FLC", "vernalization", "Polycomb", "H3K27me3", "epigenetic memory", "Arabidopsis", "Class V", "ground truth"],
        "relatedProcesses": ["yeast_sup35_prion", "synthetic_integrase_memory"],
        "notes": "Ground-truth plant Class V: self-maintaining Polycomb chromatin memory (epigenetic winter memory).",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "FLC nucleation region", "boundFactor": "PRC2 (VRN2/CLF) -> H3K27me3", "operator": "SELF-MODIFY (chromatin)", "effect": "heritable silencing of FLC", "sequenceMotif": "FLC intron-1 nucleation element", "note": "read-write H3K27me3 spreading is mitotically inherited"},
            ],
            "derivedLogic": "FLC_state := silence(FLC) by H3K27me3 ; self-maintained -> heritable memory",
            "references": ["Bastow et al. 2004", "Angel et al. 2011"],
        },
    },
    {
        "id": "arabidopsis_aba_guard_cell",
        "name": "ABA Guard-Cell Stomatal Homeostat",
        "organism": "Arabidopsis thaliana",
        "category": "Hormone Signaling / Water Balance",
        "circuitClass": "II",
        "topologyType": "hormonal_negative_feedback_homeostat",
        "rationale": "Drought raises ABA; PYR/PYL receptors bind ABA and inhibit PP2C phosphatases, freeing SnRK2 kinases that open anion channels to close stomata; reduced transpiration restores water status, lowering ABA — a negative-feedback homeostat for plant water balance. Class II.",
        "description": "Plants conserve water through ABA-driven stomatal closure. Drought-elevated ABA is bound by PYR/PYL receptors that inhibit clade-A PP2C phosphatases, releasing SnRK2 kinases; SnRK2 activates SLAC1 anion channels and inhibits inward K+ channels, so guard cells lose turgor and stomata close. Lower transpiration rehydrates the plant, ABA falls, and stomata reopen.",
        "scientificAccuracy": "The PYR/PYL–PP2C–SnRK2 ABA core signaling module and stomatal water feedback are established (Ma et al. 2009; Park et al. 2009; Cutler et al. 2010).",
        "nodes": [
            ("A", "[Drought: ABA rises]", "red"),
            ("B", "[/PYR/PYL inhibit PP2C/]", "green"),
            ("C", "[SnRK2 kinases active]", "yellow"),
            ("D", "[Open SLAC1 anion channels; stomata close]", "green"),
            ("E", "[Transpiration drops; water restored]", "blue"),
            ("F", "[/Rehydration lowers ABA/]", "green"),
            ("G", "(Water-status homeostasis)", "violet"),
        ],
        "edges": [
            ("A", "B", ""), ("B", "C", ""), ("C", "D", ""),
            ("D", "E", ""), ("E", "F", ""), ("F", "A", "⊣ feedback"), ("E", "G", ""),
        ],
        "gates": (0, 0, 2),
        "sources": [
            {"title": "Regulators of PP2C phosphatase activity function as receptors for abscisic acid", "authors": "Ma Y, Szostkiewicz I, Korte A, et al.", "journal": "Science", "year": 2009, "volume": "324", "pages": "1064-1068", "pmid": "19407143", "doi": "10.1126/science.1172408"},
            {"title": "Abscisic acid: emergence of a core signaling network", "authors": "Cutler SR, Rodriguez PL, Finkelstein RR, Abrams SR", "journal": "Annual Review of Plant Biology", "year": 2010, "volume": "61", "pages": "651-679", "pmid": "20192755", "doi": "10.1146/annurev-arplant-042809-112122"},
        ],
        "keywords": ["ABA", "guard cell", "stomata", "PYR/PYL", "PP2C", "SnRK2", "negative feedback", "Arabidopsis", "Class II", "ground truth"],
        "relatedProcesses": ["human_glucocorticoid_hpa_axis", "ecoli_e._coli_osmotic_stress_response"],
        "notes": "Ground-truth plant Class II homeostat: ABA core module closes stomata; rehydration feedback lowers ABA.",
        "sequenceAnnotation": {
            "schemaVersion": "0.1",
            "regulatoryRegions": [
                {"name": "ABRE (ABA-responsive elements)", "boundFactor": "ABF/AREB bZIP (SnRK2-activated)", "operator": "IF ABA / NOT(PP2C)", "effect": "ABA-responsive gene + channel activation", "sequenceMotif": "ACGTGGC (ABRE)", "note": "water feedback lowers ABA -> closes the loop"},
            ],
            "derivedLogic": "stomatal-close = ABA AND NOT PP2C ; water restored -| ABA (negative feedback)",
            "references": ["Ma et al. 2009", "Cutler et al. 2010"],
        },
    },
]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for spec in SPECS:
        proc = make_process(spec)
        path = OUT_DIR / f"{spec['id']}.json"
        with open(path, "w") as fh:
            json.dump(proc, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        rows.append((proc["id"], proc["organism"], proc["circuitClass"],
                     proc.get("circuitSubclass") or "-", proc["totalNodes"],
                     proc["loops"], proc["logicGates"]))
    print(f"Wrote {len(rows)} Arabidopsis ground-truth files -> {OUT_DIR}\n")
    print(f"{'id':<32} {'organism':<22} {'cls':<4} {'sub':<5} {'nodes':<6} {'loops':<6} gates")
    for r in rows:
        print(f"{r[0]:<32} {r[1]:<22} {r[2]:<4} {r[3]:<5} {r[4]:<6} {r[5]:<6} {r[6]}")


if __name__ == "__main__":
    main()
