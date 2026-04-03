$ErrorActionPreference = "Stop"

Set-Location (Split-Path -Parent $PSScriptRoot)

function Get-PythonCommand {
    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if ($pythonCommand) {
        return @($pythonCommand.Source)
    }

    $pyCommand = Get-Command py -ErrorAction SilentlyContinue
    if ($pyCommand) {
        return @($pyCommand.Source, "-3")
    }

    throw "Python was not found. Install Python 3 and make sure 'python' or 'py' works in PowerShell."
}

function Invoke-Python {
    param(
        [string[]]$PythonCommand,
        [string[]]$Arguments
    )

    $command = $PythonCommand[0]
    $prefixArgs = @()
    if ($PythonCommand.Length -gt 1) {
        $prefixArgs = $PythonCommand[1..($PythonCommand.Length - 1)]
    }

    & $command @prefixArgs @Arguments
}

try {
    if (-not (Test-Path ".env")) {
        Copy-Item ".env.example" ".env"
    }

    $pythonCommand = Get-PythonCommand

    Write-Host "Running migrations..."
    Invoke-Python -PythonCommand $pythonCommand -Arguments @("manage.py", "migrate")

    Write-Host "Starting Django app on http://127.0.0.1:8000 ..."
    Write-Host "Keep this terminal open while using the website."
    Invoke-Python -PythonCommand $pythonCommand -Arguments @("manage.py", "runserver", "127.0.0.1:8000")
}
catch {
    Write-Host ""
    Write-Host "Failed to start the website:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to close"
}
