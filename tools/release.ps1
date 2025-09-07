param(
  [ValidateSet('patch','minor','major')]
  [string]$Bump = 'patch',
  [string]$Notes = 'Auto build'
)

$ErrorActionPreference = 'Stop'

function Require-Cmd($name) {
  if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
    throw "Required command not found: $name"
  }
}

Require-Cmd git

# Ensure we are at repo root
if (-not (Test-Path .git)) { throw 'Run from repo root.' }

git fetch --tags | Out-Null

$latest = (git tag --list 'v*' --sort=-version:refname | Select-Object -First 1)
if (-not $latest) { $latest = 'v0.0.0' }

if ($latest -notmatch '^v(\d+)\.(\d+)\.(\d+)$') { throw "Unexpected tag format: $latest" }
$major = [int]$Matches[1]
$minor = [int]$Matches[2]
$patch = [int]$Matches[3]

switch ($Bump) {
  'major' { $major++; $minor = 0; $patch = 0 }
  'minor' { $minor++; $patch = 0 }
  default { $patch++ }
}

$newTag = "v$major.$minor.$patch"

# Check clean working tree (warn only)
$status = git status --porcelain
if ($status) {
  Write-Warning 'Working tree not clean. Only tagged commit will be released.'
}

Write-Host "Latest tag: $latest"
Write-Host "New tag   : $newTag"

# Create annotated tag and push
git tag -a $newTag -m "Release $newTag`n`n$Notes"
git push origin $newTag

# Try to trigger workflow manually too (optional)
if (Get-Command gh -ErrorAction SilentlyContinue) {
  try {
    gh workflow run release.yml -f tag=$newTag --ref main | Out-Null
    Write-Host 'Triggered workflow_dispatch via gh.'
  } catch {
    Write-Warning "gh workflow run failed: $_"
  }
} else {
  Write-Host 'gh CLI not found; relying on tag push trigger.'
}

Write-Host "Release will appear at: https://github.com/${env:GITHUB_REPOSITORY:-'Nikitzima/YT-DLP-GUI'}/releases/tag/$newTag"
Write-Host "Latest .exe link: https://github.com/Nikitzima/YT-DLP-GUI/releases/latest/download/YT-DLP_GUI.exe"

