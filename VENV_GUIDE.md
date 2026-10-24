# Virtual Environment Guide

## What is a Virtual Environment?

A virtual environment (venv) is an isolated Python environment for your project. It keeps your project dependencies separate from your system Python, preventing version conflicts.

## Benefits

✅ **Isolation**: Dependencies won't conflict with other projects  
✅ **Reproducibility**: Same environment on any machine  
✅ **Clean**: Easy to delete and recreate  
✅ **Professional**: Industry standard practice

---

## Setup (First Time)

### Automatic Setup (Easiest)

```powershell
.\setup_venv.ps1
```

This script will:
1. Create the `venv/` folder
2. Install all required packages
3. Activate the environment

### Manual Setup

```powershell
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
.\venv\Scripts\Activate.ps1

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Install dependencies
pip install langchain langchain-community langchain-huggingface langchain-text-splitters langchain-ollama chromadb pypdf sentence-transformers tiktoken
```

---

## Daily Usage

### Activate the Virtual Environment

**Every time** you open a new terminal to work on this project:

```powershell
.\activate_venv.ps1
```

Or manually:
```powershell
.\venv\Scripts\Activate.ps1
```

You'll see `(venv)` at the start of your terminal prompt:
```
(venv) PS C:\Users\Anto\OneDrive\Desktop\COA capstone>
```

### Run Your Scripts

With venv activated:
```bash
python notebooks/test_vectorstore.py
python src/ingest.py
python src/query.py
```

### Deactivate When Done

```bash
deactivate
```

The `(venv)` prefix will disappear.

---

## Common Issues

### "Execution of scripts is disabled"

If you get this error when activating:
```
.\venv\Scripts\Activate.ps1 : File cannot be loaded because running scripts is disabled
```

**Fix**: Run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

### Wrong Python Version

Make sure you're using the venv's Python:
```powershell
# Check Python location (should point to venv folder)
Get-Command python
```

Expected output:
```
C:\Users\Anto\OneDrive\Desktop\COA capstone\venv\Scripts\python.exe
```

### Packages Not Found

If you get `ModuleNotFoundError`, make sure:
1. The venv is activated (you see `(venv)` in prompt)
2. Packages are installed: `pip list`
3. Re-run setup if needed: `.\setup_venv.ps1`

---

## VSCode Integration

To use the venv in VSCode:

1. Open Command Palette (`Ctrl+Shift+P`)
2. Type: `Python: Select Interpreter`
3. Choose: `.\venv\Scripts\python.exe`

Now VSCode will automatically use your venv!

---

## Deleting and Recreating

If something goes wrong:

```powershell
# 1. Deactivate if active
deactivate

# 2. Delete the venv folder
Remove-Item -Recurse -Force venv

# 3. Recreate it
.\setup_venv.ps1
```

---

## Requirements.txt

The `requirements.txt` file lists all dependencies. To update it after installing new packages:

```bash
pip freeze > requirements.txt
```

To install from requirements.txt:

```bash
pip install -r requirements.txt
```

---

## Summary Cheat Sheet

```powershell
# First time setup
.\setup_venv.ps1

# Every session: activate
.\activate_venv.ps1

# Run your scripts
python src/ingest.py
python src/query.py

# When done: deactivate
deactivate

# Nuclear option: recreate venv
Remove-Item -Recurse -Force venv
.\setup_venv.ps1
```

---

**Best Practice**: Always activate the venv before working on this project! 🎯
