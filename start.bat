@echo off
title Organization Chart Server
cd /d "%~dp0"
echo ========================================
echo    Starting Organization Chart...
echo    http://localhost:8501
echo ========================================
echo.
streamlit run app.py --server.port 8501
pause
