# Compute persistent homology on GLMP feature matrix
import numpy as np
import pandas as pd
from ripser import ripser
from persim import plot_diagrams
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("glmp_features.csv")
num_cols = ["node_count", "conditional_count", "or_gates", "and_gates", "not_gates"]
X = StandardScaler().fit_transform(df[num_cols].fillna(0).astype(float))
result = ripser(X, maxdim=2)
fig, ax = plt.subplots(figsize=(10, 8))
plot_diagrams(result["dgms"], show=False, ax=ax)
ax.set_title("Persistent Homology of GLMP Biological Processes")
plt.savefig("glmp_persistence_diagram.png", dpi=300, bbox_inches="tight")
plt.close()
np.save("persistence_result.npy", {"dgms": result["dgms"]})
print("Saved glmp_persistence_diagram.png and persistence_result.npy")
