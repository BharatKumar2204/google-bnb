@echo off
REM AI News App - Google Cloud Run Deployment Setup Script (Windows)
REM This script helps you set up everything needed for deployment

echo ==================================================
echo AI News App - GCP Deployment Setup
echo ==================================================
echo.

REM Check if gcloud is installed
where gcloud >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: gcloud CLI is not installed
    echo Install from: https://cloud.google.com/sdk/docs/install
    exit /b 1
)

echo [OK] gcloud CLI found
echo.

REM Get project ID
set /p PROJECT_ID="Enter your Google Cloud Project ID: "

if "%PROJECT_ID%"=="" (
    echo Error: Project ID cannot be empty
    exit /b 1
)

REM Set project
gcloud config set project %PROJECT_ID%
echo [OK] Project set to: %PROJECT_ID%
echo.

REM Enable APIs
echo Enabling required APIs...
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
echo [OK] APIs enabled
echo.

REM Create Artifact Registry
echo Creating Artifact Registry repository...
gcloud artifacts repositories create ai-news --repository-format=docker --location=us-central1 --description="AI News App containers" 2>nul || echo Repository may already exist
echo [OK] Artifact Registry ready
echo.

REM Create Service Account
echo Creating service account for GitHub Actions...
gcloud iam service-accounts create github-actions --display-name="GitHub Actions Deployer" 2>nul || echo Service account may already exist

set SA_EMAIL=github-actions@%PROJECT_ID%.iam.gserviceaccount.com

REM Grant permissions
echo Granting permissions...
gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:%SA_EMAIL%" --role="roles/run.admin" --quiet
gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:%SA_EMAIL%" --role="roles/artifactregistry.writer" --quiet
gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:%SA_EMAIL%" --role="roles/iam.serviceAccountUser" --quiet
echo [OK] Permissions granted
echo.

REM Create service account key
echo Creating service account key...
set KEY_FILE=github-actions-key.json
gcloud iam service-accounts keys create %KEY_FILE% --iam-account=%SA_EMAIL%
echo [OK] Key created: %KEY_FILE%
echo.

REM Summary
echo ==================================================
echo Setup Complete!
echo ==================================================
echo.
echo Next steps:
echo.
echo 1. Add these GitHub Secrets to your repository:
echo    Settings -^> Secrets and variables -^> Actions -^> New repository secret
echo.
echo    GCP_SA_KEY:
echo    Copy the entire content of: %KEY_FILE%
echo.
echo    GCP_PROJECT_ID:
echo    %PROJECT_ID%
echo.
echo    GEMINI_API_KEY:
echo    Get from: https://makersuite.google.com/app/apikey
echo.
echo 2. Deploy backend first (manually or via GitHub Actions)
echo.
echo 3. Get backend URL and add as BACKEND_URL secret:
echo    gcloud run services describe ai-news-backend --region us-central1 --format "value(status.url)"
echo.
echo 4. Deploy frontend (will use BACKEND_URL)
echo.
echo ==================================================
echo.
echo IMPORTANT: Keep %KEY_FILE% secure and never commit it!
echo.
pause
