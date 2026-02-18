# Push TDA Analysis to garywelz/glmp

## Option A: Copy folder into your glmp clone

If you have the glmp repo cloned locally:

```bash
# 1. Navigate to your glmp repo
cd /path/to/glmp   # e.g. ~/glmp or ~/repos/glmp

# 2. Copy tda-analysis (excluding venv) - adjust source path as needed
rsync -av --exclude='venv' --exclude='__pycache__' --exclude='*.npy' \
  ~/copernicus-web-public/glmp-tda-analysis/ ./tda-analysis/

# 3. Commit and push
git add tda-analysis/
git commit -m "Add TDA analysis: persistent homology on 108 GLMP processes"
git push origin main
```

## Option B: Add glmp as a sibling and copy

```bash
# If glmp is cloned (e.g. ~/glmp), copy and clean:
cp -r ~/copernicus-web-public/glmp-tda-analysis ~/glmp/tda-analysis
cd ~/glmp
# Remove venv before committing
rm -rf tda-analysis/venv tda-analysis/__pycache__ tda-analysis/*.npy
git add tda-analysis/
git commit -m "Add TDA analysis: persistent homology on 108 GLMP processes"
git push origin main
```

## What gets committed

- Scripts: `fetch_glmp_data.py`, `compute_persistence.py`, `generate_report.py`, `analyze_h1_loops.py`
- Data: `glmp_features.csv`
- Outputs: `glmp_persistence_diagram.png`, `glmp_tda_report.html`
- Reports: `*.pdf`, `*.md`
- Config: `README.md`, `requirements.txt`, `.gitignore`

## Share link

After pushing: https://github.com/garywelz/glmp/tree/main/tda-analysis
