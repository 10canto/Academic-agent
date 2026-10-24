# Activate the virtual environment for this project
# Usage: .\activate_venv.ps1

Write-Host "Activating virtual environment..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"
Write-Host "Virtual environment activated!" -ForegroundColor Green
Write-Host "Python location: $(which python)" -ForegroundColor Cyan
Write-Host "To deactivate, type: deactivate" -ForegroundColor Yellow
