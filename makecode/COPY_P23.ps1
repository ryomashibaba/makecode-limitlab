param([switch]$PrepareOnly, [string]$OutputRoot)
$ErrorActionPreference = 'Stop'
$source = Join-Path $PSScriptRoot 'limitlab_p2_3.ts'
if (-not (Test-Path -LiteralPath $source)) { throw 'P2.3 source not found' }
$code = [IO.File]::ReadAllText($source,[Text.Encoding]::UTF8)
$cr = [string][char]13
$lf = [string][char]10
$code = $code.Replace(($cr+$lf),$lf).Replace($cr,$lf)
if ($code.Length -lt 12000 -or -not $code.StartsWith('// LIMITLAB P2.3 START') -or
    -not $code.Contains('// LIMITLAB P2.3 END') -or
    -not $code.Contains('player.onChat("labcity23"') -or
    -not $code.Contains('player.onChat("labarea23"') -or
    -not $code.Contains('player.onChat("labstatus23"') -or
    -not $code.Contains('player.onChat("labstop23"') -or
    -not $code.Contains('TEST FINISHED') -or
    -not $code.Contains('TEST STOPPED')) {
    throw 'P2.3 incomplete or unexpected source. Clipboard unchanged.'
}
# Pin checked-in source to exact Git blob (after standardizing line endings).
$bytes = [Text.Encoding]::UTF8.GetBytes($code)
$header = [Text.Encoding]::ASCII.GetBytes("blob " + $bytes.Length + [char]0)
$blob = New-Object byte[] ($header.Length + $bytes.Length)
[Array]::Copy($header,0,$blob,0,$header.Length)
[Array]::Copy($bytes,0,$blob,$header.Length,$bytes.Length)
$sha = [Security.Cryptography.SHA1]::Create()
try {
    $actual = [BitConverter]::ToString($sha.ComputeHash($blob)).Replace('-','').ToLowerInvariant()
} finally { $sha.Dispose() }
if ($actual -cne 'c807f0c797ba1325961ee6a848edf15b50cb65b9') {
    throw ('P2.3 source checksum mismatch: ' + $actual + '. Clipboard unchanged.')
}
$root = if ($OutputRoot) { [IO.Path]::GetFullPath($OutputRoot) } else { Join-Path (Join-Path $env:USERPROFILE 'Downloads') 'MakeCode_LimitLab' }
[void][IO.Directory]::CreateDirectory((Join-Path $root 'results'))
[void][IO.Directory]::CreateDirectory((Join-Path $root 'logs'))
$latch = Join-Path $root 'logs/P23_ONCE.txt'
if (-not (Test-Path -LiteralPath $latch)) {
    [IO.File]::WriteAllText($latch,'READY_P23',(New-Object Text.UTF8Encoding($false)))
}
if ([IO.File]::ReadAllText($latch) -cne 'READY_P23') {
    Write-Host 'P2.3 one-shot latch already used: runtime will refuse. Do not reset or retry.' -ForegroundColor Yellow
}
if (-not $code.Contains('__P23_ROOT__')) { throw 'Missing local output path placeholder' }
$code = $code.Replace('__P23_ROOT__', $root.Replace('\','/'))
if ($code.Contains('__P23_ROOT__')) { throw 'Unresolved output directory' }
$fallback = Join-Path $PSScriptRoot 'PASTE_THIS_P23.ts'
[IO.File]::WriteAllText($fallback,$code,(New-Object Text.UTF8Encoding($false)))
if ([IO.File]::ReadAllText($fallback,[Text.Encoding]::UTF8) -cne $code) {
    throw 'P2.3 fallback file mismatched. Clipboard untouched.'
}
Write-Host ('Verified source Git blob: ' + $actual)
Write-Host ('Prepared fallback: ' + $fallback)
if ($PrepareOnly) {
    Write-Host 'PREPARE PASS. Clipboard not accessed.' -ForegroundColor Green
    exit 0
}
if ([Threading.Thread]::CurrentThread.GetApartmentState() -ne [Threading.ApartmentState]::STA) {
    throw 'STA clipboard required: run COPY_P23.cmd'
}
Add-Type -AssemblyName System.Windows.Forms
function NormalizeClipboard([string]$value) {
    if ($null -eq $value) { return '' }
    return $value.Replace(($cr+$lf),$lf).Replace($cr,$lf).TrimEnd([char[]]@([char]13,[char]10))
}
$expected = NormalizeClipboard $code
$success = $false
$lastError = ''
for($attempt=1;$attempt -le 5;$attempt++) {
    try {
        [System.Windows.Forms.Clipboard]::SetText($code,[System.Windows.Forms.TextDataFormat]::UnicodeText)
        Start-Sleep -Milliseconds 120
        $actualClipboard = [System.Windows.Forms.Clipboard]::GetText([System.Windows.Forms.TextDataFormat]::UnicodeText)
        if ($expected -ceq (NormalizeClipboard $actualClipboard)) {
            $success = $true
            break
        }
        $lastError = 'UnicodeText clipboard readback mismatch'
    } catch { $lastError = $_.Exception.Message }
    Start-Sleep -Milliseconds (150*$attempt)
}
if (-not $success) {
    Write-Host ('Copy mismatch: ' + $lastError) -ForegroundColor Yellow
    Write-Host ('Use fallback ' + $fallback) -ForegroundColor Yellow
    throw 'COPY FAILED after five attempts; do not paste unverified clipboard'
}
Write-Host 'COPY OK: P2.3 verified complete source placed on clipboard' -ForegroundColor Green
Write-Host 'Paste into MakeCode JS. Keep File Read & Write extension; then labarea23 to preview, and labcity23 ONCE (FAST sampled).'
