# Deployment Checklist

Use this checklist to ensure a smooth deployment to Google Cloud Run.

## Pre-Deployment

### Google Cloud Setup
- [ ] Google Cloud account created
- [ ] Billing enabled on project
- [ ] gcloud CLI installed
- [ ] Authenticated with gcloud (`gcloud auth login`)
- [ ] Project selected (`gcloud config set project PROJECT_ID`)

### GitHub Setup
- [ ] Code pushed to GitHub repository
- [ ] Repository is accessible
- [ ] GitHub Actions enabled

## Initial Setup (One-time)

### Run Setup Script
- [ ] Navigate to `ai-news-app` directory
- [ ] Run setup script:
  - Windows: `setup-gcp-deployment.bat`
  - Linux/Mac: `./setup-gcp-deployment.sh`
- [ ] Script completed successfully
- [ ] `github-actions-key.json` file created

### Google Cloud APIs
- [ ] Cloud Run API enabled
- [ ] Artifact Registry API enabled
- [ ] Cloud Build API enabled

### Artifact Registry
- [ ] Repository `ai-news` created
- [ ] Location: `us-central1`
- [ ] Format: Docker

### Service Account
- [ ] Service account `github-actions` created
- [ ] Role: `roles/run.admin` granted
- [ ] Role: `roles/artifactregistry.writer` granted
- [ ] Role: `roles/iam.serviceAccountUser` granted
- [ ] Service account key downloaded

## GitHub Secrets Configuration

### Required Secrets
- [ ] `GCP_SA_KEY` added (content of `github-actions-key.json`)
- [ ] `GCP_PROJECT_ID` added (your project ID)
- [ ] `GEMINI_API_KEY` added (from Google AI Studio)
- [ ] `BACKEND_URL` placeholder created (will update after backend deploy)

### Optional Secrets (if using)
- [ ] `GOOGLE_SEARCH_API_KEY` added
- [ ] `GOOGLE_SEARCH_ENGINE_ID` added

## Backend Deployment

### Pre-deployment Checks
- [ ] `mcp_server/Dockerfile` exists
- [ ] `mcp_server/requirements.txt` is up to date
- [ ] `mcp_server/.dockerignore` configured
- [ ] Environment variables reviewed

### Deploy Backend
- [ ] Code committed and pushed to main branch
- [ ] GitHub Actions workflow triggered
- [ ] Workflow completed successfully
- [ ] No errors in workflow logs

### Verify Backend
- [ ] Backend service deployed to Cloud Run
- [ ] Service URL obtained
- [ ] Health check passes:
  ```bash
  curl https://ai-news-backend-xxxxx-uc.a.run.app/health
  ```
- [ ] API endpoints responding correctly

### Update GitHub Secrets
- [ ] `BACKEND_URL` secret updated with actual backend URL

## Frontend Deployment

### Pre-deployment Checks
- [ ] `frontend/Dockerfile` exists
- [ ] `frontend/nginx.conf` configured
- [ ] `frontend/.dockerignore` configured
- [ ] `BACKEND_URL` secret is set correctly

### Deploy Frontend
- [ ] Code committed and pushed to main branch
- [ ] GitHub Actions workflow triggered
- [ ] Workflow completed successfully
- [ ] No errors in workflow logs

### Verify Frontend
- [ ] Frontend service deployed to Cloud Run
- [ ] Service URL obtained
- [ ] Health check passes:
  ```bash
  curl https://ai-news-frontend-xxxxx-uc.a.run.app/health
  ```
- [ ] Website loads in browser
- [ ] Can connect to backend API

## Post-Deployment Testing

### Backend Tests
- [ ] `/health` endpoint returns healthy status
- [ ] `/` endpoint returns API info
- [ ] `/agents/news_fetch` endpoint works
- [ ] `/agents/truth_verification` endpoint works
- [ ] `/agents/summary_context` endpoint works
- [ ] `/agents/map_intelligence` endpoint works
- [ ] Gemini AI integration working
- [ ] No errors in Cloud Run logs

### Frontend Tests
- [ ] Homepage loads correctly
- [ ] Trending News tab works
- [ ] Quick Summary tab works
- [ ] Text Analysis tab works
- [ ] Location News tab works
- [ ] Map displays correctly
- [ ] API calls to backend succeed
- [ ] No console errors

### Integration Tests
- [ ] Frontend can fetch news from backend
- [ ] AI analysis features work
- [ ] Location-based search works
- [ ] All tabs functional
- [ ] Error handling works properly

## Security Verification

### Credentials
- [ ] `credentials.json` NOT in repository
- [ ] `credentials.json` in `.gitignore`
- [ ] `.env` files NOT in repository
- [ ] `.env` files in `.gitignore`
- [ ] `github-actions-key.json` stored securely
- [ ] All secrets in GitHub Secrets (not in code)

### Service Configuration
- [ ] Backend uses non-root user
- [ ] Frontend uses non-root user
- [ ] HTTPS enforced (automatic with Cloud Run)
- [ ] CORS configured correctly
- [ ] Security headers configured in Nginx

## Monitoring Setup

### Cloud Run Monitoring
- [ ] Cloud Run dashboard accessible
- [ ] Metrics visible (requests, latency, errors)
- [ ] Logs accessible and readable
- [ ] No unexpected errors in logs

### Alerts (Optional)
- [ ] Error rate alert configured
- [ ] Latency alert configured
- [ ] Cost alert configured

## Documentation

### Update Documentation
- [ ] Service URLs documented
- [ ] Deployment date recorded
- [ ] Any custom configurations documented
- [ ] Team members notified

## Optimization (Optional)

### Performance
- [ ] Cloud CDN enabled (if needed)
- [ ] Custom domain configured (if needed)
- [ ] SSL certificate configured (if custom domain)

### Cost Optimization
- [ ] Min instances set to 0 (for cost savings)
- [ ] Max instances configured appropriately
- [ ] Memory/CPU settings optimized
- [ ] Timeout values appropriate

### Advanced Features
- [ ] Cloud Armor configured (if needed)
- [ ] VPC connector configured (if needed)
- [ ] Secret Manager integration (if needed)
- [ ] Cloud SQL connection (if needed)

## Continuous Deployment

### Workflow Verification
- [ ] Backend workflow triggers on `mcp_server/**` changes
- [ ] Frontend workflow triggers on `frontend/**` changes
- [ ] Manual workflow dispatch works
- [ ] Workflows complete in reasonable time

### Testing
- [ ] Make a small change to backend
- [ ] Verify auto-deployment works
- [ ] Make a small change to frontend
- [ ] Verify auto-deployment works

## Rollback Plan

### Preparation
- [ ] Know how to list revisions:
  ```bash
  gcloud run revisions list --service SERVICE_NAME --region us-central1
  ```
- [ ] Know how to rollback:
  ```bash
  gcloud run services update-traffic SERVICE_NAME --to-revisions REVISION=100
  ```
- [ ] Tested rollback procedure (optional)

## Final Verification

### Smoke Tests
- [ ] All features work end-to-end
- [ ] Performance is acceptable
- [ ] No errors in production
- [ ] Users can access the application

### Documentation
- [ ] Deployment documented
- [ ] Service URLs shared with team
- [ ] Access instructions provided
- [ ] Support contacts documented

## Cleanup (if needed)

### Remove Test Resources
- [ ] Test deployments deleted
- [ ] Unused service account keys revoked
- [ ] Temporary files removed
- [ ] Local credentials secured

---

## Quick Reference

### Service URLs
- Backend: `https://ai-news-backend-xxxxx-uc.a.run.app`
- Frontend: `https://ai-news-frontend-xxxxx-uc.a.run.app`

### Important Commands
```bash
# View logs
gcloud run services logs read SERVICE_NAME --region us-central1

# Describe service
gcloud run services describe SERVICE_NAME --region us-central1

# List services
gcloud run services list --region us-central1

# Update service
gcloud run services update SERVICE_NAME --region us-central1 [OPTIONS]
```

### Support
- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [Quick Deploy](QUICK_DEPLOY.md)
- [Deployment Summary](DEPLOYMENT_SUMMARY.md)

---

**Deployment Status**: ⬜ Not Started | 🟡 In Progress | ✅ Complete

**Last Updated**: _________________

**Deployed By**: _________________

**Notes**: _________________
