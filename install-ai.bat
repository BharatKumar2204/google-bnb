@echo off
echo ========================================
echo Installing AI Dependencies
echo ========================================
echo.

cd mcp_server
pip install google-generativeai

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Now restart your backend:
echo   cd mcp_server
echo   python run_server.py
echo.
pause
