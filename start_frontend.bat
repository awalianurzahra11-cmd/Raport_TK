@echo off
title Frontend React Server - E-Raport TK ABK
cd /d "%~dp0"
echo ========================================================
echo   Menjalankan Frontend React di http://localhost:5173
echo ========================================================
cd frontend-react
call npm run dev
pause
