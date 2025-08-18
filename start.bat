@echo off
echo Starting Home Shopping Application...
echo.

echo Starting Flask API Server...
start "Flask API" cmd /k "cd api && python app.py"

echo Waiting for API server to start...
timeout /t 5 /nobreak > nul

echo Starting React Frontend...
start "React Frontend" cmd /k "cd frontend && pnpm dev"

echo.
echo Application is starting...
echo Flask API: http://localhost:5000
echo React App: http://localhost:5173
echo.
echo Press any key to exit this launcher...
pause > nul 