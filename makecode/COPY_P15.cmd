@echo off
powershell.exe -NoLogo -NoProfile -STA -ExecutionPolicy Bypass -File "%~dp0COPY_P15.ps1"
if errorlevel 1 (
  echo P1.5 COPY FAILED. Do not paste an unverified clipboard.
  echo If generated, open makecode\PASTE_THIS_P15.ts to copy manually.
  pause
  exit /b 1
)
pause
