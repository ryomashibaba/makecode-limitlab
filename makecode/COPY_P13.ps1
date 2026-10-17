$ErrorActionPreference = 'Stop'
$src = Join-Path $PSScriptRoot 'endurance_p1_3.ts'
if (-not (Test-Path -LiteralPath $src)) { throw 'Missing endurance_p1_3.ts' }
$root = Join-Path (Join-Path $env:USERPROFILE 'Downloads') 'MakeCode_LimitLab'
[IO.Directory]::CreateDirectory((Join-Path $root 'logs')) | Out-Null
[IO.Directory]::CreateDirectory((Join-Path $root 'results')) | Out-Null
$code = [IO.File]::ReadAllText($src, [Text.Encoding]::UTF8)
if ($code.Length -lt 3500 -or -not $code.StartsWith('// LIMITLAB P1.3 START') -or -not $code.Contains('// LIMITLAB P1.3 END')) { throw 'Incomplete P1.3 source; aborting' }
$code = $code.Replace('__P13_ROOT__', $root.Replace('\','/'))
if ($code.Contains('__P13_ROOT__')) { throw 'Output directory marker unresolved' }
Set-Clipboard -Value $code
$actual = Get-Clipboard -Raw
$norm = { param([string]$v) (($v -replace "`r`n", "`n").TrimEnd([char]13,[char]10)) }
if ((& $norm $code) -cne (& $norm $actual)) { throw 'Clipboard verification failed' }
Write-Host 'COPY OK: P1.3 COMPLETE CODE' -ForegroundColor Green
Write-Host ('Characters: ' + $code.Length)
Write-Host 'Paste in MakeCode, press Play, then enter labrun13.'
