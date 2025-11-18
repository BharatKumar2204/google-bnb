# Deployment Guide - Google Cloud Run

This guide will help you deploy the AI News Verification Platform to Google Cloud Run using GitHub Actions.

## Architecture

- **Frontend**: React + Vite → Nginx → Cloud Run
- **Backend**: FastAPI + Python → Cloud Run
- **CI/CD**: GitHub Actions
- **Container Registry**: Google Artifact Registry

## Prerequisites

1. Google Cloud Project with billing enabled
2. GitHub repository
3. Google Cloud credentials (Service Account)

## Step 1: Google Cloud Setup

### 1.1 Enable Required APIs

```bash
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 1.2 Create Artifact Registry Repository

```bash
gcloud artifacts repositories create ai-news \
  --repository-format=docker \
  --location=us-central1 \
  --description="AI News App containers"
```

### 1.3 Create Service Account

```bash
# Create service account
gcloud iam service-accounts create github-actions \
  --display-name="GitHub Actions Deployer"

# Get your project ID
export PROJECT_ID=$(gcloud config get-value project)

# Grant necessary permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

# Create and download key
gcloud iam service-accounts keys create github-actions-key.json \
  --iam-account=github-actions@$PROJECT_ID.iam.gserviceaccount.com
```

## Step 2: GitHub Secrets Setup

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add the following secrets:

### Required Secrets

1. **GCP_SA_KEY**
   - Content of `github-actions-key.json` file
   - Copy the entire JSON content

2. **GCP_PROJECT_ID**
   - Your Google Cloud Project ID
   - Example: `my-project-12345`

3. **GEMINI_API_KEY**
   - Your Google Gemini API key
   - Get from: https://makersuite.google.com/app/apikey

4. **BACKEND_URL** (will be set after first backend deployment)
   - Format: `https://ai-news-backend-xxxxx-uc.a.run.app`
   - Leave empty initially, update after first backend deploy

### Optional Secrets (if using)

5. **GOOGLE_SEARCH_API_KEY**
6. **GOOGLE_SEARCH_ENGINE_ID**

## Step 3: Deploy Backend First

### 3.1 Manual First Deployment

```bash
cd ai-news-app/mcp_server

# Build Docker image
docker build -t gcr.io/$PROJECT_ID/ai-news-backend:latest .

# Push to Container Registry
docker push gcr.io/$PROJECT_ID/ai-news-backend:latest

# Deploy to Cloud Run
gcloud run deploy ai-news-backend \
  --image gcr.io/$PROJECT_ID/ai-news-backend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "GEMINI_API_KEY=your-key,GCP_PROJECT_ID=$PROJECT_ID,MCP_SERVER_HOST=0.0.0.0,MCP_SERVER_PORT=8080" \
  --memory 2Gi \
  --cpu 2
```

### 3.2 Get Backend URL

```bash
gcloud run services describe ai-news-backend \
  --region us-central1 \
  --format 'value(status.url)'
```

Copy this URL and add it as `BACKEND_URL` secret in GitHub.

## Step 4: Deploy Frontend

### 4.1 Update GitHub Secret

Add the backend URL from Step 3.2 as `BACKEND_URL` secret.

### 4.2 Trigger Deployment

Push to main branch or manually trigger the workflow:

```bash
git add .
git commit -m "Deploy to Cloud Run"
git push origin main
```

Or use GitHub UI: Actions → Deploy Frontend to Cloud Run → Run workflow

## Step 5: Verify Deployment

### Backend Health Check

```bash
curl https://ai-news-backend-xxxxx-uc.a.run.app/health
```

Expected response:
```json
{
  "status": "✅ healthy",
  "service": "MCP Server v3.0",
  "root_agent": "Google ADK"
}
```

### Frontend Health Check

```bash
curl https://ai-news-frontend-xxxxx-uc.a.run.app/health
```

Expected response:
```
healthy
```

## Step 6: Configure Custom Domain (Optional)

### 6.1 Map Domain to Cloud Run

```bash
# Backend
gcloud run services update ai-news-backend \
  --region us-central1 \
  --add-custom-domain api.yourdomain.com

# Frontend
gcloud run services update ai-news-frontend \
  --region us-central1 \
  --add-custom-domain yourdomain.com
```

### 6.2 Update DNS Records

Follow the instructions provided by Cloud Run to add DNS records.

### 6.3 Update BACKEND_URL Secret

Update the `BACKEND_URL` secret to use your custom domain:
```
https://api.yourdomain.com
```

## Workflow Triggers

### Automatic Deployment

- **Backend**: Triggers on changes to `mcp_server/**` or workflow file
- **Frontend**: Triggers on changes to `frontend/**` or workflow file

### Manual Deployment

Go to: Actions → Select workflow → Run workflow

## Environment Variables

### Backend (Cloud Run)

Set via GitHub secrets or Cloud Run console:

```env
GEMINI_API_KEY=your-gemini-api-key
GCP_PROJECT_ID=your-project-id
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8080
DEBUG=False
```

### Frontend (Build time)

Set via GitHub secrets:

```env
VITE_API_URL=https://ai-news-backend-xxxxx-uc.a.run.app
```

## Monitoring & Logs

### View Logs

```bash
# Backend logs
gcloud run services logs read ai-news-backend --region us-central1

# Frontend logs
gcloud run services logs read ai-news-frontend --region us-central1
```

### Cloud Console

Visit: https://console.cloud.google.com/run

## Cost Optimization

### Cloud Run Pricing

- **Free tier**: 2 million requests/month
- **Pay per use**: Only charged when serving requests
- **Min instances**: Set to 0 to avoid idle costs

### Recommended Settings

**Backend:**
- Memory: 2Gi
- CPU: 2
- Min instances: 0
- Max instances: 10
- Timeout: 300s

**Frontend:**
- Memory: 512Mi
- CPU: 1
- Min instances: 0
- Max instances: 5
- Timeout: 60s

## Troubleshooting

### Build Fails

**Issue**: Docker build fails
- Check Dockerfile syntax
- Verify all dependencies in requirements.txt/package.json
- Check build logs in GitHub Actions

### Deployment Fails

**Issue**: Cloud Run deployment fails
- Verify service account permissions
- Check GCP_SA_KEY secret is valid JSON
- Ensure APIs are enabled

### Backend Not Responding

**Issue**: 502/503 errors
- Check backend logs: `gcloud run services logs read ai-news-backend`
- Verify GEMINI_API_KEY is set correctly
- Check memory/CPU limits

### Frontend Can't Connect to Backend

**Issue**: CORS or connection errors
- Verify BACKEND_URL is correct
- Check backend is deployed and healthy
- Verify CORS settings in backend

## Rollback

### Rollback to Previous Revision

```bash
# List revisions
gcloud run revisions list --service ai-news-backend --region us-central1

# Rollback
gcloud run services update-traffic ai-news-backend \
  --region us-central1 \
  --to-revisions REVISION-NAME=100
```

## Security Best Practices

1. **Never commit credentials**
   - Use GitHub Secrets
   - Add credentials.json to .gitignore

2. **Use least privilege**
   - Service account has only required permissions
   - Review IAM roles regularly

3. **Enable authentication** (if needed)
   - Remove `--allow-unauthenticated` flag
   - Use Cloud IAM for access control

4. **Rotate secrets regularly**
   - Update API keys periodically
   - Regenerate service account keys

## Continuous Deployment

The workflows are configured for automatic deployment:

1. Push to `main` branch
2. GitHub Actions triggers
3. Builds Docker image
4. Pushes to Artifact Registry
5. Deploys to Cloud Run
6. Service URL available

## Support

For issues:
1. Check GitHub Actions logs
2. Check Cloud Run logs
3. Verify all secrets are set correctly
4. Review this guide

## Next Steps

After successful deployment:

1. Test all features
2. Set up monitoring alerts
3. Configure custom domain
4. Set up Cloud CDN (optional)
5. Enable Cloud Armor (optional)
6. Set up backup strategy

---

**Deployment Complete! 🚀**

Your AI News Verification Platform is now running on Google Cloud Run with automatic CI/CD via GitHub Actions.
