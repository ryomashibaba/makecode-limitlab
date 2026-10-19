param([switch]$PrepareOnly, [string]$OutputRoot)
$ErrorActionPreference = 'Stop'
$source = Join-Path $PSScriptRoot 'limitlab_p2_3.ts'
if (-not (Test-Path -LiteralPath $source)) { throw 'P2.4R source not found' }
$code = [IO.File]::ReadAllText($source,[Text.Encoding]::UTF8)
$cr = [string][char]13
$lf = [string][char]10
$code = $code.Replace(($cr+$lf),$lf).Replace($cr,$lf)
if ($code.Length -lt 12000 -or -not $code.StartsWith('// LIMITLAB P2.4R START') -or
    -not $code.Contains('// LIMITLAB P2.4R END') -or
    -not $code.Contains('player.onChat("labcity24r"') -or
    -not $code.Contains('player.onChat("labarea24r"') -or
    -not $code.Contains('player.onChat("labstatus24r"') -or
    -not $code.Contains('player.onChat("labstop24r"') -or
    -not $code.Contains('TEST FINISHED') -or
    -not $code.Contains('TEST STOPPED')) {
    throw 'P2.4R incomplete or unexpected source. Clipboard unchanged.'
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
if ($actual -cne 'd23ef8e3269f9198df8880e49194c10b64f15346') {
    throw ('P2.4R source checksum mismatch: ' + $actual + '. Clipboard unchanged.')
}
$root = if ($OutputRoot) { [IO.Path]::GetFullPath($OutputRoot) } else { Join-Path (Join-Path $env:USERPROFILE 'Downloads') 'MakeCode_LimitLab/P24R_R1' }
[void][IO.Directory]::CreateDirectory((Join-Path $root 'results'))
[void][IO.Directory]::CreateDirectory((Join-Path $root 'logs'))
$latch = Join-Path $root 'logs/P24R_ONCE.txt'
if (-not (Test-Path -LiteralPath $latch)) {
    [IO.File]::WriteAllText($latch,'READY_P24R',(New-Object Text.UTF8Encoding($false)))
}
$csv = Join-Path $root 'results/USER_UPLOAD_THIS_P24R_STATUS.csv'
if (Test-Path -LiteralPath $csv) {
    throw 'Existing P2.4R result CSV preserved. Do not overwrite or reset the latch.'
}
if ([IO.File]::ReadAllText($latch) -cne 'READY_P24R') {
    throw 'Existing P2.4R one-shot latch not READY. No copy/retry.'
}
if (-not $code.Contains('__P24R_ROOT__')) { throw 'Missing local output path placeholder' }
$code = $code.Replace('__P24R_ROOT__', $root.Replace('\','/'))
if ($code.Contains('__P24R_ROOT__')) { throw 'Unresolved output directory' }
$fallback = Join-Path $PSScriptRoot 'PASTE_THIS_P24R_R1.ts'
[IO.File]::WriteAllText($fallback,$code,(New-Object Text.UTF8Encoding($false)))
if ([IO.File]::ReadAllText($fallback,[Text.Encoding]::UTF8) -cne $code) {
    throw 'P2.4R fallback file mismatched. Clipboard untouched.'
}
Write-Host ('Verified source Git blob: ' + $actual)
Write-Host ('Prepared fallback: ' + $fallback)
if ($PrepareOnly) {
    Write-Host 'PREPARE PASS. Clipboard not accessed.' -ForegroundColor Green
    exit 0
}
if ([Threading.Thread]::CurrentThread.GetApartmentState() -ne [Threading.ApartmentState]::STA) {
    throw 'STA clipboard required: run COPY_P24R.cmd'
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
Write-Host 'COPY OK: P2.4R verified complete source placed on clipboard' -ForegroundColor Green
Write-Host 'Paste into MakeCode JS. Keep File Read & Write extension; then labarea24r to preview, and labcity24r ONCE (FAST sampled).'
