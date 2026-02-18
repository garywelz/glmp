#!/usr/bin/env python3
"""
Run the full GLMP TDA pipeline:
1. Fetch GLMP metadata
2. Compute persistence
3. Generate report
"""

import subprocess
import sys

def main():
    steps = [
        ("fetch_glmp_data.py", "Fetching GLMP data"),
        ("compute_persistence.py", "Computing persistent homology"),
        ("generate_report.py", "Generating HTML report"),
    ]
    for script, desc in steps:
        print(f"\n>>> {desc} ({script})")
        rc = subprocess.run([sys.executable, script])
        if rc.returncode != 0:
            print(f"ERROR: {script} failed with code {rc.returncode}")
            sys.exit(rc.returncode)
    print("\n>>> Pipeline complete. Outputs:")
    print("    - glmp_features.csv")
    print("    - glmp_persistence_diagram.png")
    print("    - glmp_tda_report.html")

if __name__ == "__main__":
    main()
