@echo off
powershell.exe -NoProfile -NoLogo -STA -ExecutionPolicy Bypass -File "%~dp0COPY_P20.ps1"
if errorlevel 1 (
  echo COPY FAILED. Do not paste unverified clipboard.
  echo If available, open PASTE_THIS_P20.ts and copy its contents manually.
  pause
  exit /b 1
)
pause
