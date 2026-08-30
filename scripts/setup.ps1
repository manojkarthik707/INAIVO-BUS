param([switch]$SkipFrontend)

$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $ProjectRoot

$UserProfilePath = [Environment]::GetFolderPath('UserProfile')
$CodexPython = Join-Path $UserProfilePath '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$BasePython = if (Test-Path -LiteralPath $CodexPython) { $CodexPython } else { (Get-Command python).Source }
$WindowsVenvPython = Join-Path $ProjectRoot '.venv\Scripts\python.exe'
$PosixVenvPython = Join-Path $ProjectRoot '.venv\bin\python.exe'
if ((Test-Path -LiteralPath $PosixVenvPython) -and (Test-Path -LiteralPath $CodexPython)) {
    Write-Host '[SETUP] Replacing incompatible MSYS virtual environment with native CPython'
    Remove-Item -LiteralPath (Join-Path $ProjectRoot '.venv') -Recurse -Force
}
if (-not (Test-Path -LiteralPath $WindowsVenvPython) -and -not (Test-Path -LiteralPath $PosixVenvPython)) {
    Write-Host '[SETUP] Creating Python 3.11 virtual environment'
    & $BasePython -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw "virtual environment creation failed with exit code $LASTEXITCODE" }
}
$VenvPython = if (Test-Path -LiteralPath $WindowsVenvPython) { $WindowsVenvPython } else { $PosixVenvPython }

Write-Host '[SETUP] Installing pinned Python dependencies'
& $VenvPython -m pip install --disable-pip-version-check -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "Python dependency installation failed with exit code $LASTEXITCODE" }

if (-not $SkipFrontend) {
    Write-Host '[SETUP] Installing dashboard dependencies using the local npm cache'
    Push-Location frontend
    try {
        npm --cache '..\npm-cache' install
        if ($LASTEXITCODE -ne 0) { throw "npm install failed with exit code $LASTEXITCODE" }
        npm --cache '..\npm-cache' run build
        if ($LASTEXITCODE -ne 0) { throw "dashboard build failed with exit code $LASTEXITCODE" }
    }
    finally {
        Pop-Location
    }
}

Write-Host '[SETUP] Environment ready'
