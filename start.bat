@echo off
cd /d "%~dp0"
echo Installing frontend packages...
call npm install
echo Installing Python packages...
python -m pip install -r backend\requirements.txt
echo Starting API on http://127.0.0.1:8010
start "AI Travel Guide API" cmd /k python run.py
echo Starting app on http://localhost:5173
call npm run dev
