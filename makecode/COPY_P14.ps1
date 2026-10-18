param([switch]$PrepareOnly)
$ErrorActionPreference = 'Stop'

# Preserve the exact source. Never report COPY OK for incomplete or mismatched data.
$src = Join-Path $PSScriptRoot 'limitlab_p1_4.ts'
if (-not (Test-Path -LiteralPath $src)) { throw 'Missing limitlab_p1_4.ts' }
$root = Join-Path (Join-Path $env:USERPROFILE 'Downloads') 'MakeCode_LimitLab'
$logs = Join-Path $root 'logs'
$results = Join-Path $root 'results'
[void][IO.Directory]::CreateDirectory($logs)
[void][IO.Directory]::CreateDirectory($results)

# Git on Windows can check out LF files using CRLF. Hash the normalized text
# rather than raw bytes; this preserves integrity without false failures.
$code = [IO.File]::ReadAllText($src, [Text.Encoding]::UTF8)
$normalizedSource = $code.Replace("`r`n", "`n").Replace("`r", "`n")
$shaCheck = [Security.Cryptography.SHA256]::Create()
try {
    $hashBytes = [Text.Encoding]::UTF8.GetBytes($normalizedSource)
    $fileHash = [BitConverter]::ToString($shaCheck.ComputeHash($hashBytes)).Replace('-', '').ToLowerInvariant()
} finally { $shaCheck.Dispose() }
if ($fileHash -ne '653bf4977d1e032f4ada85a9bbfcb02d5a927c4a1a3863c3d2cad2d71b4e73aa') { throw 'Source SHA256 verification failed. Do not paste.' }
# Use a consistent line ending in the resulting clipboard and fallback text.
$code = $normalizedSource
if ($code.Length -lt 10000 -or -not $code.StartsWith('// LIMITLAB P1.4 START') -or
    -not $code.Contains('// LIMITLAB P1.4 END') -or
    -not $code.Contains('player.onChat("labauto14"') -or
    -not $code.Contains('player.onChat("labstatus14"') -or
    -not $code.Contains('player.onChat("labstop14"')) {
    throw 'P1.4 source integrity check FAILED. Clipboard unchanged.'
}
if (-not $code.Contains('__P14_ROOT__')) { throw 'Output path marker missing.' }
$code = $code.Replace('__P14_ROOT__', $root.Replace('\', '/'))
if ($code.Contains('__P14_ROOT__')) { throw 'Output path marker unresolved.' }

# A standalone, precisely rendered fallback is always available, even if another
# Windows application temporarily locks or alters the clipboard.
$backup = Join-Path $PSScriptRoot 'PASTE_THIS_P14.ts'
[IO.File]::WriteAllText($backup, $code, ([System.Text.UTF8Encoding]::new($false)))
$fromDisk = [IO.File]::ReadAllText($backup, [Text.Encoding]::UTF8)
if ($fromDisk -cne $code) { throw 'Prepared backup file mismatch. Clipboard unchanged.' }

function Normalize-ClipboardText([string]$value) {
    if ($null -eq $value) { return '' }
    return $value.Replace("`r`n", "`n").Replace("`r", "`n").TrimEnd([char[]]@([char]13, [char]10))
}
function Sha256Text([string]$value) {
    $bytes = [Text.Encoding]::UTF8.GetBytes($value)
    $sha = [Security.Cryptography.SHA256]::Create()
    try { return [BitConverter]::ToString($sha.ComputeHash($bytes)).Replace('-', '').ToLowerInvariant() }
    finally { $sha.Dispose() }
}
$expected = Normalize-ClipboardText $code
Write-Host ('Source verified: ' + $code.Length + ' characters; SHA256 ' + (Sha256Text $expected))
Write-Host ('Prepared file: ' + $backup)
if ($PrepareOnly) {
    Write-Host 'PREPARE PASS: validated file. Clipboard intentionally untouched.' -ForegroundColor Green
    exit 0
}

# Windows PowerShell 5.1 is STA by default; the CMD entry point forces STA as well.
# Use the Windows Forms clipboard API for both set and get to avoid cmdlet-specific
# LF/CRLF and raw-text representation differences.
if ([Threading.Thread]::CurrentThread.GetApartmentState() -ne [Threading.ApartmentState]::STA) {
    throw 'Clipboard requires STA. Run COPY_P14.cmd (it starts PowerShell with -STA).'
}
Add-Type -AssemblyName System.Windows.Forms
$verified = $false
$lastError = ''
$lastActual = ''
for ($attempt = 1; $attempt -le 5; $attempt++) {
    try {
        [System.Windows.Forms.Clipboard]::SetText($code, [System.Windows.Forms.TextDataFormat]::UnicodeText)
        Start-Sleep -Milliseconds 120
        $actual = [System.Windows.Forms.Clipboard]::GetText([System.Windows.Forms.TextDataFormat]::UnicodeText)
        $lastActual = Normalize-ClipboardText $actual
        if ($expected -ceq $lastActual) {
            $verified = $true
            break
        }
        $lastError = 'Clipboard content differs after readback.'
    } catch {
        $lastError = $_.Exception.Message
    }
    Start-Sleep -Milliseconds (150 * $attempt)
}
if (-not $verified) {
    Write-Host ('Expected length: ' + $expected.Length + ' / Readback length: ' + $lastActual.Length) -ForegroundColor Yellow
    Write-Host ('Expected SHA256: ' + (Sha256Text $expected))
    Write-Host ('Readback SHA256: ' + (Sha256Text $lastActual))
    Write-Host ('Last error: ' + $lastError) -ForegroundColor Yellow
    Write-Host ('SAFE FALLBACK: open ' + $backup + ' in Notepad, Ctrl+A, Ctrl+C, then paste into MakeCode.') -ForegroundColor Yellow
    throw 'Clipboard could not be verified after 5 attempts; please use the prepared file.'
}
Write-Host 'COPY OK: P1.4 COMPLETE CODE verified with Windows clipboard API' -ForegroundColor Green
Write-Host ('Characters: ' + $code.Length)
Write-Host 'Paste in MakeCode, press Play, then enter labauto14.'
