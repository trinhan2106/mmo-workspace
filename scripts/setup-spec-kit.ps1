[CmdletBinding()]
param([switch]$Initialize)
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot
$pin = (Get-Content -LiteralPath 'project/tooling.json' -Raw | ConvertFrom-Json).spec_kit
$sourcePath = Join-Path $repoRoot '.reference/spec-kit'
$venvPath = Join-Path $repoRoot '.tools/spec-kit-venv'
$cachePath = Join-Path $repoRoot '.tools/uv-cache'
if (-not (Test-Path -LiteralPath $sourcePath)) {
    New-Item -ItemType Directory -Path '.reference' -Force | Out-Null
    & git clone --depth 1 --branch $pin.tag $pin.repository $sourcePath
    if ($LASTEXITCODE -ne 0) { throw 'Spec Kit clone failed' }
}
$commit = (& git -C $sourcePath rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $commit -ne $pin.commit) { throw 'Spec Kit source commit differs from pin; do not overwrite local source' }
$specifyPath = Join-Path $venvPath 'Scripts/specify.exe'
$alreadyInstalled = $false
if (Test-Path -LiteralPath $specifyPath) {
    $installedVersion = & $specifyPath --version
    $alreadyInstalled = ($LASTEXITCODE -eq 0 -and $installedVersion -eq ('specify ' + $pin.version))
}
if (-not $alreadyInstalled) {
    & uv --cache-dir $cachePath venv --python 3.12 --allow-existing $venvPath
    if ($LASTEXITCODE -ne 0) { throw 'venv failed; uv and Python 3.12 are required' }
    $pythonPath = Join-Path $venvPath 'Scripts/python.exe'
    & uv --cache-dir $cachePath pip install --python $pythonPath $sourcePath
    if ($LASTEXITCODE -ne 0) { throw 'Spec Kit installation failed' }
}
& $specifyPath --version
if ($LASTEXITCODE -ne 0) { throw 'CLI check failed' }
if ($Initialize) {
    if (Test-Path -LiteralPath '.specify/integration.json') {
        throw 'Already initialized. Upgrades must be reviewed; do not overwrite generated files blindly.'
    }
    & $specifyPath init --here --force --non-interactive --integration codex '--integration-options=--skills --events false' --ignore-agent-tools --script ps --extension github
    if ($LASTEXITCODE -ne 0) { throw 'Spec Kit initialization failed' }
}
