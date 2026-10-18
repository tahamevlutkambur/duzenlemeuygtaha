@echo off
title PROMKOL Katalog Editoru
cd /d "%~dp0"
echo ====================================================
echo   PROMKOL KATALOG STUDYO & CANLI DOKUMAN EDITORU
echo ====================================================
echo.
echo Sunucu baslatiliyor...
start "" "http://localhost:8080/katalog.html"
"C:\Users\Taha\AppData\Local\Programs\Python\Python311\python.exe" editor_server.py
pause
