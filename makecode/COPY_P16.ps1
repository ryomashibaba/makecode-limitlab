param([switch]$PrepareOnly)
$ErrorActionPreference = 'Stop'

# Read the exact reviewed P1.6 source; never silently accept a damaged paste.
$source = Join-Path $PSScriptRoot 'limitlab_p1_6.ts'
if (-not (Test-Path -LiteralPath $source)) { throw 'Missing limitlab_p1_6.ts' }
$code = [IO.File]::ReadAllText($source, [Text.Encoding]::UTF8)
$code = $code.Replace("`r`n", "`n").Replace("`r", "`n")
$sha = [Security.Cryptography.SHA256]::Create()
try {
    $rawHash = [BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($code))).Replace('-', '').ToLowerInvariant()
} finally { $sha.Dispose() }
$expectedHash = 'c519391314b8243f757d76dc79a880ddbcbd405c942ceb0826151f8f69b70dc4'
if ($rawHash -cne $expectedHash) { throw ('P1.6 source checksum MISMATCH. Do not paste: ' + $rawHash) }
if ($code.Length -lt 11000 -or -not $code.StartsWith('// LIMITLAB P1.6 START') -or
    -not $code.Contains('// LIMITLAB P1.6 END') -or
    -not $code.Contains('player.onChat("labauto16"') -or
    -not $code.Contains('player.onChat("labstatus16"') -or
    -not $code.Contains('player.onChat("labstop16"') -or
    -not $code.Contains('player.onChat("labprobe16"')) {
    throw 'P1.6 structural integrity check failed. Clipboard not touched.'
}
$root = Join-Path (Join-Path $env:USERPROFILE 'Downloads') 'MakeCode_LimitLab'
[void][IO.Directory]::CreateDirectory((Join-Path $root 'logs'))
[void][IO.Directory]::CreateDirectory((Join-Path $root 'results'))
if (-not $code.Contains('__P16_ROOT__')) { throw 'Missing root placeholder.' }
$code = $code.Replace('__P16_ROOT__', $root.Replace('\', '/'))
if ($code.Contains('__P16_ROOT__')) { throw 'Root substitution failed.' }

# Safe fallback is always written and read back before attempting clipboard.
$fallback = Join-Path $PSScriptRoot 'PASTE_THIS_P16.ts'
[IO.File]::WriteAllText($fallback, $code, (New-Object Text.UTF8Encoding($false)))
$readback = [IO.File]::ReadAllText($fallback, [Text.Encoding]::UTF8)
if ($readback -cne $code) { throw 'Saved fallback readback mismatch. Clipboard not touched.' }
Write-Host ('SOURCE OK: ' + $code.Length + ' chars; SHA256 ' + $rawHash)
Write-Host ('Verified fallback file: ' + $fallback)
if ($PrepareOnly) {
    Write-Host 'PREPARE PASS: clipboard intentionally unchanged' -ForegroundColor Green
    exit 0
}

if ([Threading.Thread]::CurrentThread.GetApartmentState() -ne [Threading.ApartmentState]::STA) {
    throw 'Clipboard requires STA. Use COPY_P16.cmd.'
}
Add-Type -AssemblyName System.Windows.Forms
function Normalize-ClipboardText([string]$value) {
    if ($null -eq $value) { return '' }
    return $value.Replace("`r`n", "`n").Replace("`r", "`n").TrimEnd([char[]]@([char]13,[char]10))
}
$expected = Normalize-ClipboardText $code
$verified = $false
$lastMessage = ''
for ($attempt = 1; $attempt -le 5; $attempt++) {
    try {
        [System.Windows.Forms.Clipboard]::SetText($code, [System.Windows.Forms.TextDataFormat]::UnicodeText)
        Start-Sleep -Milliseconds 120
        $actual = [System.Windows.Forms.Clipboard]::GetText([System.Windows.Forms.TextDataFormat]::UnicodeText)
        if ($expected -ceq (Normalize-ClipboardText $actual)) { $verified = $true; break }
        $lastMessage = 'Clipboard readback mismatch after UnicodeText copy.'
    } catch { $lastMessage = $_.Exception.Message }
    Start-Sleep -Milliseconds (150 * $attempt)
}
if (-not $verified) {
    Write-Host ('COPY FAILURE: ' + $lastMessage) -ForegroundColor Yellow
    Write-Host ('SAFE FALLBACK: open ' + $fallback + ', then Ctrl+A and Ctrl+C to copy.') -ForegroundColor Yellow
    throw 'Clipboard verification failed 5 times; no COPY OK emitted.'
}
Write-Host 'COPY OK: P1.6 full source verified in Windows clipboard.' -ForegroundColor Green
Write-Host 'Next: paste into MakeCode JS, press Play, then labauto16 in disposable test world.'
