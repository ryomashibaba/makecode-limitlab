@echo off
setlocal
title G4C7 P2 - Native Blender Operator One-Shot LOCAL AI Trial - ART HOLD
echo G4C7 P2: ONE local AI native operator study; NO Work, NO Minecraft.
echo No install or Git clone is required. The verified v3 file remains untouched.
set "SCRIPT=%TEMP%\G4C7_P2_NATIVE_OPERATOR_%RANDOM%_%RANDOM%.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ProgressPreference='SilentlyContinue'; Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/ryomashibaba/makecode-limitlab/99065244c6d5cc099f3383a9e9e36762cbcee74b/tools/g4c7_m37p2_run_native_operator_first_pair.ps1' -OutFile '%SCRIPT%' -UseBasicParsing; if ((Get-Item -LiteralPath '%SCRIPT%').Length -lt 4000) {throw 'Incomplete authoring script'}"
if errorlevel 1 (
  echo STOP: Could not fetch fixed audited script. No original Blender files changed.
  pause
  exit /b 1
)
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT%"
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" (
  echo.
  echo ART HOLD. Native model/Blender trial stopped safely. Existing original unchanged.
  echo Send the error text or the opened evidence folder.
  pause
  exit /b %RC%
)
echo.
echo TECH ONLY. Three real Cycles images and separate .blend, NOT approved city art.
echo Review screenshots and send the comparison for independent visual assessment.
pause
exit /b 0
