$ErrorActionPreference='Stop'
$repo = Split-Path -Parent $PSScriptRoot
$source=Join-Path $repo 'makecode/limitlab_stair_bench_a1c.ts'
if(-not (Test-Path -LiteralPath $source)){throw 'Missing isolated stair bench source. Nothing copied.'}
$s=[IO.File]::ReadAllText($source,[Text.Encoding]::UTF8).Replace("`r`n","`n").Replace("`r","`n")
if(-not $s.StartsWith('// LIMITLAB STB A1C START') -or
   -not $s.Contains('// LIMITLAB STB A1C END') -or
   -not $s.Contains('player.onChat("labstbonce"') -or
   -not $s.Contains('blocks.blockWithData(109,d)')){
   throw 'Unexpected A1C source. Clipboard unchanged.'
}
$b=[Text.Encoding]::UTF8.GetBytes($s)
$header=[Text.Encoding]::ASCII.GetBytes("blob "+$b.Length+[char]0)
$packed=New-Object byte[] ($header.Length+$b.Length)
[Array]::Copy($header,0,$packed,0,$header.Length)
[Array]::Copy($b,0,$packed,$header.Length,$b.Length)
$sha=[Security.Cryptography.SHA1]::Create()
try { $actual=[BitConverter]::ToString($sha.ComputeHash($packed)).Replace('-','').ToLowerInvariant() }
finally { $sha.Dispose() }
if($actual -cne '961d99eba8ccb24a649873837b2125112a20f0ca'){
 throw ('STAIR BENCH SHA mismatch '+$actual+'. Clipboard unchanged.')
}
Set-Clipboard -Value $s
$back=(Get-Clipboard -Raw).Replace("`r`n","`n").Replace("`r","`n").TrimEnd([char]10)
if($back -cne $s.TrimEnd([char]10)){throw 'Clipboard verification failed. DO NOT paste or run.'}
Write-Host 'A1C VERIFIED AND COPIED. NO WORLD OR FILE DATA CHANGED.' -ForegroundColor Green
Write-Host '1. Open a BRAND-NEW DISPOSABLE SUPERFLAT Minecraft Education world.'
Write-Host '2. MakeCode > JavaScript > Ctrl+A then Ctrl+V; check zero editor errors.'
Write-Host '3. Stand on level solid flat ground, 50+ empty blocks in the east/south quadrant.'
Write-Host '4. Type labstbonce ONLY ONCE. Four 6-stair flights, 24 blocks total.'
Write-Host '5. With Auto Jump OFF, try ordinary walking East/West/South/North up all 6 steps.'
Write-Host '6. Report whether all four face correctly and ascend WITHOUT jump.'
Write-Host 'NEVER use this bench on existing G4C4/G4C5 city. NEVER repeat after STOP.'
