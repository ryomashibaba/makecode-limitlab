param([switch]$PrepareOnly)
$ErrorActionPreference = 'Stop'
$source = Join-Path $PSScriptRoot 'limitlab_p1_8.ts'
if (-not (Test-Path -LiteralPath $source)) { throw 'P1.8 source not found' }
$code = [IO.File]::ReadAllText($source,[Text.Encoding]::UTF8)
$cr = [string][char]13
$lf = [string][char]10
$code = $code.Replace(($cr+$lf),$lf).Replace($cr,$lf)
if ($code.Length -lt 12000 -or -not $code.StartsWith('// LIMITLAB P1.8 START') -or
    -not $code.Contains('// LIMITLAB P1.8 END') -or
    -not $code.Contains('player.onChat("labauto18"') -or
    -not $code.Contains('player.onChat("labstatus18"') -or
    -not $code.Contains('player.onChat("labstop18"') -or
    -not $code.Contains('TEST FINISHED') -or
    -not $code.Contains('TEST STOPPED')) {
    throw 'P1.8 incomplete or unexpected source. Clipboard unchanged.'
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
if ($actual -cne '27d7feb2c49d95ade6ce0a089a0c56299ab5e30a') {
    throw ('P1.8 source checksum mismatch: ' + $actual + '. Clipboard unchanged.')
}
$root = Join-Path (Join-Path $env:USERPROFILE 'Downloads') 'MakeCode_LimitLab'
[void][IO.Directory]::CreateDirectory((Join-Path $root 'results'))
[void][IO.Directory]::CreateDirectory((Join-Path $root 'logs'))
if (-not $code.Contains('__P18_ROOT__')) { throw 'Missing local output path placeholder' }
$code = $code.Replace('__P18_ROOT__', $root.Replace('\','/'))
if ($code.Contains('__P18_ROOT__')) { throw 'Unresolved output directory' }
$fallback = Join-Path $PSScriptRoot 'PASTE_THIS_P18.ts'
[IO.File]::WriteAllText($fallback,$code,(New-Object Text.UTF8Encoding($false)))
if ([IO.File]::ReadAllText($fallback,[Text.Encoding]::UTF8) -cne $code) {
    throw 'P1.8 fallback file mismatched. Clipboard untouched.'
}
Write-Host ('Verified source Git blob: ' + $actual)
Write-Host ('Prepared fallback: ' + $fallback)
if ($PrepareOnly) {
    Write-Host 'PREPARE PASS. Clipboard not accessed.' -ForegroundColor Green
    exit 0
}
if ([Threading.Thread]::CurrentThread.GetApartmentState() -ne [Threading.ApartmentState]::STA) {
    throw 'STA clipboard required: run COPY_P18.cmd'
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
Write-Host 'COPY OK: P1.8 verified complete source placed on clipboard' -ForegroundColor Green
Write-Host 'Paste into MakeCode JS. Keep File Read & Write extension; then labauto18.'
