[CmdletBinding()]
param([switch]$InstallOriginalSeat)
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot
$source = (Get-Content -LiteralPath 'jailbreak/catalog.json' -Raw | ConvertFrom-Json).source
if ($InstallOriginalSeat) {
    $state = Get-Content -LiteralPath 'project/tasks.json' -Raw | ConvertFrom-Json
    $bundleTask = $state.tasks | Where-Object { $_.id -eq 'T018' }
    if ($bundleTask.status -eq 'blocked' -or (Test-Path -LiteralPath 'jailbreak/local/INSTALL-BLOCKED.json')) {
        throw 'T018 is blocked after Defender detection. Preserve protection and resolve the guest-environment prerequisite before retrying.'
    }
}
$sourcePath = Join-Path $repoRoot 'jailbreak/gpt6-Astra'
if (-not (Test-Path -LiteralPath $sourcePath)) {
    & git init $sourcePath
    if ($LASTEXITCODE -ne 0) { throw 'Source initialization failed' }
    & git -C $sourcePath remote add origin ('https://github.com/' + $source.repository + '.git')
    if ($LASTEXITCODE -ne 0) { throw 'Source remote failed' }
    & git -C $sourcePath fetch --depth 1 origin $source.commit
    if ($LASTEXITCODE -ne 0) { throw 'Pinned source fetch failed' }
    & git -C $sourcePath checkout --detach FETCH_HEAD
    if ($LASTEXITCODE -ne 0) { throw 'Pinned source checkout failed' }
}
$commit = (& git -C $sourcePath rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $commit -ne $source.commit) { throw 'Upstream commit mismatch; preserve local source' }
& node scripts/bypass.cjs check
if ($LASTEXITCODE -ne 0) { throw 'Invalid byPass catalog' }
$desktopPath = Join-Path $sourcePath 'desktop'
$npmCache = Join-Path $repoRoot '.tools/npm-cache'
Push-Location -LiteralPath $desktopPath
try {
    & npm ci --ignore-scripts --no-audit --no-fund --cache $npmCache
    if ($LASTEXITCODE -ne 0) { throw 'ColdCoffee dependency installation failed' }
    $priorCache = $env:ELECTRON_CACHE
    $priorGlobalCache = $env:electron_config_cache
    try {
        $env:ELECTRON_CACHE = Join-Path $repoRoot '.tools/electron-cache'
        $env:electron_config_cache = $env:ELECTRON_CACHE
        & node node_modules/electron/install.js
        if ($LASTEXITCODE -ne 0) { throw 'Electron runtime preparation failed' }
    } finally {
        $env:ELECTRON_CACHE = $priorCache
        $env:electron_config_cache = $priorGlobalCache
    }
} finally {
    Pop-Location
}
& node scripts/bypass.cjs preview
if ($LASTEXITCODE -ne 0) { throw 'Scoped upstream installation preview failed' }
if ($InstallOriginalSeat) {
    & node scripts/bypass.cjs install
    if ($LASTEXITCODE -ne 0) { throw 'Scoped upstream installation failed' }
    & node scripts/bypass.cjs verify
    if ($LASTEXITCODE -ne 0) { throw 'Installed files failed upstream verification' }
} else {
    Write-Output 'Source, locked dependencies and Electron prepared. Full seat deployment is separate and currently BLOCKED in T018; no full-install success is claimed.'
}
