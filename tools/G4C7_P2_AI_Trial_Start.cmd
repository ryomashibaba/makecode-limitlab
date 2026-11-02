@echo off
setlocal
chcp 65001 >nul
title G4C7 P2 Local AI Vertex Trial - ART HOLD
set "DEST=%TEMP%\G4C7_P2_AUDITED_AI_TRIAL_%RANDOM%.ps1"
echo G4-C7 M37-P2: Local Ollama trial (no Work, no Minecraft writes)
echo Downloading the project script pinned to a fixed GitHub commit...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ProgressPreference='SilentlyContinue'; Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/ryomashibaba/makecode-limitlab/11a55e339894b8680c3239cadfa9c835ce73ea25/tools/g4c7_m37p2_run_local_ai_vertex_trial.ps1' -OutFile '%DEST%' -UseBasicParsing; if ((Get-Item -LiteralPath '%DEST%').Length -lt 4000) { throw 'Incomplete file' }"
if errorlevel 1 (
  echo Could not download the pinned script. No Blender data changed.
  pause
  exit /b 1
)
powershell -NoProfile -ExecutionPolicy Bypass -File "%DEST%"
set "EXIT=%ERRORLEVEL%"
if not "%EXIT%"=="0" (
  echo.
  echo The local model or strict geometry checks stopped the trial. ART HOLD.
  echo Your existing Blender remains unchanged; check the session folder.
  pause
  exit /b %EXIT%
)
echo.
echo The trial report and 3 genuine PNGs, if generated, are in the automatically opened folder.
echo These are UNAPPROVED and must be judged; they are NOT completed city art.
pause
exit /b 0
