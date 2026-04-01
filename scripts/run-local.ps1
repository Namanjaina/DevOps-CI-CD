$ErrorActionPreference = "Stop"

Set-Location (Split-Path -Parent $PSScriptRoot)

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
}

Write-Host "Starting Django app on http://127.0.0.1:8000 ..."
python manage.py runserver 127.0.0.1:8000

