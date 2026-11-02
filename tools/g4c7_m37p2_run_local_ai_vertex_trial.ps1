# P2 local AI *explicit vertex* first-art trial. One command, no Work.
# CLI generates an UNAPPROVED proposal from locally installed Ollama Qwen,
# validates its authored vertices, opens a SEPARATE headless Blender process,
# saves fresh .blend and 3 genuine render PNGs. Never changes user's open Blender.
[CmdletBinding()]
param(
    [string]$Model = "qwen3:14b",
    [string]$SessionRoot = "",
    [string]$BlenderExe = "",
    [switch]$PrepareOnly
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$expectedSha = "536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249"
# Pin code at a concrete commit; no remote unreviewed branch execution.
$codeCommit = "784ed3c8eb8d326c10293e6bb49a669e084ba90f"
$sourceName = "P2_DIRECT_AUTHOR_UNAPPROVED.blend"
$scriptFile = "g4c7_m37p2_local_vertex_author.py"

function Find-VerifiedEmptyAuthorCopy([string]$Root) {
    if (-not (Test-Path -LiteralPath $Root -PathType Container)) {
        throw "G4C7_AUTHOR_SESSION_ROOT_NOT_FOUND: $Root. Start the verified v3 launcher first."
    }
    $choices = @(Get-ChildItem -LiteralPath $Root -Directory -ErrorAction Stop |
        Sort-Object LastWriteTime -Descending)
    foreach ($directory in $choices) {
        $candidate = Join-Path $directory.FullName $sourceName
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            $hash = (Get-FileHash -LiteralPath $candidate -Algorithm SHA256).Hash.ToLowerInvariant()
            if ($hash -eq $expectedSha) {
                return [pscustomobject]@{ Folder = $directory.FullName; Native = $candidate }
            }
        }
    }
    throw "PINNED_EMPTY_V3_NOT_FOUND_OR_USER_WORKING_COPY_MODIFIED. Do not overwrite existing edits."
}

function Find-BlenderExe([string]$Requested) {
    if ($Requested) {
        if (-not (Test-Path -LiteralPath $Requested -PathType Leaf)) {
            throw "BLENDER_BIN_NOT_FOUND: $Requested"
        }
        return (Resolve-Path -LiteralPath $Requested).Path
    }
    $programDirectories = @($env:ProgramFiles, [Environment]::GetFolderPath("ProgramFilesX86"))
    $found = @()
    foreach ($directory in $programDirectories) {
        if (-not $directory) { continue }
        $base = Join-Path $directory "Blender Foundation"
        if (-not (Test-Path -LiteralPath $base -PathType Container)) { continue }
        $found += @(Get-ChildItem -LiteralPath $base -Directory -ErrorAction SilentlyContinue |
            ForEach-Object {
                $e = Join-Path $_.FullName "blender.exe"
                if (Test-Path -LiteralPath $e -PathType Leaf) {
                    [pscustomobject]@{ File = $e; Version = $_.Name }
                }
            })
    }
    if ($found.Count -gt 0) {
        return (@($found | Sort-Object Version -Descending)[0]).File
    }
    $cmd = Get-Command blender.exe -ErrorAction SilentlyContinue
    if ($cmd -and $cmd.Source) { return $cmd.Source }
    throw "BLENDER_NOT_INSTALLED_OR_NOT_FOUND"
}

function Find-Python {
    $p = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($p -and $p.Source) { return [pscustomobject]@{ File = $p.Source; Args = @() } }
    $py = Get-Command py.exe -ErrorAction SilentlyContinue
    if ($py -and $py.Source) { return [pscustomobject]@{ File = $py.Source; Args = @("-3") } }
    throw "PYTHON_NOT_FOUND"
}

try {
    if (-not $SessionRoot) {
        $SessionRoot = Join-Path ([Environment]::GetFolderPath("MyDocuments")) "G4C7\P2_Author_Sessions"
    }
    $base = Find-VerifiedEmptyAuthorCopy $SessionRoot
    $blender = Find-BlenderExe $BlenderExe
    $python = Find-Python

    $trial = Join-Path $base.Folder ("LOCAL_AI_EXPLICIT_VERTEX_TRIAL_" +
        (Get-Date -Format "yyyyMMdd_HHmmss") + "_" + [Guid]::NewGuid().ToString("N").Substring(0,6))
    New-Item -ItemType Directory -Path $trial -ErrorAction Stop | Out-Null

    # Explicitly download an audited script only. Ollama output is JSON data
    # and is never evaluated as Python code.
    $runner = Join-Path $trial $scriptFile
    $remote = "https://raw.githubusercontent.com/ryomashibaba/makecode-limitlab/$codeCommit/tools/$scriptFile"
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $remote -OutFile $runner -UseBasicParsing

    $native = Join-Path $trial "P2_NATIVE_LLM_VERTEX_ART_HOLD"
    $plan = Join-Path $trial "P2_LOCAL_LLM_VERTEX_PLAN.json"
    $readme = Join-Path $trial "RESULT_README_FIRST_JA.txt"
    @'
このフォルダは M37-P2 のローカルAIによる未採用の実3D造形「実験」です。

- 既存Blenderで開いている作業画面は変更しません。
- AIが一つ一つの頂点とポリゴンの形をJSONで提案します。
- 単純な箱だけ・5用途の欠落・実立体の不足は検査で不採用にします。
- 通過した場合のみ別のBlender処理で新BLENDと3つのPNG画像を保存。
- ここでのPASSは技術検証だけ。美術的に不合格なら即停止します。
- 新都市のMinecraft施工はしません。正本のGitHub/mainは触りません。
- 正式ART採用0件、331/993 NOT RUN、Minecraft FORBIDDEN。
- これはGUI直接作者の実制作と同一視できません。
'@ | Set-Content -LiteralPath $readme -Encoding UTF8

    $first = [ordered]@{
        schema = "g4c7-local-llm-explicit-vertex-trial-v1"
        source_sha256 = $expectedSha
        local_author_source = $base.Native
        local_model = $Model
        art = "HOLD"
        official_adoptions = 0
        formal_331_993 = "NOT_RUN"
        minecraft = "FORBIDDEN"
        gui_direct_author = "NOT_PERFORMED"
        source_master_modified = $false
        state = "PREPARED_ONLY_NOT_ART"
    }
    $first | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $trial "SAFE_PREPARE_MANIFEST.json") -Encoding UTF8

    if ($PrepareOnly) {
        Write-Host ("P2_SAFE_LOCAL_AI_PREPARE_ONLY: " + $trial)
        return
    }

    # Check the user's existing local Ollama; start it without installing any
    # packages when available. This is a foreground user-invoked local trial,
    # not a ChatGPT background task or Work usage.
    $tags = $null
    try {
        $tags = Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags" -Method Get -TimeoutSec 4
    } catch {
        $ollama = Get-Command ollama.exe -ErrorAction SilentlyContinue
        $ollamaPath = if ($ollama -and $ollama.Source) { $ollama.Source } else {
            Join-Path $env:LOCALAPPDATA "Programs\Ollama\ollama.exe"
        }
        if (-not (Test-Path -LiteralPath $ollamaPath -PathType Leaf)) {
            throw "OLLAMA_NOT_RUNNING_AND_EXECUTABLE_NOT_FOUND. This trial never installs models."
        }
        Write-Host "Starting already-installed local Ollama server..."
        Start-Process -FilePath $ollamaPath -ArgumentList "serve" -WindowStyle Hidden | Out-Null
        for ($attempt=0; $attempt -lt 12; $attempt++) {
            Start-Sleep -Seconds 2
            try {
                $tags = Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags" -Method Get -TimeoutSec 3
                break
            } catch {}
        }
        if ($null -eq $tags) {
            throw "LOCAL_OLLAMA_COULD_NOT_BE_STARTED. No Blender source changed."
        }
    }
    $modelNames = @($tags.models | ForEach-Object { $_.name })
    if (-not (($modelNames -contains $Model) -or
            ($modelNames | Where-Object { $_ -like ($Model + "-*") }))) {
        throw ("LOCAL_MODEL_MISSING: " + $Model + ". Available: " + ($modelNames -join ", "))
    }

    Write-Host "LOCAL_AI_STAGE_1: Ollama creates explicit vertex/face author proposal (no executable generated code)."
    $pythonArgs = @($python.Args) + @($runner, "--mode", "propose", "--model", $Model, "--out", $plan)
    & $python.File @pythonArgs
    if ($LASTEXITCODE -ne 0) {
        Write-Warning ("ART_HOLD: candidate rejected before any Blender geometry. Evidence folder: " + $trial)
        Start-Process -FilePath explorer.exe -ArgumentList ('"{0}"' -f $trial) | Out-Null
        exit 2
    }

    Write-Host "LOCAL_AI_STAGE_2: Actual native Blender render of unapproved model. Open Blender window remains unchanged."
    & $blender --background --factory-startup --python $runner -- --mode render --plan $plan --source $base.Native --out $native
    if ($LASTEXITCODE -ne 0) {
        throw ("NATIVE_BLEND_RENDER_FAILED: stage 2; evidence folder " + $trial)
    }
    $evidence = Join-Path $native "P2_LOCAL_AI_NATIVE_ART_HOLD_REPORT.json"
    if (-not (Test-Path -LiteralPath $evidence)) { throw "NATIVE_RENDER_EVIDENCE_MISSING" }
    $result = Get-Content -LiteralPath $evidence -Raw | ConvertFrom-Json
    if ($result.art -ne "HOLD" -or $result.official_adoptions -ne 0 -or
        $result.Minecraft -ne "FORBIDDEN" -or $result.original_v3_sha256 -ne $expectedSha) {
        throw "ART_OR_SOURCE_INTEGRITY_BROKEN"
    }
    if ((Get-FileHash -LiteralPath $base.Native -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expectedSha) {
        throw "LOCAL_EMPTY_SOURCE_WAS_CHANGED"
    }
    Start-Process -FilePath explorer.exe -ArgumentList ('"{0}"' -f $native) | Out-Null
    Write-Host ("LOCAL_AI_NATIVE_THREE_EYE_TRIAL_READY_FOR_STRICT_ART_CRITIQUE: " + $native)
    Write-Host "New meshes exist only in the separate trial file; ART HOLD, adoption 0, Minecraft untouched."
} catch {
    Write-Error ("P2_LOCAL_AI_AUTHOR_TRIAL_STOPPED_HOLD: " + $_.Exception.Message)
    exit 1
}
