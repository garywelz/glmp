#!/usr/bin/env python3
"""
Rebuild GLMP v2 metadata.json for the database table + viewer.

Scans process JSON files under:
  /home/gdubs/glmp/glmp-v2/processes/{ecoli,yeast,bacillus}/*.json

Outputs:
  - /home/gdubs/glmp/glmp-v2/data/metadata.json
  - /home/gdubs/glmp/glmp-v2/metadata.json   (copy for backwards-compatible table URL)
"""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Tuple


BASE = Path("/home/gdubs/glmp/glmp-v2/processes")
OUT_DATA = Path("/home/gdubs/glmp/glmp-v2/data/metadata.json")
OUT_ROOT = Path("/home/gdubs/glmp/glmp-v2/metadata.json")


def safe_int(v: Any, default: int = 0) -> int:
    try:
        if v is None:
            return default
        return int(v)
    except Exception:
        return default


def extract_gate_counts(proc: Dict[str, Any]) -> Tuple[int, int, int]:
    # Prefer root fields if present
    lg_root = proc.get("logicGates") or {}
    or_root = safe_int(lg_root.get("or"))
    and_root = safe_int(lg_root.get("and"))
    not_root = safe_int(lg_root.get("not"))
    if or_root or and_root or not_root:
        return or_root, and_root, not_root

    # Else fall back to complexity.logicGates (used in some v2 files)
    cplx = proc.get("complexity") or {}
    lg = (cplx.get("logicGates") or {})
    # two possible schemas: {orGates,andGates,total} or {or,and,not,total}
    or_g = safe_int(lg.get("orGates", lg.get("or")))
    and_g = safe_int(lg.get("andGates", lg.get("and")))
    not_g = safe_int(lg.get("notGates", lg.get("not")))
    return or_g, and_g, not_g


def extract_nodes(proc: Dict[str, Any]) -> int:
    if "totalNodes" in proc:
        return safe_int(proc.get("totalNodes"))
    cplx = proc.get("complexity") or {}
    return safe_int(cplx.get("nodes", proc.get("nodes")))


def extract_conditionals(proc: Dict[str, Any]) -> int:
    return safe_int(proc.get("conditionals"))


def extract_complexity_label(proc: Dict[str, Any]) -> str:
    cplx = proc.get("complexity") or {}
    label = cplx.get("detailLevel") or proc.get("complexity")
    if isinstance(label, str) and label.strip():
        return label
    return "unknown"


def scan_processes() -> List[Dict[str, Any]]:
    processes: List[Dict[str, Any]] = []
    for org_dir in ["ecoli", "yeast", "bacillus"]:
        pdir = BASE / org_dir
        if not pdir.exists():
            continue
        for jf in sorted(pdir.glob("*.json")):
            data = json.loads(jf.read_text(encoding="utf-8"))
            pid = data.get("id") or jf.stem

            or_g, and_g, not_g = extract_gate_counts(data)
            nodes = extract_nodes(data)
            conditionals = extract_conditionals(data)

            sources = data.get("sources") or data.get("citations") or []
            citations_count = len(sources) if isinstance(sources, list) else 0

            processes.append(
                {
                    "id": pid,
                    "name": data.get("name", "Unknown Process"),
                    "organism": data.get("organism", "Unknown"),
                    "category": data.get("category", "Unknown"),
                    "description": data.get("description", ""),
                    "verified": bool(data.get("verified", False)),
                    "created": data.get("created", ""),
                    "lastUpdated": data.get("lastUpdated", ""),
                    "citations": citations_count,
                    "complexity": extract_complexity_label(data),
                    "nodes": nodes,
                    "conditionals": conditionals,
                    "logicGates": {"or": or_g, "and": and_g, "total": (or_g + and_g)},
                    "notGates": not_g,
                }
            )
    return processes


def build_metadata(processes: List[Dict[str, Any]]) -> Dict[str, Any]:
    today = str(date.today())

    organism_counts = defaultdict(int)
    category_counts = defaultdict(int)

    totals = {
        "totalNodes": 0,
        "totalConditionals": 0,
        "orGates": 0,
        "andGates": 0,
        "notGates": 0,
        "totalLogicGates": 0,
        "verifiedProcesses": 0,
    }

    for p in processes:
        organism_counts[p.get("organism") or "Unknown"] += 1
        category_counts[p.get("category") or "Unknown"] += 1

        totals["totalNodes"] += safe_int(p.get("nodes"))
        totals["totalConditionals"] += safe_int(p.get("conditionals"))
        totals["orGates"] += safe_int((p.get("logicGates") or {}).get("or"))
        totals["andGates"] += safe_int((p.get("logicGates") or {}).get("and"))
        totals["notGates"] += safe_int(p.get("notGates"))
        totals["verifiedProcesses"] += 1 if p.get("verified") else 0

    totals["totalLogicGates"] = totals["orGates"] + totals["andGates"] + totals["notGates"]

    organisms = [{"name": k, "processCount": v} for k, v in sorted(organism_counts.items(), key=lambda kv: (-kv[1], kv[0]))]
    categories = [{"name": k, "processCount": v} for k, v in sorted(category_counts.items(), key=lambda kv: (-kv[1], kv[0]))]

    return {
        "name": "GLMP Process Collection",
        "version": "2.2.0",
        "created": today,
        "lastUpdated": today,
        "totalProcesses": len(processes),
        "organisms": organisms,
        "categories": categories,
        "statistics": totals,
        "processes": processes,
    }


def main() -> None:
    processes = scan_processes()
    if not processes:
        raise SystemExit(f"No process JSON files found under {BASE}")

    metadata = build_metadata(processes)

    OUT_DATA.parent.mkdir(parents=True, exist_ok=True)
    OUT_DATA.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUT_ROOT.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Wrote: {OUT_DATA}")
    print(f"Wrote: {OUT_ROOT}")
    print(f"Total processes: {metadata['totalProcesses']}")
    print(f"Totals: nodes={metadata['statistics']['totalNodes']}, cond={metadata['statistics']['totalConditionals']}, OR={metadata['statistics']['orGates']}, AND={metadata['statistics']['andGates']}, NOT={metadata['statistics']['notGates']}")


if __name__ == "__main__":
    main()

