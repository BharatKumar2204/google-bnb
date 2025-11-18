@echo off
echo ========================================
echo AI News Verification Dashboard Setup
echo ========================================
echo.

echo [1/4] Setting up backend...
cd mcp_server
if not exist .env (
    copy .env.example .env
    echo Created .env file - Please configure your API keys
)
pip install -r requirements.txt
cd ..

echo.
echo [2/4] Setting up frontend...
cd frontend
if not exist .env (
    copy .env.example .env
)
call npm install
cd ..

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Configure API keys in mcp_server\.env (optional for demo)
echo 2. Run start-backend.bat in one terminal
echo 3. Run start-frontend.bat in another terminal
echo 4. Open http://localhost:3000 in your browser
echo.
pause
