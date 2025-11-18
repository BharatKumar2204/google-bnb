# Cloud Run Deployment Guide

This guide walks you through deploying the AI News Platform to Google Cloud Run using GitHub Actions.

## Prerequisites

1. **Google Cloud Account** with billing enabled
2. **GitHub Repository** with your code
3. **Google Cloud Project** created
4. **Gemini API Key** from Google AI Studio

## Step 1: Set Up Google Cloud

### 1.1 Enable Required APIs

```bash
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 1.2 Create Service Account

```bash
gcloud iam service-accounts create github-actions \
    --display-name="GitHub Actions Deployer"
```

### 1.3 Grant Permissions

```bash
# Get your project ID
PROJECT_ID=$(gcloud config get-value project)

# Grant necessary roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"
```

### 1.4 Create Service Account Key

```bash
gcloud iam service-accounts keys create key.json \
    --iam-account=github-actions@$PROJECT_ID.iam.gserviceaccount.com
```

This creates a `key.json` file. Keep it secure!

## Step 2: Configure GitHub Secrets

Go to your GitHub repository:
1. Click **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add these secrets:

| Secret Name | Value | How to Get |
|------------|-------|------------|
| `GCP_SA_KEY` | Contents of `key.json` file | Copy entire JSON content |
| `GCP_PROJECT_ID` | Your GCP project ID | Run `gcloud config get-value project` |
| `GEMINI_API_KEY` | Your Gemini API key | Get from [Google AI Studio](https://makersuite.google.com/app/apikey) |
| `BACKEND_URL` | Backend Cloud Run URL | Leave empty initially, update after first backend deploy |

### Getting Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click **Get API Key**
3. Create or select a project
4. Copy the API key

## Step 3: Deploy Backend

### Option A: Automatic Deployment

Push to main branch:
```bash
git add .
git commit -m "Deploy backend"
git push origin main
```

The workflow triggers automatically when `mcp_server/**` files change.

### Option B: Manual Deployment

1. Go to GitHub → **Actions** tab
2. Select **Deploy Backend to Cloud Run**
3. Click **Run workflow**
4. Select `main` branch
5. Click **Run workflow**

### Monitor Deployment

1. Watch the workflow progress in Actions tab
2. Wait for completion (usually 3-5 minutes)
3. Check the logs for the backend URL
4. Copy the URL (looks like: `https://ai-news-backend-xxx-uc.a.run.app`)

## Step 4: Update Backend URL Secret

1. Go to GitHub → **Settings** → **Secrets and variables** → **Actions**
2. Click on `BACKEND_URL` secret (or create if doesn't exist)
3. Paste the backend Cloud Run URL from Step 3
4. Click **Update secret**

## Step 5: Deploy Frontend

### Option A: Automatic Deployment

Push to main branch:
```bash
git add .
git commit -m "Deploy frontend"
git push origin main
```

The workflow triggers automatically when `frontend/**` files change.

### Option B: Manual Deployment

1. Go to GitHub → **Actions** tab
2. Select **Deploy Frontend to Cloud Run**
3. Click **Run workflow**
4. Select `main` branch
5. Click **Run workflow**

### Monitor Deployment

1. Watch the workflow progress in Actions tab
2. Wait for completion (usually 2-4 minutes)
3. Check the logs for the frontend URL
4. Copy the URL (looks like: `https://ai-news-frontend-xxx-uc.a.run.app`)

## Step 6: Test Your Deployment

1. Open the frontend URL in your browser
2. Test each feature:
   - Trending News
   - Quick Summary
   - Text Analysis
   - Location News (map)

## Troubleshooting

### Workflow Fails at Authentication

**Error:** `Failed to authenticate to Google Cloud`

**Solution:**
- Verify `GCP_SA_KEY` secret contains valid JSON
- Check service account exists: `gcloud iam service-accounts list`
- Ensure key hasn't expired

### Workflow Fails at Build

**Error:** `Docker build failed`

**Solution:**
- Check Dockerfile syntax
- Verify all dependencies in requirements.txt/package.json
- Review build logs in Actions tab

### Workflow Fails at Deploy

**Error:** `Permission denied` or `Cloud Run API not enabled`

**Solution:**
```bash
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Verify service account permissions
gcloud projects get-iam-policy $PROJECT_ID \
    --flatten="bindings[].members" \
    --filter="bindings.members:serviceAccount:github-actions@*"
```

### Backend Deploys but Returns 500 Error

**Solution:**
- Check Cloud Run logs: `gcloud run services logs read ai-news-backend --region us-central1`
- Verify `GEMINI_API_KEY` is set correctly
- Check environment variables in Cloud Run console

### Frontend Shows "Cannot connect to backend"

**Solution:**
- Verify `BACKEND_URL` secret is set correctly
- Check backend is deployed and running
- Verify CORS is enabled in backend
- Check browser console for errors

## Monitoring and Logs

### View Cloud Run Logs

```bash
# Backend logs
gcloud run services logs read ai-news-backend --region us-central1 --limit 50

# Frontend logs
gcloud run services logs read ai-news-frontend --region us-central1 --limit 50
```

### View in Console

1. Go to [Cloud Run Console](https://console.cloud.google.com/run)
2. Click on service name
3. Click **Logs** tab
4. Filter by severity or search text

## Cost Estimation

### Cloud Run Pricing (us-central1)

**Backend:**
- Memory: 2GB × $0.0000025/GB-second
- CPU: 2 vCPU × $0.00002400/vCPU-second
- Requests: $0.40 per million requests
- Estimated: ~$5-20/month for moderate traffic

**Frontend:**
- Memory: 512MB × $0.0000025/GB-second
- CPU: 1 vCPU × $0.00002400/vCPU-second
- Requests: $0.40 per million requests
- Estimated: ~$2-10/month for moderate traffic

**Free Tier:**
- 2 million requests/month
- 360,000 GB-seconds/month
- 180,000 vCPU-seconds/month

## Updating Your Deployment

### Update Backend

1. Make changes to `mcp_server/**` files
2. Commit and push to main branch
3. Workflow runs automatically

### Update Frontend

1. Make changes to `frontend/**` files
2. Commit and push to main branch
3. Workflow runs automatically

### Update Environment Variables

```bash
# Update backend env vars
gcloud run services update ai-news-backend \
    --region us-central1 \
    --set-env-vars "NEW_VAR=value"

# Update frontend (requires rebuild)
# Update BACKEND_URL secret in GitHub and redeploy
```

## Rollback

### Rollback to Previous Revision

```bash
# List revisions
gcloud run revisions list --service ai-news-backend --region us-central1

# Rollback to specific revision
gcloud run services update-traffic ai-news-backend \
    --region us-central1 \
    --to-revisions REVISION_NAME=100
```

## Custom Domain (Optional)

### Map Custom Domain

```bash
# Map domain to service
gcloud run domain-mappings create \
    --service ai-news-frontend \
    --domain your-domain.com \
    --region us-central1
```

Follow the instructions to update DNS records.

## Security Best Practices

1. **Rotate secrets regularly** - Update service account keys every 90 days
2. **Use least privilege** - Only grant necessary permissions
3. **Enable VPC** - For production, use VPC connector
4. **Set up monitoring** - Configure Cloud Monitoring alerts
5. **Use Secret Manager** - For production, migrate to Secret Manager

## Next Steps

- [ ] Set up custom domain
- [ ] Configure Cloud CDN for frontend
- [ ] Set up Cloud Monitoring alerts
- [ ] Enable Cloud Armor for DDoS protection
- [ ] Set up staging environment
- [ ] Configure backup and disaster recovery

## Support

For issues:
1. Check workflow logs in GitHub Actions
2. Review Cloud Run logs
3. Verify all secrets are set correctly
4. Check [Troubleshooting](#troubleshooting) section

---

**Your AI News Platform is now live on Cloud Run!** 🚀
