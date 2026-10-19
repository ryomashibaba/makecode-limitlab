param(
    [ValidateSet('Inspect','Prepare')][string]$Mode = 'Prepare',
    [string]$OutputRoot,
    [int]$WatchSeconds = 900
)
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$python = Join-Path $PSScriptRoot 'qa_p24_g2.py'
$observer = Join-Path $PSScriptRoot 'qa_p24.py'
$copy = Join-Path $repo 'makecode/COPY_P23.ps1'
$root = if ($OutputRoot) { [IO.Path]::GetFullPath($OutputRoot) }
        else { Join-Path (Join-Path $env:USERPROFILE 'Downloads') 'MakeCode_LimitLab' }

if ($WatchSeconds -lt 1) { throw 'WatchSeconds must be positive.' }
if (-not (Test-Path -LiteralPath $python) -or
    -not (Test-Path -LiteralPath $observer) -or
    -not (Test-Path -LiteralPath $copy)) { throw 'G2 requires the complete repository; no ZIP fragment.' }

$action = if ($Mode -eq 'Inspect') { 'inspect' } else { 'preflight' }
# This gate does NOT create directories, latches, or clipboard contents.
$raw = & python $python $action --repo $repo --output-root $root
$gateExit = $LASTEXITCODE
if (-not $raw) { throw 'G2 gate returned no result. No preparation attempted.' }
try { $report = $raw | ConvertFrom-Json } catch {
    throw 'G2 gate returned unreadable JSON. No preparation attempted.'
}
Write-Host ('G2: ' + $report.decision + ' / ' + $report.reason)
Write-Host ('Git HEAD: ' + $report.git_head)
Write-Host ('Pinned source: ' + $report.source)
Write-Host ('P23 latch: ' + $report.latch + ' / P23 CSV: ' + $report.p23_csv)
if ($Mode -eq 'Inspect') {
    Write-Host 'READ ONLY: no files, clipboard, or Minecraft were changed.'
    exit 0
}
if ($gateExit -ne 0 -or $report.decision -cne 'ALLOW_PREPARE') {
    Write-Host 'BLOCKED. Keep historical CSV/latch. No automatic reset or retry.' -ForegroundColor Yellow
    exit 3
}
if ([Threading.Thread]::CurrentThread.GetApartmentState() -ne
    [Threading.ApartmentState]::STA) {
    throw 'Clipboard requires an STA session. Launch RUN_P24_G2.cmd.'
}

# A PREPARE launch is a deliberate local preparation action, NOT authorization
# to enter labcity23 in Minecraft. This reuses existing SHA-pinned checks.
Write-Host 'Preparing the verified P2.3 clipboard and existing one-shot latch...'
& powershell.exe -NoProfile -NoLogo -STA -ExecutionPolicy Bypass -File $copy -OutputRoot $root
if ($LASTEXITCODE -ne 0) {
    throw 'P2.3 clipboard verification failed. Do not paste or run.'
}

# Fail closed if another process changed the latch during clipboard setup.
$latch = Join-Path $root 'logs/P23_ONCE.txt'
if (-not (Test-Path -LiteralPath $latch) -or
    [IO.File]::ReadAllText($latch) -cne 'READY_P23') {
    throw 'After preparation, latch is not READY. Do not run Minecraft.'
}
Write-Host ''
Write-Host 'PREPARED: source is on clipboard. NO MINECRAFT CONSTRUCTION WAS STARTED.' -ForegroundColor Green
Write-Host '1. Only in a NEW DISPOSABLE LimitLab world, paste MakeCode JS and check 0 errors.'
Write-Host '2. Run labarea23 to inspect the entire planned site.'
Write-Host '3. Run labcity23 ONCE only after separately approving the construction.'
Write-Host '4. Stay with this window for automatic read-only CSV result diagnosis.'
Write-Host 'Never repeat a failed run by deleting the P23 latch.'
Write-Host ''
Write-Host 'G2 observer: waiting for a NEW stable P2.3 CSV; no GUI automation.'
& python $observer watch --repo $repo --output-root $root --timeout $WatchSeconds
$watchExit = $LASTEXITCODE
Write-Host ''
if ($watchExit -eq 0) {
    Write-Host 'OBSERVATION ENDED: review sampled-only or STOP result above.' -ForegroundColor Green
} elseif ($watchExit -eq 2) {
    Write-Host 'NO NEW TERMINAL CSV: timeout. Do not reset latch or auto-retry.' -ForegroundColor Yellow
} else {
    Write-Host 'OBSERVER ERROR: preserve all evidence; do not auto-retry.' -ForegroundColor Red
}
exit $watchExit
