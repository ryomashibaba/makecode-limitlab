param([switch]$PrepareOnly)
$ErrorActionPreference = 'Stop'
$src = Join-Path $PSScriptRoot 'endurance_p1_3.ts'
if (-not (Test-Path -LiteralPath $src)) { throw 'Missing endurance_p1_3.ts' }
$root = Join-Path (Join-Path $env:USERPROFILE 'Downloads') 'MakeCode_LimitLab'
[void][IO.Directory]::CreateDirectory((Join-Path $root 'logs'))
[void][IO.Directory]::CreateDirectory((Join-Path $root 'results'))
$code = [IO.File]::ReadAllText($src, [Text.Encoding]::UTF8)
if ($code.Length -lt 3500 -or -not $code.StartsWith('// LIMITLAB P1.3 START') -or
    -not $code.Contains('// LIMITLAB P1.3 END') -or
    -not $code.Contains('player.onChat("labrun13"') -or
    -not $code.Contains('player.onChat("labstatus13"') -or
    -not $code.Contains('player.onChat("labstop13"')) {
    throw 'P1.3 source integrity check FAILED. Clipboard unchanged.'
}
if (-not $code.Contains('__P13_ROOT__')) { throw 'Output path marker missing.' }
$code = $code.Replace('__P13_ROOT__', $root.Replace('\', '/'))
if ($code.Contains('__P13_ROOT__')) { throw 'Output path marker unresolved.' }
$backup = Join-Path $PSScriptRoot 'PASTE_THIS_P13.ts'
[IO.File]::WriteAllText($backup, $code, ([System.Text.UTF8Encoding]::new($false)))
$fromDisk = [IO.File]::ReadAllText($backup, [Text.Encoding]::UTF8)
if ($fromDisk -cne $code) { throw 'Prepared backup file mismatch. Clipboard unchanged.' }

function Normalize-ClipboardText([string]$value) {
    if ($null -eq $value) { return '' }
    $cr = [string][char]13
    $lf = [string][char]10
    return $value.Replace(($cr + $lf), $lf).Replace($cr, $lf).TrimEnd([char[]]@([char]13, [char]10))
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

if ([Threading.Thread]::CurrentThread.GetApartmentState() -ne [Threading.ApartmentState]::STA) {
    throw 'Clipboard requires STA. Run COPY_P13.cmd (it starts PowerShell with -STA).'
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
Write-Host 'COPY OK: P1.3 COMPLETE CODE verified with Windows clipboard API' -ForegroundColor Green
Write-Host ('Characters: ' + $code.Length)
Write-Host 'Paste in MakeCode, press Play, then enter labrun13.'
