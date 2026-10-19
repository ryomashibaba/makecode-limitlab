$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$copy = Join-Path $repo 'makecode/COPY_G4B.ps1'
$observer = Join-Path $PSScriptRoot 'g4b_capture.py'
if (-not (Test-Path -LiteralPath $copy) -or -not (Test-Path -LiteralPath $observer)) {
    throw 'Incomplete G4B A1 files: no execution.'
}
# New independent result folder on EVERY launch; never reuse a run or delete data.
$runId = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ') + '_' +
    [Guid]::NewGuid().ToString('N').Substring(0,12)
$base = Join-Path (Join-Path $env:USERPROFILE 'Downloads') 'MakeCode_LimitLab/G4B_B1/runs'
$root = Join-Path $base $runId
Write-Host ('G4B A1 new run: ' + $runId)
Write-Host ('Private output: ' + $root)
Write-Host 'Old P2.3 / P2.4R CSV and USED latches remain untouched.'
& powershell.exe -NoLogo -NoProfile -STA -ExecutionPolicy Bypass -File $copy -OutputRoot $root
if ($LASTEXITCODE -ne 0) {
    throw 'New run preparation blocked. Do not paste unverified code or delete any past results.'
}
Write-Host ''
Write-Host 'PREPARED: pasted source is ONLY for this unique run.' -ForegroundColor Green
Write-Host '1. In a disposable Minecraft Education test world, replace MakeCode JavaScript with Ctrl+A then Ctrl+V.'
Write-Host '2. Keep File Read & Write extension and check for zero editor errors.'
Write-Host '3. Type labareag4b to preview the civic district at Y96 or higher.'
Write-Host '4. Type labcityg4b ONCE in a disposable test world only.'
Write-Host '5. The existing result CSV/latch of ALL previous runs are never reused.'
Write-Host 'If you exit this window, DO NOT prepare a different run just to collect old evidence.'
Write-Host ('Output folder to preserve: ' + $root)
Write-Host ''
Write-Host 'Read-only observer waiting at most 20 minutes for new run evidence...'
& python -B $observer --output-root $root --wait 1200
$code = $LASTEXITCODE
if ($code -eq 0) {
    Write-Host ('Result ZIP generated in: ' + (Join-Path $root 'private_results')) -ForegroundColor Green
} else {
    Write-Host 'No terminal CSV detected; do not reset or re-execute the same run.' -ForegroundColor Yellow
    Write-Host 'For later evidence collection, use the path printed above with g4b_capture.py.'
}
exit $code
