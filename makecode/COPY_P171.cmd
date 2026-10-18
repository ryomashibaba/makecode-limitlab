@echo off
powershell.exe -NoProfile -NoLogo -STA -ExecutionPolicy Bypass -File "%~dp0COPY_P171.ps1"
if errorlevel 1 (
  echo COPY FAILED. Do not paste unverified clipboard.
  echo Open PASTE_THIS_P171.ts if prepared and copy it manually.
  pause
  exit /b 1
)
pause
