@echo off
REM GLMP Batch 9 - one-click GCS deploy for Windows (Yoga 9i)
REM Uses your service account key in Downloads and deploys viewer + 217 processes + database table.

setlocal EnableDelayedExpansion
set KEY_FILE=%USERPROFILE%\Downloads\regal-scholar-453620-r7-b66204f047cc.json
set REPO_DIR=%USERPROFILE%\glmp
set PROJECT=regal-scholar-453620-r7
set BRANCH=cursor/batch-9-ground-truth-c7ff

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

echo Running deploy...
call DEPLOY_BATCH9_ALL.sh
if errorlevel 1 (
    echo.
    echo If DEPLOY_BATCH9_ALL.sh failed on Windows, run from Git Bash:
    echo   cd %%USERPROFILE%%\glmp
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
