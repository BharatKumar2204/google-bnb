# FACT-X Project Structure

## Root Directory

```
ai-news-app/
├── .git/                           # Git repository
├── .github/                        # GitHub workflows for deployment
│   └── workflows/
│       ├── deploy-backend.yml      # Backend deployment workflow
│       ├── deploy-frontend.yml     # Frontend deployment workflow
│       └── README.md               # Workflow documentation
├── .vscode/                        # VS Code settings
├── frontend/                       # React frontend application
├── mcp_server/                     # Python backend server
├── DEEP_ANALYSIS_IMPROVEMENTS.md  # Deep analysis feature docs
├── DYNAMIC_VERIFICATION_SCORING.md # Scoring system docs
├── FAKE_NEWS_DETECTION.md         # Fake news detection docs
├── FEATURES.md                     # Consolidated feature overview
├── README.md                       # Main project documentation
├── setup.bat                       # Initial project setup script
├── start-backend.bat               # Start backend (Windows CMD)
├── start-backend.ps1               # Start backend (PowerShell)
├── start-frontend.bat              # Start frontend (Windows CMD)
└── start-frontend.ps1              # Start frontend (PowerShell)
```

## Quick Start

### 1. Setup
```bash
setup.bat
```

### 2. Start Backend
```bash
# Windows CMD
start-backend.bat

# PowerShell
.\start-backend.ps1
```

### 3. Start Frontend
```bash
# Windows CMD
start-frontend.bat

# PowerShell
.\start-frontend.ps1
```

## Documentation

- **README.md** - Complete setup and usage guide
- **FEATURES.md** - Overview of all features
- **DEEP_ANALYSIS_IMPROVEMENTS.md** - Deep analysis details
- **DYNAMIC_VERIFICATION_SCORING.md** - Scoring system
- **FAKE_NEWS_DETECTION.md** - Fake news detection

## Directories

### Frontend (`frontend/`)
React application with:
- Components (Dashboard, TrendingNews, DeepAnalysis, etc.)
- Services (API integration)
- Styles (CSS files)
- Configuration (Vite, environment variables)

### Backend (`mcp_server/`)
Python FastAPI server with:
- Agents (8 specialized AI agents)
- ADK Agent (Google ADK integration)
- Configuration (environment setup)
- Utilities (logging, helpers)

### GitHub Workflows (`.github/workflows/`)
CI/CD pipelines for:
- Backend deployment
- Frontend deployment
- Automated testing

## Development

### Backend
```bash
cd mcp_server
pip install -r requirements.txt
python run_server.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Deployment

GitHub Actions workflows handle automatic deployment:
- Push to main branch triggers deployment
- Backend deploys to Cloud Run
- Frontend deploys to Cloud Run
- Environment variables managed via GitHub Secrets

## Environment Variables

### Backend (.env in mcp_server/)
```env
GEMINI_API_KEY=your_gemini_api_key
GCP_PROJECT_ID=your_project_id
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8000
```

### Frontend (.env in frontend/)
```env
VITE_API_URL=http://localhost:8000
```

## Tech Stack

### Backend
- Python 3.11
- FastAPI
- Google Gemini 2.5 Pro
- Google Cloud Platform
- Uvicorn

### Frontend
- React 18
- Vite
- Axios
- Leaflet.js
- date-fns

## Project Status

✅ Clean and organized
✅ All test files removed
✅ Documentation consolidated
✅ Ready for development
✅ Ready for deployment

---

**Last Updated**: November 2024
**Version**: 3.0
