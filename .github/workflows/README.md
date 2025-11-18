# GitHub Actions Workflows

This directory contains automated CI/CD workflows for deploying to Google Cloud Run.

## Workflows

### 1. deploy-backend.yml

**Triggers:**
- Push to `main` branch with changes in `mcp_server/**`
- Manual workflow dispatch

**Steps:**
1. Checkout code
2. Authenticate with Google Cloud
3. Build Docker image (Python + FastAPI)
4. Push to Artifact Registry
5. Deploy to Cloud Run
6. Output service URL

**Environment Variables:**
- `GEMINI_API_KEY` - From GitHub secret
- `GCP_PROJECT_ID` - From GitHub secret
- `MCP_SERVER_HOST` - Set to 0.0.0.0
- `MCP_SERVER_PORT` - Set to 8080
- `DEBUG` - Set to False

**Service Configuration:**
- Memory: 2Gi
- CPU: 2 cores
- Timeout: 300s
- Max instances: 10
- Min instances: 0

### 2. deploy-frontend.yml

**Triggers:**
- Push to `main` branch with changes in `frontend/**`
- Manual workflow dispatch

**Steps:**
1. Checkout code
2. Authenticate with Google Cloud
3. Build Docker image (React + Nginx)
4. Push to Artifact Registry
5. Deploy to Cloud Run
6. Output service URL

**Build Arguments:**
- `VITE_API_URL` - Backend URL from GitHub secret

**Service Configuration:**
- Memory: 512Mi
- CPU: 1 core
- Timeout: 60s
- Max instances: 5
- Min instances: 0

## Required GitHub Secrets

| Secret | Description | Example |
|--------|-------------|---------|
| `GCP_SA_KEY` | Service account JSON key | `{"type": "service_account"...}` |
| `GCP_PROJECT_ID` | Google Cloud project ID | `my-project-12345` |
| `GEMINI_API_KEY` | Gemini AI API key | `AIzaSy...` |
| `BACKEND_URL` | Backend service URL | `https://ai-news-backend-xxx.run.app` |

## Manual Workflow Dispatch

To manually trigger a deployment:

1. Go to **Actions** tab in GitHub
2. Select the workflow (Deploy Backend or Deploy Frontend)
3. Click **Run workflow**
4. Select branch (usually `main`)
5. Click **Run workflow** button

## Workflow Status

View workflow runs:
- GitHub → Actions tab
- See all runs, logs, and status
- Download artifacts if needed

## Troubleshooting

### Workflow Fails at Authentication
- Verify `GCP_SA_KEY` secret is valid JSON
- Check service account has required permissions
- Ensure APIs are enabled in GCP

### Workflow Fails at Build
- Check Dockerfile syntax
- Verify all dependencies are listed
- Review build logs in Actions tab

### Workflow Fails at Deploy
- Verify service account has `roles/run.admin`
- Check Cloud Run API is enabled
- Ensure region is correct (us-central1)

## Monitoring Workflows

### View Logs
1. Go to Actions tab
2. Click on workflow run
3. Click on job name
4. Expand steps to see logs

### Notifications
Configure in: Settings → Notifications
- Email notifications for failed workflows
- Slack/Discord webhooks (optional)

## Workflow Optimization

### Caching
Both workflows use Docker layer caching for faster builds.

### Parallel Execution
Backend and frontend workflows run independently and can execute in parallel.

### Conditional Execution
Workflows only trigger when relevant files change:
- Backend: `mcp_server/**`
- Frontend: `frontend/**`

## Security

### Secrets Management
- Never commit secrets to repository
- Use GitHub Secrets for sensitive data
- Rotate secrets regularly

### Service Account Permissions
Least privilege principle:
- `roles/run.admin` - Deploy to Cloud Run
- `roles/artifactregistry.writer` - Push images
- `roles/iam.serviceAccountUser` - Use service account

## Cost Optimization

### Workflow Minutes
- GitHub Actions: 2,000 minutes/month free (public repos)
- Private repos: 2,000 minutes/month on free plan

### Cloud Run
- Only charged when serving requests
- Min instances: 0 (no idle cost)
- Auto-scales based on traffic

## Next Steps

1. Set up branch protection rules
2. Add testing stage before deployment
3. Create staging environment
4. Set up deployment approvals
5. Configure monitoring alerts

## Support

For issues:
1. Check workflow logs in Actions tab
2. Review [DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md)
3. Verify all secrets are set correctly
4. Check Cloud Run logs

---

**Automated CI/CD with GitHub Actions + Google Cloud Run** 🚀
