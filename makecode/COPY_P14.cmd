@echo off
powershell.exe -NoLogo -NoProfile -STA -ExecutionPolicy Bypass -File "%~dp0COPY_P14.ps1"
if errorlevel 1 (
  echo COPY FAILED. Do not paste unverified contents.
  echo Use the PASTE_THIS_P14.ts fallback in this folder.
  pause
  exit /b 1
)
pause
