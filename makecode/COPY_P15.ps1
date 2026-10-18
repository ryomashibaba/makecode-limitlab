param([switch]$PrepareOnly)
$ErrorActionPreference = 'Stop'
$src = Join-Path $PSScriptRoot 'limitlab_p1_5.ts'
if (-not (Test-Path -LiteralPath $src)) { throw 'Missing limitlab_p1_5.ts' }
$code = [IO.File]::ReadAllText($src, [Text.Encoding]::UTF8)
$cr = [string][char]13
$lf = [string][char]10
$code = $code.Replace(($cr + $lf), $lf).Replace($cr, $lf)
if ($code.Length -lt 8500 -or -not $code.StartsWith('// LIMITLAB P1.5 START') -or
    -not $code.Contains('// LIMITLAB P1.5 END') -or
    -not $code.Contains('player.onChat("labauto15"') -or
    -not $code.Contains('player.onChat("labstatus15"') -or
    -not $code.Contains('player.onChat("labstop15"')) {
    throw 'P1.5 incomplete or unexpected source. No copy attempted.'
}
# Pin the Git blob SHA1; normalize CRLF before hashing to support Windows checkout.
$bytes = [Text.Encoding]::UTF8.GetBytes($code)
$header = [Text.Encoding]::ASCII.GetBytes("blob " + $bytes.Length + [char]0)
$blob = New-Object byte[] ($header.Length + $bytes.Length)
[Array]::Copy($header, 0, $blob, 0, $header.Length)
[Array]::Copy($bytes, 0, $blob, $header.Length, $bytes.Length)
$sha = [Security.Cryptography.SHA1]::Create()
try { $actualSha = [BitConverter]::ToString($sha.ComputeHash($blob)).Replace('-', '').ToLowerInvariant() }
finally { $sha.Dispose() }
if ($actualSha -cne '95fd9934acd11fe6f35d6d5f78ad35c017a71b1d') {
    throw ('P1.5 source Git blob SHA mismatch: ' + $actualSha + '. Clipboard unchanged.')
}
$root = Join-Path (Join-Path $env:USERPROFILE 'Downloads') 'MakeCode_LimitLab'
[void][IO.Directory]::CreateDirectory((Join-Path $root 'logs'))
[void][IO.Directory]::CreateDirectory((Join-Path $root 'results'))
if (-not $code.Contains('__P15_ROOT__')) { throw 'Output directory marker missing.' }
$code = $code.Replace('__P15_ROOT__', $root.Replace('\','/'))
if ($code.Contains('__P15_ROOT__')) { throw 'Output directory marker unresolved.' }
$fallback = Join-Path $PSScriptRoot 'PASTE_THIS_P15.ts'
[IO.File]::WriteAllText($fallback, $code, (New-Object Text.UTF8Encoding($false)))
if ([IO.File]::ReadAllText($fallback, [Text.Encoding]::UTF8) -cne $code) {
    throw 'Fallback file readback mismatch: aborting.'
}
Write-Host ('Source OK. ' + $code.Length + ' characters; Git blob ' + $actualSha)
Write-Host ('Fallback file: ' + $fallback)
if ($PrepareOnly) {
    Write-Host 'PREPARE PASS (clipboard untouched)' -ForegroundColor Green
    exit 0
}
if ([Threading.Thread]::CurrentThread.GetApartmentState() -ne [Threading.ApartmentState]::STA) {
    throw 'Run COPY_P15.cmd; STA clipboard required.'
}
Add-Type -AssemblyName System.Windows.Forms
function Normalize([string]$s) {
    if ($null -eq $s) { return '' }
    return $s.Replace(($cr + $lf), $lf).Replace($cr, $lf).TrimEnd([char[]]@([char]13,[char]10))
}
$expected = Normalize $code
$ok = $false
$lastError = ''
for ($attempt=1; $attempt -le 5; $attempt++) {
    try {
        [Windows.Forms.Clipboard]::SetText($code, [Windows.Forms.TextDataFormat]::UnicodeText)
        Start-Sleep -Milliseconds 120
        $actual = [Windows.Forms.Clipboard]::GetText([Windows.Forms.TextDataFormat]::UnicodeText)
        if ($expected -ceq (Normalize $actual)) { $ok = $true; break }
        $lastError = 'Clipboard readback mismatch.'
    } catch { $lastError = $_.Exception.Message }
    Start-Sleep -Milliseconds (150 * $attempt)
}
if (-not $ok) {
    Write-Host ('Copy verification failed: ' + $lastError) -ForegroundColor Yellow
    Write-Host ('Fallback: open ' + $fallback + ' and Ctrl+A / Ctrl+C') -ForegroundColor Yellow
    throw 'Clipboard mismatch after 5 retries. Do NOT paste from clipboard.'
}
Write-Host 'COPY OK: P1.5 code fully verified in clipboard' -ForegroundColor Green
Write-Host 'Paste into MakeCode JavaScript, then use labauto15 in a disposable test world.'
