@echo off
REM GLMP Batch 9 - one-click GCS deploy for Windows (Yoga 9i)
REM Uses your service account key in Downloads and deploys viewer + 217 processes + database table.

setlocal EnableDelayedExpansion
set KEY_FILE=%USERPROFILE%\Downloads\regal-scholar-453620-r7-b66204f047cc.json
set REPO_DIR=%USERPROFILE%\glmp
set PROJECT=regal-scholar-453620-r7
set BRANCH=main

echo.
echo === GLMP Batch 9 Deploy (Windows) ===
echo.

if not exist "%KEY_FILE%" (
    echo ERROR: Key file not found:
    echo   %KEY_FILE%
    echo Put your JSON key in Downloads or edit KEY_FILE in this script.
    pause
    exit /b 1
)
echo OK: Found key file

where gcloud >nul 2>&1
if errorlevel 1 (
    echo ERROR: gcloud not found. Install Google Cloud SDK:
    echo   https://cloud.google.com/sdk/docs/install
    pause
    exit /b 1
)
echo OK: gcloud found

if not exist "%REPO_DIR%\.git" (
    echo Cloning glmp to %REPO_DIR% ...
    git clone https://github.com/garywelz/glmp.git "%REPO_DIR%"
)
cd /d "%REPO_DIR%"

echo Fetching branch %BRANCH% ...
git fetch origin %BRANCH%
git checkout %BRANCH%
git pull origin %BRANCH%

echo Authenticating...
gcloud auth activate-service-account --key-file="%KEY_FILE%"
gcloud config set project %PROJECT%

echo Running deploy via Git Bash...
where bash >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git Bash not found. Install Git for Windows, then re-run.
    pause
    exit /b 1
)
bash DEPLOY_BATCH9_ALL.sh
if errorlevel 1 (
    echo.
    echo Deploy failed. Try manually from Git Bash:
    echo   cd /c/Users/garyw/glmp
    echo   git checkout main
    echo   bash DEPLOY_BATCH9_ALL.sh
    pause
    exit /b 1
)

echo.
echo === DONE ===
echo Viewer: https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-v2/viewer/index.html
echo Table:  https://storage.googleapis.com/regal-scholar-453620-r7-podcast-storage/glmp-database-table.html
echo.
pause
