[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot
$venvPath = Join-Path $repoRoot '.tools/quality-venv'
$ruffPath = Join-Path $venvPath 'Scripts/ruff.exe'
$wanted = (Get-Content -LiteralPath 'project/quality-requirements.txt' -Raw).Trim().Replace('==', ' ')
if (Test-Path -LiteralPath $ruffPath) {
    $actual = & $ruffPath --version
    if ($LASTEXITCODE -eq 0 -and $actual -eq $wanted) { Write-Output $actual; return }
}
& uv --cache-dir .tools/uv-cache venv --python 3.12 --allow-existing $venvPath
if ($LASTEXITCODE -ne 0) { throw 'quality venv creation failed' }
& uv --cache-dir .tools/uv-cache pip install --python (Join-Path $venvPath 'Scripts/python.exe') -r project/quality-requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'quality tooling installation failed' }
& $ruffPath --version
