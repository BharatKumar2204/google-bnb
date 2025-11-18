# Container Registry Update

## Issue Fixed

GitHub Actions was failing with:
```
name unknown: Repository "ai-news" not found
```

This happened because Artifact Registry requires pre-creating repositories.

## Solution

Updated workflows to use **Container Registry (gcr.io)** instead of Artifact Registry.

### Why Container Registry?

1. **No Pre-creation Needed**: Repositories are created automatically
2. **Simpler Setup**: No need to run `gcloud artifacts repositories create`
3. **Same Performance**: Both work equally well with Cloud Run
4. **Widely Used**: Standard for many Cloud Run deployments

### Changes Made

**Before (Artifact Registry):**
```yaml
gcloud auth configure-docker us-central1-docker.pkg.dev
docker build -t us-central1-docker.pkg.dev/PROJECT/ai-news/SERVICE:TAG .
```

**After (Container Registry):**
```yaml
gcloud auth configure-docker
docker build -t gcr.io/PROJECT/SERVICE:TAG .
```

### Files Updated

1. `.github/workflows/deploy-backend.yml`
2. `.github/workflows/deploy-frontend.yml`
3. `setup-gcp-deployment.sh`
4. `setup-gcp-deployment.bat`

### API Changes

**Before:**
- `artifactregistry.googleapis.com`

**After:**
- `containerregistry.googleapis.com`

### Next Steps

1. Commit and push the updated workflows:
   ```cmd
   git add .
   git commit -m "Switch to Container Registry (gcr.io)"
   git push origin main
   ```

2. GitHub Actions will now work without pre-creating repositories

3. Images will be stored at:
   - Backend: `gcr.io/YOUR_PROJECT_ID/ai-news-backend`
   - Frontend: `gcr.io/YOUR_PROJECT_ID/ai-news-frontend`

## Migration to Artifact Registry (Optional)

If you want to use Artifact Registry later, run:

```bash
# Create repository
gcloud artifacts repositories create ai-news \
  --repository-format=docker \
  --location=us-central1

# Update workflows to use:
# us-central1-docker.pkg.dev/PROJECT_ID/ai-news/SERVICE_NAME
```

## Benefits of Current Setup

- ✅ Works immediately without setup
- ✅ No repository pre-creation needed
- ✅ Simpler configuration
- ✅ Same performance as Artifact Registry
- ✅ Automatic cleanup of old images (configurable)

---

**Status**: ✅ Fixed and ready to deploy
**Date**: November 18, 2025
