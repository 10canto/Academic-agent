# Setup script - creates venv and installs all dependencies
# Usage: .\setup_venv.ps1

Write-Host "Creating virtual environment..." -ForegroundColor Green
python -m venv venv

Write-Host "`nActivating virtual environment..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"

Write-Host "`nInstalling dependencies from requirements.txt..." -ForegroundColor Green
pip install --upgrade pip
pip install langchain langchain-community langchain-huggingface langchain-text-splitters langchain-ollama chromadb pypdf sentence-transformers tiktoken

Write-Host "`n✓ Setup complete!" -ForegroundColor Green
Write-Host "To activate the venv in the future, run: .\activate_venv.ps1" -ForegroundColor Cyan
