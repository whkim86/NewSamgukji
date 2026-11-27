@echo off
cd /d "%~dp0"
where node >nul 2>&1 || (echo Install Node.js LTS first: https://nodejs.org/ & pause & exit /b 1)
where npm >nul 2>&1 || (echo npm not found & pause & exit /b 1)
if not exist node_modules\vite\bin\vite.js (
 call npm install --no-audit --no-fund
 if errorlevel 1 (echo Dependency installation failed. Check internet connection. & pause & exit /b 1)
)
call npm run dev -- --open --port 5173
pause
