#!/usr/bin/env python3
"""
Phase 1: Gene Circuit Classification Pipeline
Classifies K562 Perturb-seq benchmark genes into GLMP complexity Classes I-V
based on regulatory circuit topology from TRRUST v2.

Output: gene_circuit_classes.tsv
"""

import csv
import sys
from collections import defaultdict
from pathlib import Path

import networkx as nx

TRRUST_FILE = Path("regulatory_data/trrust_rawdata.human.tsv")
GENE_LIST = Path("k562_benchmark_genes.txt")
OUTPUT_FILE = Path("gene_circuit_classes.tsv")

# ── Well-characterized circuits (literature overrides) ──────────────────
# These override any automated classification. Source: canonical papers.
KNOWN_CIRCUITS = {
    # Class II — negative autoregulation / negative feedback
    "HIF1A":  ("II", "negative_feedback",   "HIF1A-VHL oxygen-sensing loop", "literature"),
    "NFKB1":  ("II", "negative_feedback",   "NF-κB–IκBα negative feedback",  "literature"),
    "NFKB2":  ("II", "negative_feedback",   "NF-κB pathway negative feedback","literature"),
    "RELA":   ("II", "negative_feedback",   "NF-κB–IκBα negative feedback",  "literature"),
    "FOS":    ("II", "negative_autoregulation", "FOS negative autoregulation", "literature"),

    # Class III — bistable switches / positive feedback / mutual repression
    "TP53":   ("III", "toggle_switch",      "p53-MDM2 toggle",               "literature"),
    "MDM2":   ("III", "toggle_switch",      "MDM2-p53 toggle",               "literature"),
    "MYC":    ("III", "positive_feedback",  "MYC autoactivation + feedback",  "literature"),
    "GATA1":  ("III", "mutual_repression",  "GATA1-PU.1 bistable switch",    "literature"),
    "SPI1":   ("III", "mutual_repression",  "PU.1-GATA1 bistable switch",    "literature"),
    "NANOG":  ("III", "positive_feedback",  "Yamanaka/pluripotency circuit",  "literature"),
    "SOX2":   ("III", "positive_feedback",  "Yamanaka/pluripotency circuit",  "literature"),
    "POU5F1": ("III", "positive_feedback",  "Oct4 pluripotency circuit",      "literature"),
    "STAT3":  ("III", "positive_feedback",  "JAK-STAT positive feedback",     "literature"),
    "JUN":    ("II",  "negative_autoregulation", "JUN/AP-1 autorepression",   "literature"),
    "RB1":    ("III", "toggle_switch",      "Rb-E2F bistable switch",         "literature"),
    "E2F1":   ("III", "toggle_switch",      "E2F-Rb bistable switch",         "literature"),

    # Class IV — oscillatory / mixed feedback with delay
    "CLOCK":  ("IV", "oscillator",          "CLOCK-BMAL1 circadian loop",     "literature"),
    "ARNTL":  ("IV", "oscillator",          "BMAL1 circadian oscillator",     "literature"),
    "PER1":   ("IV", "oscillator",          "PER-CRY circadian feedback",     "literature"),
    "PER2":   ("IV", "oscillator",          "PER-CRY circadian feedback",     "literature"),
    "CRY1":   ("IV", "oscillator",          "CRY circadian negative arm",     "literature"),
    "CRY2":   ("IV", "oscillator",          "CRY circadian negative arm",     "literature"),
    "NR1D1":  ("IV", "oscillator",          "REV-ERBα circadian loop",        "literature"),

    # Class V — self-modifying epigenetic
    "DNMT1":  ("V", "self_modifying",       "DNMT1 maintenance methylation",  "literature"),
    "DNMT3A": ("V", "self_modifying",       "DNMT3A de novo + self-methylation","literature"),
    "DNMT3B": ("V", "self_modifying",       "DNMT3B de novo methylation",     "literature"),
    "EZH2":   ("V", "self_modifying",       "EZH2 PRC2 autosilencing",        "literature"),
    "EED":    ("V", "self_modifying",       "PRC2 component, epigenetic memory","literature"),
    "SUZ12":  ("V", "self_modifying",       "PRC2 component, epigenetic memory","literature"),
    "TET1":   ("V", "self_modifying",       "TET1 DNA demethylation",         "literature"),
    "TET2":   ("V", "self_modifying",       "TET2 DNA demethylation",         "literature"),
    "KDM5A":  ("V", "self_modifying",       "Histone demethylase, circuit rewiring","literature"),
    "KDM5B":  ("V", "self_modifying",       "Histone demethylase, circuit rewiring","literature"),
    "KMT2A":  ("V", "self_modifying",       "MLL1 histone methyltransferase", "literature"),
    "SETD2":  ("V", "self_modifying",       "H3K36 methyltransferase",        "literature"),
    "HDAC1":  ("V", "self_modifying",       "Histone deacetylase, chromatin remodeling","literature"),
    "HDAC2":  ("V", "self_modifying",       "Histone deacetylase, chromatin remodeling","literature"),
    "KAT5":   ("V", "self_modifying",       "Tip60 HAT, chromatin + DNA repair","literature"),
    "SMARCA4":("V", "self_modifying",       "SWI/SNF chromatin remodeling",   "literature"),
    "SMARCB1":("V", "self_modifying",       "SWI/SNF chromatin remodeling",   "literature"),
    "ARID1A": ("V", "self_modifying",       "SWI/SNF chromatin remodeling",   "literature"),
    "BRD4":   ("V", "self_modifying",       "Bromodomain reader, superenhancer regulation","literature"),
    "CBX5":   ("V", "self_modifying",       "HP1α heterochromatin maintenance","literature"),
}


def load_trrust(path):
    """Load TRRUST v2 into a NetworkX DiGraph with edge attributes."""
    G = nx.DiGraph()
    with open(path) as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            tf, target, reg_type, pmid = row[0], row[1], row[2], row[3]
            G.add_edge(tf, target, reg_type=reg_type, pmid=pmid)
    return G


def detect_autoregulation(G, gene):
    """Check if gene regulates itself."""
    if G.has_edge(gene, gene):
        etype = G[gene][gene].get("reg_type", "Unknown")
        if etype == "Repression":
            return "negative_autoregulation"
        elif etype == "Activation":
            return "positive_autoregulation"
        else:
            return "autoregulation_unknown"
    return None


def detect_mutual_repression(G, gene):
    """Check if gene participates in a mutual repression pair (A ⊣ B, B ⊣ A)."""
    pairs = []
    for target in G.successors(gene):
        if G.has_edge(target, gene):
            e1 = G[gene][target].get("reg_type", "Unknown")
            e2 = G[target][gene].get("reg_type", "Unknown")
            if e1 == "Repression" and e2 == "Repression":
                pairs.append(("mutual_repression", target))
            elif e1 == "Activation" and e2 == "Activation":
                pairs.append(("mutual_activation", target))
            elif (e1 == "Repression" and e2 == "Activation") or \
                 (e1 == "Activation" and e2 == "Repression"):
                pairs.append(("mixed_feedback", target))
    return pairs


def detect_feedback_loops(G, gene, max_length=4):
    """Find short directed cycles (length 3-4) involving gene via BFS."""
    loops = []
    for nbr in G.successors(gene):
        if nbr == gene:
            continue
        # Length-3 cycle: gene → nbr → X → gene
        for nbr2 in G.successors(nbr):
            if nbr2 == gene:
                loops.append([gene, nbr])
                continue
            if nbr2 == nbr:
                continue
            if max_length >= 3 and G.has_edge(nbr2, gene):
                loops.append([gene, nbr, nbr2])
            # Length-4 cycle: gene → nbr → nbr2 → X → gene
            if max_length >= 4:
                for nbr3 in G.successors(nbr2):
                    if nbr3 != gene and nbr3 != nbr and nbr3 != nbr2:
                        if G.has_edge(nbr3, gene):
                            loops.append([gene, nbr, nbr2, nbr3])
    return loops


def classify_by_network(G, gene):
    """
    Classify a gene's circuit topology using TRRUST network.
    Returns (class, topology_type, description, evidence_source)
    """
    is_tf = gene in G and G.out_degree(gene) > 0
    is_target = gene in G and G.in_degree(gene) > 0

    if not is_tf and not is_target:
        return None

    # Check autoregulation
    autoreg = detect_autoregulation(G, gene)

    # Check mutual repression / feedback pairs
    mutual = detect_mutual_repression(G, gene) if is_tf else []

    # Check for longer feedback loops
    loops = detect_feedback_loops(G, gene) if is_tf else []

    # Count negative vs positive edges
    neg_loops = [m for m in mutual if m[0] == "mutual_repression"]
    pos_loops = [m for m in mutual if m[0] == "mutual_activation"]
    mixed_loops = [m for m in mutual if m[0] == "mixed_feedback"]

    # Classification logic
    if neg_loops:
        partner = neg_loops[0][1]
        return ("III", "mutual_repression",
                f"mutual repression with {partner}", "TRRUST_motif")

    if pos_loops:
        partner = pos_loops[0][1]
        return ("III", "positive_feedback",
                f"mutual activation with {partner}", "TRRUST_motif")

    if autoreg == "positive_autoregulation":
        return ("III", "positive_autoregulation",
                "positive autoregulation (self-activation)", "TRRUST_motif")

    if mixed_loops:
        partner = mixed_loops[0][1]
        return ("II", "mixed_feedback_pair",
                f"mixed feedback with {partner}", "TRRUST_motif")

    if autoreg == "negative_autoregulation":
        return ("II", "negative_autoregulation",
                "negative autoregulation (self-repression)", "TRRUST_motif")

    if autoreg == "autoregulation_unknown":
        return ("II", "autoregulation_type_unknown",
                "autoregulation (type unknown, conservatively Class II)",
                "TRRUST_motif")

    if loops:
        longest = max(loops, key=len)
        cycle_str = " → ".join(longest + [longest[0]])
        neg_count = sum(
            1 for i in range(len(longest))
            if G.has_edge(longest[i], longest[(i+1) % len(longest)])
            and G[longest[i]][longest[(i+1) % len(longest)]].get("reg_type") == "Repression"
        )
        if neg_count >= 2 and len(longest) >= 3:
            return ("IV", "feedback_loop_oscillatory",
                    f"cycle with ≥2 repressions ({cycle_str})", "TRRUST_motif")
        elif neg_count >= 1:
            return ("II", "negative_feedback_loop",
                    f"negative feedback loop ({cycle_str})", "TRRUST_motif")
        else:
            return ("III", "positive_feedback_loop",
                    f"positive feedback loop ({cycle_str})", "TRRUST_motif")

    # TF with no detected feedback → Class I (feed-forward)
    if is_tf:
        n_targets = G.out_degree(gene)
        return ("I", "feed_forward_tf",
                f"TF with {n_targets} known targets, no detected feedback",
                "TRRUST_topology")

    # Target only, not a TF → Class I (regulated but no feedback role)
    if is_target and not is_tf:
        regulators = list(G.predecessors(gene))
        return ("I", "feed_forward_target",
                f"regulated by {len(regulators)} TFs ({', '.join(regulators[:3])}{'...' if len(regulators)>3 else ''}), no feedback role",
                "TRRUST_topology")

    return None


def is_chromatin_modifier(gene):
    """
    Curated: genes encoding chromatin/epigenetic enzymes or structural
    subunits whose function implies self-modifying circuit capability.
    Conservative — excludes WD-repeat scaffolds unless specifically
    known to be core chromatin complex members.
    """
    prefixes = {
        "HDAC", "KDM", "KMT", "DNMT", "TET", "BRD",
        "SMARC", "ARID", "CHD", "RING1", "SUV39",
        "SETD", "DOT1", "EHMT", "NSD", "PRMT",
        "JMJD", "YEATS", "MBD", "MECP",
    }
    for kw in prefixes:
        if gene.startswith(kw):
            return True
    specific = {
        "EP300", "CREBBP", "KAT5", "KAT6A", "KAT6B",
        "CBX1", "CBX3", "CBX5", "CBX7",
        "PCGF1", "PCGF2", "PCGF6", "BMI1",
        "PHF12", "PHF19", "JARID2", "MTF2",
        "WDR5", "WDR82", "ASH2L", "RBBP5", "DPY30",
        "RBBP4", "RBBP7",
        "BAP1", "INO80", "INO80B", "SRCAP",
        "NCOA1", "NCOA3",
    }
    return gene in specific


# ── Signaling pathway genes with known feedback topology ────────────────
# These genes participate in well-characterized signaling feedback loops.
SIGNALING_FEEDBACK = {
    # Class II — pathway-level negative feedback
    "DUSP1":  ("II", "negative_feedback", "MAPK pathway negative feedback phosphatase", "pathway_annotation"),
    "DUSP6":  ("II", "negative_feedback", "ERK-DUSP6 negative feedback", "pathway_annotation"),
    "SPRY1":  ("II", "negative_feedback", "Sprouty negative feedback on RTK signaling", "pathway_annotation"),
    "SPRY2":  ("II", "negative_feedback", "Sprouty negative feedback on RTK signaling", "pathway_annotation"),
    "SOCS1":  ("II", "negative_feedback", "SOCS1 negative feedback on JAK-STAT", "pathway_annotation"),
    "SOCS3":  ("II", "negative_feedback", "SOCS3 negative feedback on JAK-STAT", "pathway_annotation"),
    "CDKN1A": ("II", "negative_feedback", "p21 CDK inhibitor (p53 feedback)", "pathway_annotation"),
    "CDKN1B": ("II", "negative_feedback", "p27 CDK inhibitor (mitogenic signal feedback)", "pathway_annotation"),
    "CDKN2A": ("II", "negative_feedback", "p16-Rb tumor suppressor feedback", "pathway_annotation"),
    "PTEN":   ("II", "negative_feedback", "PI3K-AKT pathway negative regulator", "pathway_annotation"),
    "TSC1":   ("II", "negative_feedback", "mTOR pathway negative regulator", "pathway_annotation"),
    "TSC2":   ("II", "negative_feedback", "mTOR pathway negative regulator", "pathway_annotation"),
    "NF1":    ("II", "negative_feedback", "RAS-GAP negative regulator", "pathway_annotation"),
    "PTPN11": ("II", "negative_feedback", "SHP2 phosphatase in RAS pathway feedback", "pathway_annotation"),
    "BCL2L1": ("III", "positive_feedback", "BCL-xL anti-apoptotic (survival/death bistability)", "pathway_annotation"),
    "BCL2":   ("III", "positive_feedback", "BCL2 anti-apoptotic (survival/death bistability)", "pathway_annotation"),
    "BAX":    ("III", "positive_feedback", "BAX pro-apoptotic (survival/death bistability)", "pathway_annotation"),
    "CTNNB1": ("III", "positive_feedback", "β-catenin Wnt pathway positive feedback", "pathway_annotation"),
    "AKT1":   ("III", "positive_feedback", "AKT survival signaling positive feedback", "pathway_annotation"),
    "PIK3CA": ("III", "positive_feedback", "PI3K catalytic subunit (AKT positive feedback loop)", "pathway_annotation"),
    "PIK3C3": ("II", "negative_feedback", "VPS34 autophagy/mTOR regulatory loop", "pathway_annotation"),
    "MTOR":   ("III", "positive_feedback", "mTOR growth signaling with positive feedback", "pathway_annotation"),
    "MAPK1":  ("II", "negative_feedback", "ERK2 MAPK cascade with DUSP feedback", "pathway_annotation"),
    "MAPK3":  ("II", "negative_feedback", "ERK1 MAPK cascade with DUSP feedback", "pathway_annotation"),
    "MAP2K1": ("II", "negative_feedback", "MEK1 MAPK cascade with ERK feedback phosphorylation", "pathway_annotation"),
    "RAF1":   ("II", "negative_feedback", "RAF1 with ERK negative feedback phosphorylation", "pathway_annotation"),
}


def classify_gene(G, gene):
    """Master classification: literature override > network motif > heuristic."""
    # Priority 1: known literature circuits
    if gene in KNOWN_CIRCUITS:
        cls, topo, desc, src = KNOWN_CIRCUITS[gene]
        return cls, topo, desc, src, "high"

    # Priority 2: TRRUST network motif detection
    result = classify_by_network(G, gene)
    if result:
        cls, topo, desc, src = result
        confidence = "high" if src == "TRRUST_motif" else "medium"
        return cls, topo, desc, src, confidence

    # Priority 3: signaling pathway feedback annotation
    if gene in SIGNALING_FEEDBACK:
        cls, topo, desc, src = SIGNALING_FEEDBACK[gene]
        return cls, topo, desc, src, "medium"

    # Priority 4: chromatin modifier heuristic → Class V
    if is_chromatin_modifier(gene):
        return ("V", "chromatin_modifier",
                "encodes chromatin/epigenetic modifier",
                "gene_function", "medium")

    # Priority 5: default — no regulatory info → Class I (feed-forward)
    return ("I", "no_regulatory_info",
            "no known feedback involvement; default feed-forward",
            "default", "low")


def main():
    print("Loading TRRUST v2 network...")
    G = load_trrust(TRRUST_FILE)
    print(f"  {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    print("Loading K562 benchmark gene list...")
    with open(GENE_LIST) as f:
        genes = [line.strip() for line in f if line.strip()]
    print(f"  {len(genes)} genes")

    print("Classifying circuits...")
    results = []
    class_counts = defaultdict(int)
    source_counts = defaultdict(int)
    confidence_counts = defaultdict(int)

    for gene in genes:
        cls, topo, desc, source, confidence = classify_gene(G, gene)
        results.append({
            "gene": gene,
            "circuit_class": cls,
            "topology_type": topo,
            "description": desc,
            "evidence_source": source,
            "confidence": confidence,
        })
        class_counts[cls] += 1
        source_counts[source] += 1
        confidence_counts[confidence] += 1

    # Write output
    print(f"\nWriting {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["gene", "circuit_class", "topology_type",
                         "description", "evidence_source", "confidence"],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(results)

    # Summary
    print("\n" + "=" * 60)
    print("CLASSIFICATION SUMMARY")
    print("=" * 60)
    print(f"\nBy class:")
    for cls in sorted(class_counts):
        pct = 100 * class_counts[cls] / len(genes)
        print(f"  Class {cls}: {class_counts[cls]:4d}  ({pct:5.1f}%)")

    print(f"\nBy evidence source:")
    for src in sorted(source_counts, key=source_counts.get, reverse=True):
        print(f"  {src:30s}: {source_counts[src]:4d}")

    print(f"\nBy confidence:")
    for conf in ["high", "medium", "low"]:
        print(f"  {conf:10s}: {confidence_counts.get(conf, 0):4d}")

    print(f"\nOutput: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
