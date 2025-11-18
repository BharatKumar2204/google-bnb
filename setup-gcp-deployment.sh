#!/bin/bash

# AI News App - Google Cloud Run Deployment Setup Script
# This script helps you set up everything needed for deployment

set -e

echo "=================================================="
echo "AI News App - GCP Deployment Setup"
echo "=================================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI is not installed${NC}"
    echo "Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo -e "${GREEN}✓ gcloud CLI found${NC}"

# Get project ID
echo ""
echo "Enter your Google Cloud Project ID:"
read -r PROJECT_ID

if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}Error: Project ID cannot be empty${NC}"
    exit 1
fi

# Set project
gcloud config set project "$PROJECT_ID"
echo -e "${GREEN}✓ Project set to: $PROJECT_ID${NC}"

# Enable APIs
echo ""
echo -e "${YELLOW}Enabling required APIs...${NC}"
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
echo -e "${GREEN}✓ APIs enabled${NC}"

# Note: Using Container Registry (gcr.io) - no need to create repository
echo ""
echo -e "${GREEN}✓ Container Registry ready (gcr.io)${NC}"

# Create Service Account
echo ""
echo -e "${YELLOW}Creating service account for GitHub Actions...${NC}"
gcloud iam service-accounts create github-actions \
  --display-name="GitHub Actions Deployer" || echo "Service account may already exist"

SA_EMAIL="github-actions@$PROJECT_ID.iam.gserviceaccount.com"

# Grant permissions
echo -e "${YELLOW}Granting permissions...${NC}"
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/run.admin" --quiet

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/artifactregistry.writer" --quiet

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/iam.serviceAccountUser" --quiet

echo -e "${GREEN}✓ Permissions granted${NC}"

# Create service account key
echo ""
echo -e "${YELLOW}Creating service account key...${NC}"
KEY_FILE="github-actions-key.json"
gcloud iam service-accounts keys create "$KEY_FILE" \
  --iam-account="$SA_EMAIL"
echo -e "${GREEN}✓ Key created: $KEY_FILE${NC}"

# Summary
echo ""
echo "=================================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=================================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Add these GitHub Secrets to your repository:"
echo "   Settings → Secrets and variables → Actions → New repository secret"
echo ""
echo "   GCP_SA_KEY:"
echo "   Copy the entire content of: $KEY_FILE"
echo ""
echo "   GCP_PROJECT_ID:"
echo "   $PROJECT_ID"
echo ""
echo "   GEMINI_API_KEY:"
echo "   Get from: https://makersuite.google.com/app/apikey"
echo ""
echo "2. Deploy backend first (manually or via GitHub Actions)"
echo ""
echo "3. Get backend URL and add as BACKEND_URL secret:"
echo "   gcloud run services describe ai-news-backend --region us-central1 --format 'value(status.url)'"
echo ""
echo "4. Deploy frontend (will use BACKEND_URL)"
echo ""
echo "=================================================="
echo ""
echo -e "${YELLOW}IMPORTANT: Keep $KEY_FILE secure and never commit it!${NC}"
echo ""
