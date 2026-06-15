# GLMP full deploy — native PowerShell (no Git Bash gcloud)
# Run: powershell -ExecutionPolicy Bypass -File DEPLOY_BATCH9_POWERSHELL.ps1

$ErrorActionPreference = "Stop"
$RepoDir = "$env:USERPROFILE\glmp"
$KeyFile = "$env:USERPROFILE\Downloads\regal-scholar-453620-r7-b66204f047cc.json"
$Bucket  = "regal-scholar-453620-r7-podcast-storage"
$Project = "regal-scholar-453620-r7"
$GcsPath = "glmp-v2"

Set-Location $RepoDir
Write-Host "`n=== GLMP Deploy (PowerShell native) ===`n"
Write-Host "Repo: $RepoDir"
Write-Host "Branch: $(git branch --show-current)"

if (-not (Test-Path $KeyFile)) {
    Write-Host "ERROR: Key not found: $KeyFile"
    exit 1
}

& gcloud.cmd auth activate-service-account --key-file=$KeyFile
& gcloud.cmd config set project $Project
Write-Host "Authenticated as: $(& gcloud.cmd auth list --filter=status:ACTIVE --format='value(account)' | Select-Object -First 1)"

Set-Location "$RepoDir\glmp-v2"
Write-Host "`n[1/4] Uploading viewer..."
& gsutil.cmd -m cp -r viewer/* "gs://$Bucket/$GcsPath/viewer/"

Write-Host "`n[2/4] Uploading processes..."
& gsutil.cmd -m cp -r processes/* "gs://$Bucket/$GcsPath/processes/"

Write-Host "`n[3/4] Uploading data..."
& gsutil.cmd -m cp -r data/* "gs://$Bucket/$GcsPath/data/"
& gsutil.cmd cp data/metadata.json "gs://$Bucket/$GcsPath/metadata.json"

Set-Location $RepoDir
Write-Host "`n[4/4] Uploading database table..."
& gsutil.cmd cp glmp-database-table.html "gs://$Bucket/glmp-database-table.html"
& gsutil.cmd setmeta -h "Cache-Control:no-cache, no-store, must-revalidate" "gs://$Bucket/glmp-database-table.html"

Write-Host "`n=== DONE ==="
Write-Host "Viewer: https://storage.googleapis.com/$Bucket/$GcsPath/viewer/index.html"
Write-Host "Table:  https://storage.googleapis.com/$Bucket/glmp-database-table.html"
Write-Host "Test:   https://storage.googleapis.com/$Bucket/$GcsPath/viewer/index.html?process=human_tlr4_lps_amplification"
