@echo off
title Setup Database MySQL - E-Raport TK ABK
cd /d "%~dp0"
echo ========================================================
echo   Inisialisasi Database MySQL (raport_tk)
echo ========================================================
python database\setup_db.py
pause
