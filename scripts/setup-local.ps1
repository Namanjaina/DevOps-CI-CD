$ErrorActionPreference = "Stop"

Set-Location (Split-Path -Parent $PSScriptRoot)

Write-Host "Installing Python dependencies..."
python -m pip install -r requirements.txt

Write-Host "Running Django migrations..."
python manage.py migrate

Write-Host "Local setup complete."
Write-Host "Start app with: powershell -ExecutionPolicy Bypass -File .\\scripts\\run-local.ps1"

