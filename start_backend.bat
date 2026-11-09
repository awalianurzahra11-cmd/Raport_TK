@echo off
title Backend FastAPI Server - E-Raport TK ABK
cd /d "%~dp0"
echo ========================================================
echo   Menjalankan Backend Server di http://127.0.0.1:8000
echo ========================================================
python run_backend.py
pause
