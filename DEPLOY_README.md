# 🚀 Deploy to Google Cloud Run - Complete Guide

Your AI News Verification Platform is ready to deploy to Google Cloud Run with automated CI/CD!

## 📋 What's Included

### GitHub Actions Workflows
- ✅ `deploy-backend.yml` - Automated backend deployment
- ✅ `deploy-frontend.yml` - Automated frontend deployment

### Docker Configuration
- ✅ Backend Dockerfile (Python + FastAPI)
- ✅ Frontend Dockerfile (React + Nginx)
- ✅ Nginx configuration with security headers
- ✅ .dockerignore files for optimized builds

### Setup Scripts
- ✅ `setup-gcp-deployment.sh` (Linux/Mac)
- ✅ `setup-gcp-deployment.bat` (Windows)

### Documentation
- ✅ `QUICK_DEPLOY.md` - 5-minute quick start
- ✅ `DEPLOYMENT_GUIDE.md` - Comprehensive guide
- ✅ `DEPLOYMENT_SUMMARY.md` - Architecture overview
- ✅ `DEPLOYMENT_CHECKLIST.md` - Step-by-step checklist

## 🎯 Quick Start (5 Minutes)

### 1. Run Setup Script

**Windows:**
```cmd
cd ai-news-app
setup-gcp-deployment.bat
```

**Linux/Mac:**
```bash
cd ai-news-app
chmod +x setup-gcp-deployment.sh
./setup-gcp-deployment.sh
```

### 2. Add GitHub Secrets

Go to: **GitHub Repo → Settings → Secrets and variables → Actions**

Add these 4 secrets:

| Secret | Value |
|--------|-------|
| `GCP_SA_KEY` | Content of `github-actions-key.json` |
| `GCP_PROJECT_ID` | Your GCP project ID |
| `GEMINI_API_KEY` | Your Gemini API key |
| `BACKEND_URL` | Leave empty for now |

### 3. Deploy Backend

**Option A - GitHub Actions (Recommended):**
```bash
git add .
git commit -m "Add deployment config"
git push origin main
```
Then: **GitHub → Actions → Deploy Backend → Run workflow**

**Option B - Manual:**
```bash
cd mcp_server
gcloud run deploy ai-news-backend --source . --region us-central1 --allow-unauthenticated
```

### 4. Update BACKEND_URL

Get backend URL:
```bash
gcloud run services describe ai-news-backend --region us-central1 --format 'value(status.url)'
```

Add it as `BACKEND_URL` secret in GitHub.

### 5. Deploy Frontend

**GitHub → Actions → Deploy Frontend → Run workflow**

### 6. Done! 🎉

Your app is live:
- Backend: `https://ai-news-backend-xxxxx-uc.a.run.app`
- Frontend: `https://ai-news-frontend-xxxxx-uc.a.run.app`

## 📚 Documentation

Choose your path:

### For Quick Deployment
👉 **[QUICK_DEPLOY.md](QUICK_DEPLOY.md)** - Get started in 5 minutes

### For Detailed Setup
👉 **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Complete step-by-step guide

### For Understanding Architecture
👉 **[DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md)** - Architecture & technical details

### For Tracking Progress
👉 **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Comprehensive checklist

## 🏗️ Architecture

```
GitHub Push → GitHub Actions → Build Docker → Push to Registry → Deploy to Cloud Run
```

**Frontend:** React + Vite → Nginx → Cloud Run (Port 8080)
**Backend:** FastAPI + Python → Cloud Run (Port 8080)

## 💰 Cost Estimate

**Free Tier:** 2 million requests/month FREE

**Typical Cost:**
- Low traffic: $0-5/month
- Medium traffic: $15-20/month
- High traffic: $150-200/month

## 🔧 What Gets Deployed

### Backend Service
- **Name:** `ai-news-backend`
- **Memory:** 2Gi
- **CPU:** 2 cores
- **Scaling:** 0-10 instances
- **Port:** 8080

### Frontend Service
- **Name:** `ai-news-frontend`
- **Memory:** 512Mi
- **CPU:** 1 core
- **Scaling:** 0-5 instances
- **Port:** 8080

## 🔐 Security

- ✅ HTTPS enforced automatically
- ✅ Non-root containers
- ✅ Secrets in GitHub Secrets
- ✅ Security headers configured
- ✅ IAM permissions (least privilege)
- ✅ No credentials in repository

## 🔄 Automatic Deployments

After initial setup, deployments are automatic:

- **Backend:** Push to `mcp_server/**` → Auto-deploys
- **Frontend:** Push to `frontend/**` → Auto-deploys

## 📊 Monitoring

### View Logs
```bash
# Backend
gcloud run services logs read ai-news-backend --region us-central1

# Frontend
gcloud run services logs read ai-news-frontend --region us-central1
```

### Cloud Console
Visit: https://console.cloud.google.com/run

## 🐛 Troubleshooting

### Build Fails
- Check Dockerfile syntax
- Verify dependencies in requirements.txt/package.json
- Review GitHub Actions logs

### Deploy Fails
- Verify service account permissions
- Check GCP_SA_KEY secret is valid
- Ensure APIs are enabled

### Backend Errors
- Check logs: `gcloud run services logs read ai-news-backend`
- Verify GEMINI_API_KEY is set
- Check environment variables

### Frontend Can't Connect
- Verify BACKEND_URL is correct
- Check backend is deployed and healthy
- Review CORS settings

## 📞 Support

Need help?

1. Check the documentation files
2. Review GitHub Actions logs
3. Check Cloud Run logs
4. Verify all secrets are set

## 🎓 Learning Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## ✅ Deployment Checklist

Quick checklist:

- [ ] Run setup script
- [ ] Add GitHub secrets (4 required)
- [ ] Deploy backend
- [ ] Update BACKEND_URL secret
- [ ] Deploy frontend
- [ ] Test both services
- [ ] Verify automatic deployments work

## 🚀 Next Steps

After deployment:

1. Test all features
2. Set up custom domain (optional)
3. Configure monitoring alerts
4. Enable Cloud CDN (optional)
5. Set up staging environment

## 📝 Files Created

```
ai-news-app/
├── .github/
│   └── workflows/
│       ├── deploy-backend.yml      # Backend CI/CD
│       └── deploy-frontend.yml     # Frontend CI/CD
├── frontend/
│   ├── Dockerfile                  # Frontend container
│   ├── nginx.conf                  # Nginx config
│   └── .dockerignore              # Build optimization
├── mcp_server/
│   ├── Dockerfile                  # Backend container
│   └── .dockerignore              # Build optimization
├── setup-gcp-deployment.sh        # Linux/Mac setup
├── setup-gcp-deployment.bat       # Windows setup
├── QUICK_DEPLOY.md                # Quick start guide
├── DEPLOYMENT_GUIDE.md            # Full guide
├── DEPLOYMENT_SUMMARY.md          # Architecture details
├── DEPLOYMENT_CHECKLIST.md        # Step-by-step checklist
└── DEPLOY_README.md               # This file
```

## 🎉 Ready to Deploy!

Everything is configured and ready. Follow the Quick Start above or dive into the detailed guides.

**Choose your path:**
- ⚡ Fast: [QUICK_DEPLOY.md](QUICK_DEPLOY.md)
- 📖 Detailed: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- ✅ Checklist: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

---

**Happy Deploying! 🚀**

Questions? Check the troubleshooting section or review the comprehensive guides.
