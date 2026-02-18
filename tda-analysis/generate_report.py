"""
Generate TDA analysis report for GLMP processes.
"""

import pandas as pd
import numpy as np
from datetime import datetime

def generate_html_report(features_df, result, output_file="glmp_tda_report.html"):
    dgms = result["dgms"]
    h0, h1 = len(dgms[0]), len(dgms[1]) if len(dgms) > 1 else 0
    h2 = len(dgms[2]) if len(dgms) > 2 else 0
    html = """<!DOCTYPE html>
<html>
<head><title>GLMP TDA Analysis Report</title>
<style>
body { font-family: Arial; margin: 40px; }
h1 { color: #2c3e50; }
.metric { background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }
img { max-width: 800px; }
table { border-collapse: collapse; }
th, td { border: 1px solid #ddd; padding: 8px; }
</style>
</head>
<body>
<h1>Topological Data Analysis of GLMP Biological Processes</h1>
<p>Generated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
<h2>Dataset Overview</h2>
<div class="metric">
<p><strong>Processes:</strong> """ + str(len(features_df)) + """</p>
<p><strong>Organisms:</strong> """ + ", ".join(sorted(features_df["organism"].unique())) + """</p>
</div>
<h2>Persistence Diagram</h2>
<img src="glmp_persistence_diagram.png" alt="Persistence Diagram">
<h2>Findings</h2>
<div class="metric">
<p>H0 (components): """ + str(h0) + """</p>
<p>H1 (loops): """ + str(h1) + """</p>
<p>H2 (voids): """ + str(h2) + """</p>
</div>
<h2>Feature Statistics</h2>
""" + features_df.describe().to_html() + """
</body>
</html>"""
    with open(output_file, "w") as f:
        f.write(html)
    print("Generated", output_file)

if __name__ == "__main__":
    features_df = pd.read_csv("glmp_features.csv")
    result = np.load("persistence_result.npy", allow_pickle=True).item()
    generate_html_report(features_df, result)
