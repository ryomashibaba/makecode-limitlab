@echo off
powershell.exe -NoLogo -NoProfile -STA -ExecutionPolicy Bypass -File "%~dp0COPY_P16.ps1"
if errorlevel 1 (
  echo.
  echo COPY FAILED. Do not paste an unverified clipboard.
  echo SAFE FALLBACK: use makecode\PASTE_THIS_P16.ts if it was created.
  pause
  exit /b 1
)
pause
