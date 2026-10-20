param([switch]$PrepareOnly, [Parameter(Mandatory=$true)][string]$OutputRoot)
$ErrorActionPreference = 'Stop'
$source = Join-Path $PSScriptRoot 'limitlab_g4c3_a2.ts'
if (-not (Test-Path -LiteralPath $source)) { throw 'G4C3 source not found' }
$code = [IO.File]::ReadAllText($source,[Text.Encoding]::UTF8)
$cr = [string][char]13
$lf = [string][char]10
$code = $code.Replace(($cr+$lf),$lf).Replace($cr,$lf)
if ($code.Length -lt 12000 -or -not $code.StartsWith('// LIMITLAB G4C3 START') -or
    -not $code.Contains('// LIMITLAB G4C3 END') -or
    -not $code.Contains('player.onChat("labcityg4c3"') -or
    -not $code.Contains('player.onChat("labareag4c3"') -or
    -not $code.Contains('player.onChat("labstatusg4c3"') -or
    -not $code.Contains('player.onChat("labstopg4c3"') -or
    -not $code.Contains('TEST FINISHED') -or
    -not $code.Contains('TEST STOPPED')) {
    throw 'G4C3 incomplete or unexpected source. Clipboard unchanged.'
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
if ($actual -cne '82c90c63f1637492b503882ae8a745d8a0db6b9e') {
    throw ('G4C3 source checksum mismatch: ' + $actual + '. Clipboard unchanged.')
}
$root = [IO.Path]::GetFullPath($OutputRoot)
# Mandatory brand-new run root. NEVER reset or overwrite previous run evidence.
if ([IO.Directory]::Exists($root) -or [IO.File]::Exists($root)) {
    throw ('A1 requires a fresh run folder. Existing folder preserved: ' + $root)
}
$parent = [IO.Path]::GetDirectoryName($root)
$walk = $parent
while ($walk -and [IO.Directory]::Exists($walk)) {
    $attr = [IO.File]::GetAttributes($walk)
    if (($attr -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
        throw ('Output parent is a link/junction: ' + $walk)
    }
    $above = [IO.Path]::GetDirectoryName($walk)
    if (-not $above -or $above -eq $walk) { break }
    $walk = $above
}

[void][IO.Directory]::CreateDirectory((Join-Path $root 'results'))
[void][IO.Directory]::CreateDirectory((Join-Path $root 'logs'))
$latch = Join-Path $root 'logs/G4C3_ONCE.txt'
if (-not (Test-Path -LiteralPath $latch)) {
    [IO.File]::WriteAllText($latch,'READY_G4C3',(New-Object Text.UTF8Encoding($false)))
}
$csv = Join-Path $root 'results/USER_UPLOAD_THIS_G4C3_STATUS.csv'
if (Test-Path -LiteralPath $csv) {
    throw 'Existing G4C3 result CSV preserved. Do not overwrite or reset the latch.'
}
if ([IO.File]::ReadAllText($latch) -cne 'READY_G4C3') {
    throw 'Existing G4C3 one-shot latch not READY. No copy/retry.'
}
if (-not $code.Contains('__G4C3_ROOT__')) { throw 'Missing local output path placeholder' }
$code = $code.Replace('__G4C3_ROOT__', $root.Replace('\','/'))
if ($code.Contains('__G4C3_ROOT__')) { throw 'Unresolved output directory' }
$fallback = Join-Path $root 'PASTE_THIS_G4C3_A2.ts'
[IO.File]::WriteAllText($fallback,$code,(New-Object Text.UTF8Encoding($false)))
if ([IO.File]::ReadAllText($fallback,[Text.Encoding]::UTF8) -cne $code) {
    throw 'G4C3 fallback file mismatched. Clipboard untouched.'
}
Write-Host ('Verified source Git blob: ' + $actual)
Write-Host ('Prepared fallback: ' + $fallback)
if ($PrepareOnly) {
    Write-Host 'PREPARE PASS. Clipboard not accessed.' -ForegroundColor Green
    exit 0
}
if ([Threading.Thread]::CurrentThread.GetApartmentState() -ne [Threading.ApartmentState]::STA) {
    throw 'STA clipboard required: run RUN_G4C3_A2.cmd'
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
Write-Host 'COPY OK: G4C3 verified complete source placed on clipboard' -ForegroundColor Green
Write-Host 'Paste into MakeCode JS. Keep File Read & Write extension; then labareag4c3 to preview, and labcityg4c3 ONCE (FAST sampled).'
