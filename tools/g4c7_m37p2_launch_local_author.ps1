# MakeCode LimitLab G4-C7 M37-P2: one-command REAL local artist editor session.
# This is a launcher, NOT a city generator. It does not modify GitHub or Minecraft.
# Tested on Windows PowerShell syntax by source inspection only; Blender 5.2 GUI
# compatibility cannot be claimed until a real local desktop run.
[CmdletBinding()]
param(
    [string]$BlenderExe = "",
    [string]$WorkspaceRoot = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# SHA-locked genuine Blender 4.5.15 empty artist studio (not an art deliverable).
$sourceCommit = "3c05ba86814443bb3b6d44718dae50a855fea083"
$relativeSource = "artifacts/g4c7-m37p2-patched-native-author-editor-v3-NOT-ART/M37P2_DIRECT_AUTHOR_NATIVE_EDITOR_FIXED_REVIEW_V3_NOT_ART.blend"
$expectedSourceSha256 = "536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249"
$source = $null
$temporary = $null
$sessionCreated = $false

function Test-P2Sha256([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return $false }
    return ((Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() -eq $expectedSourceSha256)
}

function Find-Blender([string]$Explicit) {
    if ($Explicit) {
        if (-not (Test-Path -LiteralPath $Explicit -PathType Leaf)) {
            throw "BLENDER_EXE_NOT_FOUND: $Explicit"
        }
        return (Resolve-Path -LiteralPath $Explicit).Path
    }
    $command = Get-Command blender.exe -ErrorAction SilentlyContinue
    if ($command -and $command.Source -and (Test-Path -LiteralPath $command.Source)) {
        return $command.Source
    }

    $found = @()
    foreach ($programRoot in @($env:ProgramFiles, [Environment]::GetFolderPath("ProgramFilesX86"))) {
        if ([string]::IsNullOrWhiteSpace($programRoot)) { continue }
        $foundation = Join-Path $programRoot "Blender Foundation"
        if (-not (Test-Path -LiteralPath $foundation -PathType Container)) { continue }
        $found += @(Get-ChildItem -LiteralPath $foundation -Directory -ErrorAction SilentlyContinue |
            ForEach-Object {
                $exe = Join-Path $_.FullName "blender.exe"
                if (Test-Path -LiteralPath $exe -PathType Leaf) {
                    [pscustomobject]@{ Path = $exe; Version = $_.Name }
                }
            })
    }
    if ($found.Count -gt 0) {
        # Installed Blender 5.2/5.2.1 will be chosen over older installations.
        return (@($found | Sort-Object Version -Descending)[0]).Path
    }
    throw "BLENDER_EXE_NOT_FOUND: Specify -BlenderExe 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'"
}

try {
    # Find a *correct-hash* existing local source; never trust a same-named wrong file.
    $repoRoot = Split-Path -Parent $PSScriptRoot
    $localCandidates = @(
        (Join-Path $repoRoot $relativeSource),
        (Join-Path (Get-Location).Path $relativeSource),
        (Join-Path (Join-Path $env:USERPROFILE "Projects\makecode-limitlab") $relativeSource)
    )
    foreach ($candidate in $localCandidates) {
        if (Test-P2Sha256 $candidate) {
            $source = $candidate
            break
        }
    }
    if (-not $source) {
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        $temporary = Join-Path ([IO.Path]::GetTempPath()) ("g4c7-p2-source-" + [Guid]::NewGuid().ToString("N") + ".blend")
        $url = "https://raw.githubusercontent.com/ryomashibaba/makecode-limitlab/$sourceCommit/$relativeSource"
        Write-Host "Downloading pinned P2 v3 Blender source (not changing GitHub) ..."
        Invoke-WebRequest -Uri $url -OutFile $temporary -UseBasicParsing
        if (-not (Test-P2Sha256 $temporary)) {
            throw "SOURCE_SHA256_MISMATCH_DOWNLOAD_ABORTED"
        }
        $source = $temporary
    }

    $blender = Find-Blender $BlenderExe
    if ([string]::IsNullOrWhiteSpace($WorkspaceRoot)) {
        $WorkspaceRoot = Join-Path ([Environment]::GetFolderPath("MyDocuments")) "G4C7\P2_Author_Sessions"
    }
    # Refuse accidentally placing a session inside a protected repo archive.
    if ($WorkspaceRoot -match "[\\/]artifacts[\\/]") {
        throw "WORKSPACE_MUST_NOT_BE_WITHIN_PROTECTED_ARTIFACTS"
    }
    New-Item -ItemType Directory -Path $WorkspaceRoot -Force | Out-Null
    $suffix = [Guid]::NewGuid().ToString("N").Substring(0, 6)
    $sessionName = "P2_DIRECT_ART_" + (Get-Date -Format "yyyyMMdd_HHmmss") + "_" + $suffix
    $sessionDir = Join-Path $WorkspaceRoot $sessionName
    New-Item -ItemType Directory -Path $sessionDir -ErrorAction Stop | Out-Null
    $sessionCreated = $true
    $workBlend = Join-Path $sessionDir "P2_DIRECT_AUTHOR_UNAPPROVED.blend"
    Copy-Item -LiteralPath $source -Destination $workBlend -ErrorAction Stop
    if (-not (Test-P2Sha256 $workBlend)) {
        throw "LOCAL_WORKING_COPY_SHA256_MISMATCH"
    }

    # Bootstrap only registers existing GUI tools and splits the viewport.
    # No mesh/object/city generation, no save operation, no official ART approval.
    $bootstrap = @'
import bpy
import traceback

SCRIPTS = (
    "M37P2_RUN_ONCE_PARALLEL_MACRO_LIVED_GUI.py",
    "M37P2_RUN_ONCE_NATIVE_REVIEW_BUTTON.py",
    "M37P2_RUN_ONCE_ENABLE_AUTHOR_REVIEW_PANEL.py",
)

def activate_p2_direct_author():
    if bpy.app.background:
        print("G4C7_AUTHOR_BOOTSTRAP_NOT_INTERACTIVE", flush=True)
        return None
    if bpy.context.scene.get("P2_ART") != "HOLD":
        print("G4C7_AUTHOR_BOOTSTRAP_UNEXPECTED_CHARTER", flush=True)
        return None
    for filename in SCRIPTS:
        embedded = bpy.data.texts.get(filename)
        if embedded is None:
            print("G4C7_AUTHOR_BOOTSTRAP_MISSING_SCRIPT", filename, flush=True)
            continue
        try:
            context = {
                "__name__": "g4c7_author_bootstrap_module_" + filename.replace(".", "_"),
                "__file__": filename,
            }
            exec(compile(embedded.as_string(), filename, "exec"), context)
            context["register"]()
            print("G4C7_AUTHOR_BOOTSTRAP_REGISTERED", filename, flush=True)
        except Exception:
            traceback.print_exc()
    window = bpy.context.window
    if not window:
        print("G4C7_AUTHOR_BOOTSTRAP_NO_WINDOW", flush=True)
        return None
    screen = window.screen
    area = next((a for a in screen.areas if a.type == "VIEW_3D"), None)
    if area is None:
        print("G4C7_AUTHOR_BOOTSTRAP_NO_VIEW3D", flush=True)
        return None
    region = next((r for r in area.regions if r.type == "WINDOW"), None)
    if region is None:
        print("G4C7_AUTHOR_BOOTSTRAP_NO_WINDOW_REGION", flush=True)
        return None
    try:
        with bpy.context.temp_override(window=window, screen=screen, area=area, region=region):
            result = bpy.ops.g4c7.p2_parallel_split()
            print("G4C7_AUTHOR_BOOTSTRAP_SPLIT", result, flush=True)
    except Exception:
        traceback.print_exc()
    print("G4C7_DIRECT_AUTHOR_READY_NO_MESHES_CREATED_ART_HOLD", flush=True)
    return None

bpy.app.timers.register(activate_p2_direct_author, first_interval=1.5)
'@
    $bootstrapPath = Join-Path $sessionDir "P2_GUI_BOOTSTRAP_NO_GEOMETRY.py"
    [IO.File]::WriteAllText($bootstrapPath, $bootstrap, [Text.UTF8Encoding]::new($false))

    $readme = @'
G4-C7 / M37-P2 DIRECT ART EDITING SESSION (NOT ART YET)

A real copy of the fixed v3 Blender master is opened in GUI. This session is
intended for direct author modelling, not an automatic third primitive city.
The 2-viewport script, author declaration panel, and 3-view review panel are
registered automatically when they are available.

AUTHOR GOAL: one integrated dense urban form + genuinely lived-in shipyard,
staff/visitor boundary, research/culture daylight space, private deep rooms
and real entrances/windows. Both city skyline and human space must appear in
the SAME saved native scene. Do not import/recycle rejected P1/O1 geometry.

Within Blender:
  1. Directly model the living city and real interior section in the 5
     P2_*_DIRECT_AUTHOR collections. This launcher never makes geometry.
  2. Reposition the 3 provisional cameras for actual aerial / public / home.
  3. Author panel: approve 3 camera positions and mark for early art review
     after actual distinct geometry exists in all five collections.
  4. SAVE, CLOSE and REOPEN the authored blend. For robust repeat reviews,
     save to a new name, not the original GitHub NOT_ART master.
  5. P2 Early Art Review sidebar: render the same source .blend into 3 PNG
     images for strict independent ART review. A passing technical check is
     NOT an artistic pass. If failure occurs, preserve the source and logs.

ART HOLD; official adoptions 0; 331/993 NOT RUN; G0/S1/G1/G2/G3 NOT RUN;
MakeCode NOT EVALUATED; Minecraft world writes 0; main and PR #53 unchanged.
Workspace: local only. Do not merge, publish, or build in Minecraft.
'@
    $readmePath = Join-Path $sessionDir "READ_ME_FIRST_P2_AUTHOR.txt"
    [IO.File]::WriteAllText($readmePath, $readme, [Text.UTF8Encoding]::new($false))
    $manifest = [ordered]@{
        schema = "g4c7-m37p2-local-author-session-v1"
        status = "UNAUTHORED_COPY_NOT_ART"
        source_sha256 = $expectedSourceSha256
        source_commit = $sourceCommit
        created_utc = [DateTime]::UtcNow.ToString("o")
        blender_exe = $blender
        source_blend = "P2_DIRECT_AUTHOR_UNAPPROVED.blend"
        bootstrap = "P2_GUI_BOOTSTRAP_NO_GEOMETRY.py"
        official_art_adoptions = 0
        art = "HOLD"
        formal_331_993 = "NOT_RUN"
        minecraft = "FORBIDDEN"
        github_changes = "NONE_BY_LAUNCHER"
    }
    [IO.File]::WriteAllText(
        (Join-Path $sessionDir "P2_SESSION_MANIFEST.json"),
        ($manifest | ConvertTo-Json -Depth 8),
        [Text.UTF8Encoding]::new($false)
    )

    if (-not (Test-P2Sha256 $source)) {
        throw "IMMUTABLE_SOURCE_CHANGED_DURING_LOCAL_LAUNCH"
    }
    Write-Host "Verified source SHA-256: $expectedSourceSha256"
    Write-Host "Opening directly editable Blender copy: $workBlend"
    Write-Host "No meshes generated; ART HOLD; Minecraft untouched."
    $args = ('"{0}" --python "{1}"' -f $workBlend, $bootstrapPath)
    $process = Start-Process -FilePath $blender -ArgumentList $args -PassThru
    Write-Host ("Blender started. PID: " + $process.Id)
    try {
        Start-Process -FilePath "explorer.exe" -ArgumentList ('"{0}"' -f $sessionDir) | Out-Null
    } catch {
        Write-Warning ("Could not open Explorer; manual session folder: " + $sessionDir)
    }
    Write-Host ("Session folder: " + $sessionDir)
} catch {
    Write-Error ("P2_LOCAL_LAUNCH_FAILED: " + $_.Exception.Message)
    exit 1
} finally {
    if ($temporary -and (Test-Path -LiteralPath $temporary)) {
        Remove-Item -LiteralPath $temporary -Force -ErrorAction SilentlyContinue
    }
}
