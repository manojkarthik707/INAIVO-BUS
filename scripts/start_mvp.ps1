# start_mvp.ps1
Write-Host "Starting AI-Powered Mobile Urban Intelligence Platform (MOCK MVP)" -ForegroundColor Cyan

# Start Backend
Write-Host "Generating Intelligent Traffic Routes..." -ForegroundColor Cyan
& "..\.venv\Scripts\python.exe" "intelligent_routes.py"
& "..\.venv\Scripts\python.exe" "inject_vehicles.py"

Write-Host "Starting FastAPI Backend (Webots Mode)..." -ForegroundColor Green
$env:SIMULATION_MODE="webots"
$backend_process = Start-Process -FilePath "..\.venv\Scripts\python.exe" -ArgumentList "-m uvicorn app.main:app --host 127.0.0.1 --port 8000" -WorkingDirectory "..\backend" -PassThru -NoNewWindow

# Start Frontend
Write-Host "Starting React Dashboard..." -ForegroundColor Yellow
$frontend_process = Start-Process -FilePath "npm.cmd" -ArgumentList "run dev" -WorkingDirectory "..\frontend" -PassThru -NoNewWindow

Write-Host "Both services are starting..." -ForegroundColor Green
Write-Host "Backend: http://localhost:8000"
Write-Host "Frontend: http://localhost:5173"
Write-Host "Press Ctrl+C to stop both."

try {
    Wait-Process -Id $backend_process.Id
} finally {
    Write-Host "Stopping services..." -ForegroundColor Red
    Stop-Process -Id $backend_process.Id -ErrorAction SilentlyContinue
    Stop-Process -Id $frontend_process.Id -ErrorAction SilentlyContinue
}
