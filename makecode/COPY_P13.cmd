@echo off
powershell.exe -NoLogo -NoProfile -STA -ExecutionPolicy Bypass -File "%~dp0COPY_P13.ps1"
if errorlevel 1 (
  echo.
  echo COPY FAILED. Do not paste an unverified clipboard.
  echo Safe fallback: open makecode\PASTE_THIS_P13.ts, Ctrl+A, Ctrl+C.
  pause
  exit /b 1
)
pause
