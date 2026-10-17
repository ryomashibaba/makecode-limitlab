$ErrorActionPreference = 'Stop'
$source = Join-Path $PSScriptRoot 'main.ts'
if (-not (Test-Path -LiteralPath $source)) { throw 'main.ts not found.' }
$root = Join-Path (Join-Path $env:USERPROFILE 'Downloads') 'MakeCode_LimitLab'
$logs = Join-Path $root 'logs'
$results = Join-Path $root 'results'
[IO.Directory]::CreateDirectory($logs) | Out-Null
[IO.Directory]::CreateDirectory($results) | Out-Null
$script = [IO.File]::ReadAllText($source,[Text.Encoding]::UTF8)
if ($script.Length -lt 12000 -or -not $script.StartsWith('// LIMITLAB P1.0 START') -or -not $script.Contains('// LIMITLAB P1.0 END')) { throw 'Incomplete source: aborting clipboard update.' }
if (-not $script.Contains('__P1_ROOT__')) { throw 'Output path marker is missing.' }
$script = $script.Replace('__P1_ROOT__', $root.Replace('\','/'))
if ($script.Contains('__P1_ROOT__')) { throw 'Unable to configure output directory.' }
Set-Clipboard -Value $script
$readback = Get-Clipboard -Raw
$normalize = { param([string]$s) (($s -replace "`r`n", "`n").TrimEnd([char]13,[char]10)) }
if ((& $normalize $script) -cne (& $normalize $readback)) { throw 'Clipboard verification failed; do not paste.' }
Write-Host 'COPY OK: COMPLETE LIMITLAB P1.0 CODE' -ForegroundColor Green
Write-Host ('Code characters: '+$script.Length)
Write-Host ('Logs: '+$logs)
Write-Host ('Results: '+$results)
Write-Host 'Paste in MakeCode JavaScript with Ctrl+A, Ctrl+V; press Play; enter labauto1.'
