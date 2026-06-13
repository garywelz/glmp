# GLMP Batch 9 - one-click GCS deploy for Windows (PowerShell)
# Double-click or: powershell -ExecutionPolicy Bypass -File DEPLOY_BATCH9_WINDOWS.ps1

$ErrorActionPreference = "Stop"
$KeyFile  = "$env:USERPROFILE\Downloads\regal-scholar-453620-r7-b66204f047cc.json"
$RepoDir  = "$env:USERPROFILE\glmp"
$Project  = "regal-scholar-453620-r7"
$Branch   = "cursor/batch-9-ground-truth-c7ff"

Write-Host "`n=== GLMP Batch 9 Deploy (Windows) ===`n"

if (-not (Test-Path $KeyFile)) {
    Write-Host "ERROR: Key not found: $KeyFile"
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "OK: Key file found"

$gcloud = Get-Command gcloud -ErrorAction SilentlyContinue
if (-not $gcloud) {
    Write-Host "ERROR: gcloud not installed. Get it from:"
    Write-Host "  https://cloud.google.com/sdk/docs/install"
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "OK: gcloud found"

if (-not (Test-Path "$RepoDir\.git")) {
    Write-Host "Cloning glmp..."
    git clone https://github.com/garywelz/glmp.git $RepoDir
}
Set-Location $RepoDir

git fetch origin $Branch
git checkout $Branch
git pull origin $Branch

Write-Host "Authenticating..."
& gcloud auth activate-service-account --key-file=$KeyFile
& gcloud config set project $Project

Write-Host "Deploying..."
# Git Bash runs the bash deploy script reliably on Windows
$bash = Get-Command bash -ErrorAction SilentlyContinue
if ($bash) {
    & bash ./DEPLOY_BATCH9_ALL.sh
} else {
    Write-Host "Git Bash not found. Install Git for Windows, then re-run."
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "`n=== DONE ==="
Write-Host "Viewer: https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html"
Write-Host "Table:  https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-database-table.html"
Read-Host "`nPress Enter to close"
