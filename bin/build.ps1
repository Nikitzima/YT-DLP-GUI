$ErrorActionPreference = 'Stop'

# Resolve repo root and Python
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot  = Split-Path -Parent $ScriptDir
$VenvPy    = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$Python    = if (Test-Path $VenvPy) { $VenvPy } else { "python" }

# Paths and names
$Spec       = "YT-DLP GUI.spec"
$ExeName    = "YT-DLP GUI.exe"
$ReleaseDir = "release"

Write-Host "Using Python: $Python" -ForegroundColor DarkCyan
Write-Host "Cleaning build artifacts..." -ForegroundColor Cyan
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue

Write-Host "Ensuring PyInstaller is available..." -ForegroundColor Cyan
& $Python -m pip install --upgrade pip | Out-Null
& $Python -m pip install --upgrade pyinstaller | Out-Null

# Install project dependencies
if (Test-Path (Join-Path $RepoRoot 'requirements.txt')) {
    Write-Host "Installing project requirements..." -ForegroundColor Cyan
    & $Python -m pip install -r (Join-Path $RepoRoot 'requirements.txt') | Out-Null
} else {
    Write-Host "Installing minimal runtime deps..." -ForegroundColor Cyan
    & $Python -m pip install customtkinter Pillow | Out-Null
}

Write-Host "Building one-file executable..." -ForegroundColor Cyan
& $Python -m PyInstaller --noconfirm --clean "$Spec"

if (-not (Test-Path (Join-Path dist $ExeName))) {
    Write-Error "Build failed: dist/$ExeName not found"
    exit 1
}

New-Item -ItemType Directory -Force -Path $ReleaseDir | Out-Null
$stamp = Get-Date -Format "yyyyMMdd-HHmm"
$zipPath = Join-Path $ReleaseDir ("YT-DLP_GUI_portable_$stamp.zip")

Write-Host "Packing portable zip..." -ForegroundColor Cyan
Compress-Archive -LiteralPath (Join-Path dist $ExeName) -DestinationPath $zipPath -Force

Write-Host "Done: $zipPath" -ForegroundColor Green
