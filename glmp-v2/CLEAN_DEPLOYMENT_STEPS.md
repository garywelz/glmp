# GLMP v2 - Clean Deployment Steps

## Step-by-Step Instructions (Clean Start)

---

## Step 1: Clean Up Any Existing Clone

```bash
# Remove any existing clones to start fresh
cd ~
rm -rf glmp glmp-clean glmp-project

# Verify cleanup
ls -la | grep glmp
# Should show nothing (or only your original ~/glmp directory if you want to keep it)
```

---

## Step 2: Clone Fresh

```bash
# Clone to a clean new directory
git clone https://github.com/garywelz/glmp.git glmp-clean

# Navigate into it
cd glmp-clean

# Switch to the clean-slate branch
git checkout clean-slate-v2-viewer-system

# Navigate to the v2 directory
cd glmp-v2

# Verify you're in the right place
pwd
# Should show: /home/gdubs/glmp-clean/glmp-v2

ls -la
# Should show:
#   viewer/
#   processes/
#   data/
#   DEPLOY_TO_GCS.sh
#   README.md
#   and other docs
```

---

## Step 3: Authenticate with Google Cloud

```bash
# Activate your service account
gcloud auth activate-service-account --key-file=/path/to/your-service-account-key.json

# Example:
# gcloud auth activate-service-account --key-file=/home/gdubs/keys/regal-scholar-key.json

# Set the project
gcloud config set project regal-scholar-453620-r7

# Verify authentication
gcloud auth list
# Should show your service account as ACTIVE
```

---

## Step 4: Deploy to GCS

```bash
# Make sure you're in the glmp-v2 directory
pwd
# Should show: /home/gdubs/glmp-clean/glmp-v2

# Run the deployment script
./DEPLOY_TO_GCS.sh
```

The script will:
- ✅ Verify authentication
- ✅ Upload viewer files
- ✅ Upload process files
- ✅ Upload data files
- ✅ Set public permissions
- ✅ Configure cache headers
- ✅ Display your live URLs

**Time: ~2-3 minutes**

---

## Step 5: Verify Deployment

After deployment completes, test these URLs in your browser:

**Main Viewer:**
```
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html
```

**Individual Processes:**
```
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_lac_operon

https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html?process=ecoli_dna_replication_initiation
```

---

## Complete Command Summary (Copy & Paste)

```bash
# Step 1: Clean up
cd ~
rm -rf glmp-clean

# Step 2: Clone fresh
git clone https://github.com/garywelz/glmp.git glmp-clean
cd glmp-clean
git checkout clean-slate-v2-viewer-system
cd glmp-v2

# Step 3: Authenticate (replace with your actual key path)
gcloud auth activate-service-account --key-file=/path/to/your-key.json
gcloud config set project regal-scholar-453620-r7

# Step 4: Deploy
./DEPLOY_TO_GCS.sh
```

---

## Troubleshooting

### If you get "Permission denied" on the script:
```bash
chmod +x DEPLOY_TO_GCS.sh
./DEPLOY_TO_GCS.sh
```

### If you get authentication errors:
```bash
# Check which account is active
gcloud auth list

# Re-authenticate
gcloud auth activate-service-account --key-file=/path/to/your-key.json
```

### If the script fails partway through:
```bash
# Just re-run it - it's safe to run multiple times
./DEPLOY_TO_GCS.sh
```

---

## After Successful Deployment

You'll see output like:

```
╔══════════════════════════════════════════════════════════╗
║              ✓ Deployment Complete!                      ║
╚══════════════════════════════════════════════════════════╝

Your GLMP v2 Viewer is now live at:
https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html
```

**Test the URL immediately to verify!**

---

## Questions?

- Files missing? Make sure you're in `/glmp-clean/glmp-v2/`
- Authentication failing? Check your service account key path
- Deployment failing? Make sure you have write permissions to the bucket

---

**Ready? Run the commands above and you'll be live in 3 minutes!** 🚀
