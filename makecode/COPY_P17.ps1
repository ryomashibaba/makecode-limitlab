param([switch]$PrepareOnly)
$ErrorActionPreference = 'Stop'

$source = Join-Path $PSScriptRoot 'limitlab_p1_7.ts'
if (-not (Test-Path -LiteralPath $source)) { throw 'P1.7 MakeCode source missing' }
$code = [IO.File]::ReadAllText($source, [Text.Encoding]::UTF8)
$cr = [string][char]13
$lf = [string][char]10
$code = $code.Replace(($cr + $lf), $lf).Replace($cr, $lf)
if ($code.Length -lt 10500 -or -not $code.StartsWith('// LIMITLAB P1.7 START') -or
    -not $code.Contains('// LIMITLAB P1.7 END') -or
    -not $code.Contains('player.onChat("labauto17"') -or
    -not $code.Contains('player.onChat("labstatus17"') -or
    -not $code.Contains('player.onChat("labstop17"') -or
    -not $code.Contains('TEST FINISHED') -or
    -not $code.Contains('TEST STOPPED')) {
    throw 'Incomplete or unexpected P1.7 source; clipboard untouched.'
}
# SHA pinned to reviewed GitHub blob, independent of Windows line endings.
$bytes = [Text.Encoding]::UTF8.GetBytes($code)
$header = [Text.Encoding]::ASCII.GetBytes("blob " + $bytes.Length + [char]0)
$inputBytes = New-Object byte[] ($header.Length + $bytes.Length)
[Array]::Copy($header, 0, $inputBytes, 0, $header.Length)
[Array]::Copy($bytes, 0, $inputBytes, $header.Length, $bytes.Length)
$sha = [Security.Cryptography.SHA1]::Create()
try {
    $actual = [BitConverter]::ToString($sha.ComputeHash($inputBytes)).Replace('-', '').ToLowerInvariant()
} finally { $sha.Dispose() }
if ($actual -cne 'e24519d440648fe2c8eba89378e036f13a99c1bc') {
    throw ('P1.7 source hash mismatch: ' + $actual + '. Clipboard unchanged.')
}
$root = Join-Path (Join-Path $env:USERPROFILE 'Downloads') 'MakeCode_LimitLab'
[void][IO.Directory]::CreateDirectory((Join-Path $root 'results'))
[void][IO.Directory]::CreateDirectory((Join-Path $root 'logs'))
if (-not $code.Contains('__P17_ROOT__')) { throw 'Output root placeholder missing' }
$code = $code.Replace('__P17_ROOT__', $root.Replace('\', '/'))
if ($code.Contains('__P17_ROOT__')) { throw 'Output root placeholder unresolved' }
$backup = Join-Path $PSScriptRoot 'PASTE_THIS_P17.ts'
[IO.File]::WriteAllText($backup, $code, (New-Object Text.UTF8Encoding($false)))
if ([IO.File]::ReadAllText($backup, [Text.Encoding]::UTF8) -cne $code) {
    throw 'P1.7 backup file readback mismatch'
}
Write-Host ('SOURCE VERIFIED: ' + $code.Length + ' chars, git blob ' + $actual)
Write-Host ('Backup file: ' + $backup)
if ($PrepareOnly) {
    Write-Host 'PREPARE PASS: no clipboard access' -ForegroundColor Green
    exit 0
}
if ([Threading.Thread]::CurrentThread.GetApartmentState() -ne [Threading.ApartmentState]::STA) {
    throw 'Run COPY_P17.cmd: clipboard requires STA'
}
Add-Type -AssemblyName System.Windows.Forms
function Normalize([string]$value) {
    if ($null -eq $value) { return '' }
    return $value.Replace(($cr + $lf), $lf).Replace($cr, $lf).TrimEnd([char[]]@([char]13,[char]10))
}
$expect = Normalize $code
$verified = $false
$lastFailure = ''
for ($attempt=1; $attempt -le 5; $attempt++) {
    try {
        [System.Windows.Forms.Clipboard]::SetText($code, [Windows.Forms.TextDataFormat]::UnicodeText)
        Start-Sleep -Milliseconds 120
        $actualClip = [System.Windows.Forms.Clipboard]::GetText([Windows.Forms.TextDataFormat]::UnicodeText)
        if ($expect -ceq (Normalize $actualClip)) { $verified = $true; break }
        $lastFailure = 'Clipboard content mismatch'
    } catch { $lastFailure = $_.Exception.Message }
    Start-Sleep -Milliseconds (150 * $attempt)
}
if (-not $verified) {
    Write-Host ('Clipboard not verified: ' + $lastFailure) -ForegroundColor Yellow
    Write-Host ('Use backup manually: ' + $backup) -ForegroundColor Yellow
    throw 'P1.7 COPY FAILED: Do not paste an unverified clipboard'
}
Write-Host 'COPY OK: P1.7 exact source is on clipboard' -ForegroundColor Green
Write-Host 'In MakeCode JS: Ctrl+A, Ctrl+V. Keep File Read & Write extension.'
Write-Host 'Then use labauto17 in a disposable LimitLab-only world.'
