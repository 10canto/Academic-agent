# Helper script to run any Python script in the venv
# Usage: .\run_in_venv.ps1 <script_path>
# Example: .\run_in_venv.ps1 notebooks/test_vectorstore.py

param(
    [Parameter(Mandatory=$true)]
    [string]$ScriptPath
)

if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Run .\setup_venv.ps1 first to create it." -ForegroundColor Yellow
    exit 1
}

Write-Host "Activating venv and running: $ScriptPath" -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"
python $ScriptPath
