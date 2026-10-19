$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$root = Join-Path (Join-Path $env:USERPROFILE 'Downloads') 'MakeCode_LimitLab/P24R_R1'
$copy = Join-Path $repo 'makecode/COPY_P24R.ps1'
$observer = Join-Path $PSScriptRoot 'p24r_capture.py'
if (-not (Test-Path -LiteralPath $copy) -or -not (Test-Path -LiteralPath $observer)) {
    throw 'Incomplete P2.4R repository. No preparation performed.'
}
Write-Host 'P2.4R recovery: independent source/latch/CSV; old P2.3 kept untouched.'
Write-Host 'P2.4R: preparing SHA-verified clipboard on dedicated path...'
& powershell.exe -NoLogo -NoProfile -STA -ExecutionPolicy Bypass -File $copy -OutputRoot $root
if ($LASTEXITCODE -ne 0) {
    throw 'P2.4R preparation failed. Do not paste unverified clipboard.'
}
Write-Host ''
Write-Host 'PREPARED P2.4R. Open an unused disposable LimitLab test world.' -ForegroundColor Green
Write-Host '1. In MakeCode JavaScript: Ctrl+A, Ctrl+V; keep File Read & Write extension.'
Write-Host '2. Type labarea24r to preview safe Y >=96 (floating test city).'
Write-Host '3. Type labcity24r ONCE in a disposable world only.'
Write-Host '4. If PRECHECK BLOCKED appears, move the player and call labcity24r again.'
Write-Host '   (The failed AIR precheck spends NO persistent latch and writes NO CSV.)'
Write-Host '5. If a real run starts, do not repeat. The observer will package the CSV.'
Write-Host 'P2.3 old run/CSV/latch are never reused.'
Write-Host ''
Write-Host 'Waiting for new P2.4R terminal CSV for up to 20 minutes...'
& python -B $observer --output-root $root --wait 1200
$code = $LASTEXITCODE
if ($code -eq 0) {
    Write-Host 'G4: private ZIP ready in Downloads\MakeCode_LimitLab\P24R_R1\private_results.' -ForegroundColor Green
} else {
    Write-Host 'No new terminal evidence ZIP; do not reset the latch.' -ForegroundColor Yellow
    Write-Host 'To collect an existing completed CSV later: python -B tools/p24r_capture.py'
}
exit $code
