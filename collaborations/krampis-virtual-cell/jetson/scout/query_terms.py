"""
GLMP / CopernicusAI scout query term clusters (1–3).

Imported by split scout workers to extend PubMed acquisition.
Clusters 4–5 deferred per CURSOR_BRIEFING_DECODER_AUTOMATION.md.
"""

CLUSTER_1_GLMP = [
    "boolean gene regulatory networks",
    "typed computational models gene regulation",
    "Mermaid flowchart bioinformatics",
    "circuit topology gene expression",
    "formal grammar gene regulatory",
]

CLUSTER_2_DECODER = [
    "JASPAR transcription factor motifs",
    "PWM position weight matrix prokaryote",
    "FIMO motif enrichment promoter",
    "binding site prediction eukaryote",
    "regulatory sequence annotation",
]

CLUSTER_3_SYSTEMS_BIO = [
    "Biolink knowledge graph genomics",
    "KGX biological knowledge graph",
    "gene regulatory network inference",
    "RegVelo single cell regulatory",
    "systems biology Boolean model",
]

ALL_CLUSTERS_1_3 = CLUSTER_1_GLMP + CLUSTER_2_DECODER + CLUSTER_3_SYSTEMS_BIO

# Per-term PubMed supplement cap (small daily batch per term)
GLMP_PUBMED_MAX_RESULTS_PER_TERM = 10
